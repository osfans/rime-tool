#!/usr/bin/env python3
import os, sqlite3, logging, collections, itertools, sys, re, string
import glob, fnmatch
import yaml 

def get_schemas():
    return fnmatch.filter(sys.argv[1:], "*.schema.yaml")

def open_db():
    DB = 'trime.db'
    asset = "trime/assets"
    if os.path.exists(asset): DB = os.path.join(asset, DB)
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
    if os.path.exists(fn):
        return os.path.abspath(fn)
    fns = glob.glob("brise/*/%s" % bn)
    if fns:
        return os.path.abspath(fns[0])

def parse_schemas(schemas):
    count = 0
    for fn in schemas:
        yy = yaml.load(open(fn, encoding="U8").read().replace("\t", " "))
        l = [count]
        schema_id = yy["schema"]["schema_id"]
        l.append(schema_id)
        l.append(yy["schema"]["name"])
        l.append(yaml.dump(yy))
        if "translator" in yy and "dictionary" in yy["translator"]:
            dictionary = yy["translator"]["dictionary"]
            dict_name = get_dict_name(fn, dictionary)
            if dict_name: dicts.add(dict_name)
            if "speller" in yy and "algebra" in yy["speller"]:
                algebras[schema_id] = dictionary, yy["speller"]["algebra"]
        yield l
        count += 1
        logging.info("\t%s", yy["schema"]["name"])

def get_essaydict():
    d = collections.defaultdict(int)
    if not os.path.exists("brise/essay.txt"): return
    for i in open("brise/essay.txt", encoding="U8"):
        i=i.strip()
        if i:
            hz,weight=i.split()
            d[hz]=int(weight)
    return d

half = map(ord, string.punctuation + string.ascii_uppercase)
fullwidth = {i: i - 0x20+0xff00 for i in half}
halfwidth = {i - 0x20+0xff00: i for i in half}

def is_exclude(code, exclude_patterns):
    if not exclude_patterns: return False
    for i in exclude_patterns:
        if i.fullmatch(code):
            return True
    return False

def parse_columns(line, columns):
    if line and not line.startswith("#"):
        fs = line.split("#")[0].split("\t")
    else:
        return None, None, None, None
    values = []
    for c in ["text", "code", "weight", "stem"]:
        if c in columns:
            i = columns.index(c)
            if len(fs) > i:
                values.append(fs[i])
            else:
                values.append(None)
        else:
            values.append(None)
    return values

def get_formula_index(abc):
    if "A" <=abc < "U":
        return ord(abc) - ord("A")
    if "U" <=abc <= "Z":
        return ord(abc) - ord("Z") - 1
    if "a" <=abc < "u":
        return ord(abc) - ord("a")
    if "u" <=abc <= "z":
        return ord(abc) - ord("z") - 1

def encoder_by_rules(pys, rules):
    if not rules:
        return " ".join(pys)
    l = len(pys)
    for d in rules:
        if "length_equal" in d  and l == d["length_equal"] \
            or ("length_in_range" in d and d["length_in_range"][0] <= l <=d["length_in_range"][1]):
            f = d["formula"]
            py = ""
            for i in range(0, len(f), 2):
                a, b = get_formula_index(f[i]), get_formula_index(f[i + 1])
                if b >= len(pys[a]): b = -1
                py += pys[a][b]
            return py
    return ""

def get_pyabcz(code):
    a = code.split(" ", 3)
    for i in range(4 -len(a)): a.append("")
    return a

def parse_dict(fs):
    hz = []
    hzs = set()
    zd = collections.defaultdict(list)
    mbStart = "..."
    isMB = False
    y = ""
    phrase = set()

    for line in open(fn, encoding="U8"):
        if not isMB:
            y += line
        line = line.strip()
        if line.startswith(mbStart):
            isMB = True
            yy=yaml.load(y.replace("\t", " "))
            if yy.get("use_preset_vocabulary"):
                d = essay_d.copy()
                phrase = set(filter(lambda x:1<len(x)<=yy.get("max_phrase_length", 6) and d[x]>=yy.get("min_phrase_weight", 0), d.keys()))
            else:
                d = collections.defaultdict(int)
            table = yy["name"]
            columns = yy.get("columns", ["text", "code", "weight"])
            encoder = yy.get("encoder")
            exclude_patterns = None
            rules = None
            if encoder:
                if "exclude_patterns" in encoder:
                    exclude_patterns = list(map(re.compile, encoder["exclude_patterns"]))
                if "rules" in encoder:
                    rules = encoder["rules"]
            continue
        if isMB:
            text, code, weight, stem = parse_columns(line, columns)
            if code:
                code = code.translate(fullwidth)
                if (text,code) not in hzs:
                    hzs.add((text,code))
                    hz.append([text] + get_pyabcz(code))
                if len(text) > 1 and text in phrase:
                    phrase.remove(text)
                if not is_exclude(code, exclude_patterns):
                    percent = 100
                    if weight and weight.endswith("%"):
                        try:
                            percent = float(weight[:-1])
                        except:
                            logging.warning("\t!!! %s 詞頻錯誤：%s", table, line)
                    if percent >= 5:
                        zd[text].append(stem if stem else code)
                if weight and not weight.startswith("0") and "%" not in weight:
                    try:
                        d[text] = int(float(weight))
                    except:
                        logging.warning("\t!!! %s 詞頻錯誤：%s", table, line)
            elif text:
                phrase.add(text)
    for p in phrase:
        pp = list(map(lambda x: zd.get(x, False), p))
        pps = set()
        if all(pp):
            for i in itertools.product(*pp):
                code = encoder_by_rules(i, rules)
                if code and (text,code) not in hzs:
                    hzs.add((p ,code))
                    hz.append([p] + get_pyabcz(code))

    if yy.get("sort", "original") == "by_weight":
        hz.sort(key=lambda x: d[x[0]] if d[x[0]] > 0 else 1000, reverse = True)

    cursor.execute('INSERT INTO dictionary(name, phrase_gap, full) VALUES(?, ?, ?)', [table, bool(phrase) and rules == None, yaml.dump(yy)])

    logging.info("\t%s 詞條数 %d", table, len(hz))
    return table, hz

