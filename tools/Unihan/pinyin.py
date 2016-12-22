#!/usr/bin/env python3
"從Unihan提取讀音"

import re
from collections import defaultdict

def hex2chr(uni):
    "把unicode轉換成漢字"
    return chr(int(uni[2:], 16))

def append(dic, items):
    "添加到字典"
    for each in items:
        if each not in dic:
            dic.append(each)

def main():
    "主程序"
    dic = defaultdict(list)
    for line in open("Unihan_Readings.txt"):
        fields = line.strip().split("\t", 2)
        if len(fields) != 3:
            continue
        han, typ, yin = fields
        han = hex2chr(han)
        if typ == "kMandarin":
            yin = yin.strip()
            append(dic[han], [yin])
        elif typ == "kXHC1983":
            yin = re.sub(r"[.0-9*,]+:", "", yin).split(" ")
            append(dic[han], yin)
        elif typ == "kHanyuPinyin":
            yin = re.sub(r"^.+:", "", yin).split(",")
            append(dic[han], yin)
        elif typ == "kHanyuPinlu":
            yin = re.sub(r"\(.*?\)", "", yin).split(" ")
            append(dic[han], yin)

    target = open("unihan-pinyin.txt", "w", encoding="U8")
    for han in sorted(dic.keys()):
        print("%s\t%s" % (han, (" ".join(dic[han])).strip()), file=target)
    target.close()

if __name__ == "__main__":
    main()
