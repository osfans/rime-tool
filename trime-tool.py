#!/usr/bin/env python3
import os, sqlite3, logging, collections, itertools, sys, re, string
import glob, fnmatch
import yaml 

def get_schemas():
    return fnmatch.filter(sys.argv[1:], "*.schema.yaml")

def open_db():
    DB = 'trime.db'
    if os.path.exists(DB): os.remove(DB)
    conn = sqlite3.connect(DB)
    return conn

def close_db(conn):
    conn.commit()
    conn.close()

def opencc(opencc_dir):
    for fn in ("TSCharacters.txt", "TSPhrases.txt", "STCharacters.txt", "STPhrases.txt", \
                  "TWVariantsRevPhrases.txt", "HKVariantsRevPhrases.txt"):
        r = fn[:2].lower()
        if r in ("tw", "hk"): r = r + "2t"
        else: r = "%s2%s" % (r[0], r[1])
        for i in open(opencc_dir + fn, encoding="U8"):
            i = i.strip()
            if i:
                a = i.split('\t')
                yield a[0], a[1], r
    for fn in ("TWVariants.txt", "HKVariants.txt", "HKVariantsPhrases.txt", "JPVariants.txt", \
                 "TWPhrasesIT.txt", "TWPhrasesName.txt", "TWPhrasesOther.txt"):
        r = fn[:3].lower().rstrip('v')
        for i in open(opencc_dir + fn, encoding="U8"):
            i = i.strip()
            if i:
                a = i.split('\t')
                yield a[0], a[1], "t2%s" % r
                yield a[1], a[0], "%s2t" % r

def get_dict_name(fn, dic):
    bn = dic + ".dict.yaml"
    path = os.path.dirname(fn)
    fn = os.path.join(path, bn)
    if not os.path.exists(fn):
        fns = glob.glob("./brise/*/%s" % bn)
        if fns:
            return fns[0]
    return fn

def parse_schemas(schemas):
    count = 0
    for fn in schemas:
        yy = yaml.load(open(fn, encoding="U8").read().replace("\t", " "))
        l = [count]
        dicts.add(get_dict_name(fn, yy["translator"]["dictionary"]))
        l.append(yy["schema"]["schema_id"])
        l.append(yy["schema"]["name"])
        l.append(yaml.dump(yy))
        yield l
        count += 1
        logging.info("\t%s", yy["schema"]["name"])

def get_essaydict():
    d = collections.defaultdict(int)
    if not os.path.exists("brise"): return
    for i in open("brise/essay.txt", encoding="U8"):
        i=i.strip()
        if i:
            hz,weight=i.split()
            d[hz]=int(weight)
    return d

half = map(ord, string.punctuation + string.ascii_uppercase)
fullwidth = {i: i - 0x20+0xff00 for i in half}

def parse_dict(dicts):
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
            yy=yaml.load(y.replace("\t", " "))
            if yy.get("use_preset_vocabulary", False):
                phrase = set(filter(lambda x:1<len(x)<=yy.get("max_phrase_length", 6) and d[x]>=yy.get("min_phrase_weight", 1000), d.keys()))
            continue
        if isMB and line and not line.startswith("#"):
            fs = line.split("\t")
            l = len(fs)
            if l == 1:
                phrase.add(fs[0])
            elif l > 1:
                fs[1] = fs[1].translate(fullwidth)
                hz.append(fs[:2])
                if len(fs[0]) > 1 and fs[0] in phrase:
                    phrase.remove(fs[0])
                if l == 2:
                    zd[fs[0]].append(fs[1])
                elif l == 3:
                    if not fs[2].startswith("0"):
                        zd[fs[0]].append(fs[1])
                        if "%" not in fs[2]:
                            d[fs[0]] = int(float(fs[2]))
    for p in phrase:
        pp = list(map(lambda x: zd.get(x, False), p))
        if all(pp):        
            for i in itertools.product(*pp):
                hz.append([p," ".join(i)])

    if yy.get("sort", "original") == "by_weight":
        hz.sort(key=lambda x: d[x[0]] if d[x[0]] > 0 else 1000, reverse = True)

    table = yy.get("name", os.path.basename(fn).split(".")[0])
    return table, hz

if len(sys.argv) == 1:
    print("請指定方案集schema.yaml文件！")
    exit(0)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

conn = open_db()
cursor = conn.cursor()

schemas = get_schemas()
dicts=set()

opencc_dir = "OpenCC/data/dictionary/"
if os.path.exists(opencc_dir):
    logging.info("簡繁")
    cursor.execute("CREATE VIRTUAL TABLE opencc USING fts3(s, t, r)")
    cursor.executemany('INSERT INTO opencc VALUES (?, ?, ?)', opencc(opencc_dir))

logging.info("方案")
cursor.execute('CREATE TABLE schema (_id INTEGER PRIMARY KEY, schema_id, name, full)')
cursor.executemany('INSERT INTO schema VALUES (?, ?, ?, ?)', parse_schemas(schemas))

logging.info("詞庫")
d = get_essaydict()

logging.info("字典")
for fn in dicts:
    table, hz = parse_dict(fn)
    logging.info("\t%s 詞條数 %d", table, len(hz))
    cursor.execute('CREATE VIRTUAL TABLE "%s" USING fts3(hz, py)' % table)
    cursor.executemany('INSERT INTO "{0}" VALUES(?, ?)'.format(table), hz)

close_db(conn)
logging.info("碼表")
