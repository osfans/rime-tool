#!/usr/bin/env python3
"從Unihan提取異體字"

from collections import defaultdict

def hex2chr(uni):
    "把unicode轉換成漢字"
    return chr(int(uni[2:], 16))

def main():
    "主程序"
    dic = defaultdict(set)
    for line in open("Unihan_Variants.txt"):
        line = line.strip()
        if not line:
            continue
        fields = line.split("\t", 2)
        if len(fields) == 3:
            han, var = fields[0], fields[2]
            for uni in var.split(" "):
                uni = uni.split("<")[0]
                dic[hex2chr(han)].add(hex2chr(uni))
    target = open("unihan-variant.txt", "w", encoding="U8")
    for han in sorted(dic.keys()):
        print("%s\t%s" % (han, (" ".join(dic[han])).strip()), file=target)
    target.close()

if __name__ == "__main__":
    main()