def get_prism(dictionary, algebra):
    values = []
    px = []
    if algebra:
        xform = []
        sep = re.compile("\W")
        for i in algebra:
            j = sep.search(i).group(0)
            i = i.split(j, 3)
            if i[0] != 'xlit':
                i[1] = re.sub("(?<=\()([^\)]*\)\?)", "|\\1", i[1])
                i[1] = re.compile(i[1])
                if i[2]:
                    i[2] = re.sub("\$(\d)", r"\\\1", i[2])
            xform.append(i[:3])
        pya = set()
        pyd = collections.defaultdict(set)
        for i in cursor.execute('SELECT DISTINCT pya || " " || pyb || " " || pyc || " " || pyz from "%s"' % dictionary):
            for j in i[0].split(" "):
                if j:
                    pya.add(j.translate(halfwidth))
        for py in sorted(pya):
            pys = set((py,))
            try:
                for r, a, b in xform:
                    for i in sorted(pys):
                        n = ''
                        if r == 'erase' and a.fullmatch(i):
                            pys.remove(i)
                            break
                        elif r == 'abbrev' and a.search(i):
                            n = a.sub(b, i)
                            pys.add(n)
                        elif r == 'derive' and a.search(i):
                            n = a.sub(b, i)
                            pys.add(n)
                        elif r == 'xform' and a.search(i):
                            pys.remove(i)
                            n = a.sub(b, i)
                            pys.add(n)
                        elif r == 'xlit':
                            n = i.translate(str.maketrans(a, b))
                            if n != i:
                                pys.remove(i)
                                pys.add(n)
            except:
                logging.error("%s/%s/%s/出錯：%s->%s", r, a, b, i, n)
                raise
            for i in pys:
                pyd[i].add(py)
        px = sorted(pyd)
        for i in px:
            py = pyd[i]
            #if len(py) > 4: py = [i + "*"]
            values.append([i.translate(fullwidth), (" ".join(sorted(py))).translate(fullwidth)])
    return " ".join(px).translate(fullwidth), values

if len(sys.argv) == 1:
    print("請指定方案集schema.yaml文件！")
    exit(0)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

conn = open_db()
cursor = conn.cursor()

schemas = get_schemas()
dicts=set()
algebras=dict()

opencc_dir = "OpenCC/data/dictionary/"
if os.path.exists(opencc_dir):
    logging.info("簡繁")
    cursor.execute("CREATE VIRTUAL TABLE opencc USING fts3(s, t, r)")
    cursor.executemany('INSERT INTO opencc VALUES (?, ?, ?)', opencc(opencc_dir))

logging.info("方案")
cursor.execute('CREATE VIRTUAL TABLE schema USING fts3(_id INTEGER PRIMARY KEY, schema_id, name, full, px)')
cursor.executemany('INSERT INTO schema(_id, schema_id, name, full) VALUES (?, ?, ?, ?)', parse_schemas(schemas))

logging.info("詞庫")
essay_d = get_essaydict()

logging.info("字典")
cursor.execute('CREATE TABLE dictionary (_id INTEGER PRIMARY KEY AUTOINCREMENT, name, phrase_gap INTEGER, full)')
tables = set()
for fn in dicts:
    table, hz = parse_dict(fn)
    if table not in tables:
        tables.add(table)
        cursor.execute('CREATE VIRTUAL TABLE "%s" USING fts3(hz, pya, pyb, pyc, pyz)' % table)
        cursor.executemany('INSERT INTO "%s" VALUES(?, ?, ?, ?, ?)'%(table), hz)

logging.info("棱鏡")
for i in algebras.keys():
    table = "%s.prism" % i
    logging.info("\t%s", table)
    px, values = get_prism(*algebras[i])
    if values:
        cursor.execute('CREATE VIRTUAL TABLE "%s" USING fts3(px, py)' % table)
        cursor.executemany('INSERT INTO "%s" VALUES(?, ?)'%(table), values)
        cursor.execute('UPDATE schema SET px = "%s" WHERE schema_id = "%s"' % (px , i))

close_db(conn)
logging.info("碼表")
