#!/usr/bin/env python3
import os, sqlite3, logging, collections, itertools, sys, re
import yaml 

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

schemas = sys.argv[1:]
if len(schemas) == 0:
    schemas = ["thaerv", "thaerv_ipa", "soutseu", "pinyin", "zhuyin"]
    logging.info("使用默認方案集:%s", schemas)
else:
    logging.info("使用指定方案集:%s", schemas)

DB = 'trime.db'
if os.path.exists(DB): os.remove(DB)
conn = sqlite3.connect(DB)
cursor = conn.cursor()

logging.info("essay詞庫")
hasPhrase = False
d=collections.defaultdict(int)
for i in open("data/essay.txt", encoding="U8"):
    i=i.strip()
    if i:
        hz,weight=i.split()
        d[hz]=int(weight)

logging.info("opencc簡化")
cursor.execute("CREATE VIRTUAL TABLE opencc USING fts3(t,s)")
for fn in ("opencc/TSCharacters.txt", "opencc/TSPhrases.txt"):
    for i in open(fn, encoding="U8"):
        i=i.strip()
        if i: cursor.execute('insert into opencc values (?,?)', i.split('\t'))

logging.info("方案")
sql = """
CREATE TABLE schema (
    "_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "version" TEXT,
    "author" TEXT,
    "description" TEXT,
    "dictionary" TEXT NOT NULL,
    "phrase" TEXT,
    "delimiter" TEXT,
    "alphabet" TEXT,
    "syllable" TEXT,
    "auto_select_syllable" TEXT,
    "keyboard" TEXT,
    "pyspell" TEXT,
    "py2ipa" TEXT,
    "ipa2py" TEXT,
    "ipafuzzy" TEXT
)"""
cursor.execute(sql)

dicts=set()
count = 0

for fn in schemas:
    yy = yaml.load(open("data/%s.schema.yaml" % fn, encoding="U8"))
    l = [count]
    if "dictionary" not in yy["schema"] and "translator" in yy:
        yy["schema"]["dictionary"] = yy["translator"]["dictionary"]
    dicts.add(yy["schema"]["dictionary"])
    for i in "name,version,author,description,dictionary,phrase,delimiter,alphabet,syllable,auto_select_syllable,keyboard,pyspell,py2ipa,ipa2py,ipafuzzy".split(","):
        s = yy["schema"].get(i, yy["speller"].get(i, "") if "speller" in yy else "")
        if i == "phrase" and s == "phrase": hasPhrase = True
        if type(s) == list: s = "\n".join(map(lambda x: x if type(x)==str else "",s))
        l.append(s)
    cursor.execute('insert into schema values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', l)
    count += 1
    logging.info("\t%s", yy["schema"]["name"])

logging.info("碼表")

for fn in map(lambda x: "data/%s.dict.yaml" % x, dicts):
    hz = []
    zd = collections.defaultdict(list)
    mbStart = "..."
    isMB = False
    y = ""
    phrase = set()

    for line in open(fn, encoding="U8"):
        if not isMB:
            y+=line
        line = line.strip()
        if line.startswith(mbStart):
            isMB = True
            yy=yaml.load(y)
            if yy.get("use_preset_vocabulary", False):
                phrase = set(filter(lambda x:1<len(x)<=yy.get("max_phrase_length", 6) and d[x]>=yy.get("min_phrase_weight", 1000), d.keys()))
            continue
        if isMB and line and not line.startswith("#"):
            fs = line.split("\t")
            l = len(fs)
            if l == 1:
                phrase.add(fs[0])
            elif l > 1:
                hz.append(fs[0:2])
                if len(fs[0]) > 1 and fs[0] in phrase:
                    phrase.remove(fs[0])
                if l == 2:
                    zd[fs[0]].append(fs[1])
                elif l == 3:
                    if not fs[2].startswith("0"):
                        zd[fs[0]].append(fs[1])
                        if "%" not in fs[2]:
                            d[fs[0]] = int(fs[2])
    for p in phrase:
        pp = list(map(lambda x: zd.get(x, False), p))
        if all(pp):        
            for i in itertools.product(*pp):
                hz.append([p," ".join(i)])

    if yy.get("sort", "by_weight") == "by_weight":
        hz.sort(key=lambda x: d[x[0]] if d[x[0]] > 0 else 1000, reverse = True)

    table = yy.get("name", os.path.basename(fn).split(".")[0])
    cursor.execute('CREATE VIRTUAL TABLE %s USING fts3(hz, py, pl INTEGER DEFAULT (0), tokenize=simple "separators=@")' % table)
    py2ipa = yy.get("py2ipa", [])
    for i in hz:
        sql = 'insert into %s values (?, ?, 0)' % table
        for j in py2ipa:
            r = re.split("(?<!\\\\)/", j)
            if r[0] == "xlit":
                for a,b in zip(r[1].replace("\\",""),r[2].replace("\\","")):
                    i[1]=i[1].replace(a,b)
        cursor.execute(sql, i)
    logging.info("\t%s 詞條数 %d", table, len(hz))

if hasPhrase:
    logging.info("聯想詞庫")
    cursor.execute("CREATE VIRTUAL TABLE phrase USING fts3(hz)")
    for i in sorted(filter(lambda x: len(x) > 1 and d[x] > 600, d.keys()), key=lambda x: d[x], reverse = True):
        cursor.execute('insert into phrase values (?)', (i,))

conn.commit()
conn.close()
