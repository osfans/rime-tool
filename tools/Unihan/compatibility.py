#!/usr/bin/env python3
"从Unihan中找到兼容字和對應的標準字"

def hex2chr(uni):
    "把unicode轉換成漢字"
    return chr(int(uni[2:], 16))

def main():
    "主程序"
    target = open("unihan-compatibility.txt", "w", encoding="U8")
    for line in open("Unihan_IRGSources.txt"):
        line = line.strip()
        if not line:
            continue
        fields = line.split("\t", 2)
        if len(fields) == 3:
            uni, typ, var = fields
            if typ == "kCompatibilityVariant":
                print("%s\t%s" % (hex2chr(uni), hex2chr(var)), file=target)
    target.close()

if __name__ == "__main__":
    main()
