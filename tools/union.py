#!/usr/bin/env python3
"合併相同漢字的編碼行，用空格分割"

from collections import OrderedDict

INPUT_NAME = "input.txt" #輸入input.txt
OUTPUT_NAME = "output.txt" #輸出output.txt

ENC = "utf-8"
ENCODINGS = ["utf-8-sig", "utf-16", "gbk", "gb18030"] #嘗試編碼列表

def open_file(filename):
    "嘗試解碼文件"
    for enc in ENCODINGS:
        try:
            input_file = open(filename, encoding=enc)
            return input_file
        except UnicodeError:
            continue

def main():
    "主程序"
    input_file = open_file(INPUT_NAME)
    if input_file:
        uniq = OrderedDict()
        for line in input_file:
            fields = line.strip().split("\t")
            if len(fields) != 2:
                continue
            key, value = fields
            if key not in uniq:
                uniq[key] = [value]
            else:
                uniq[key].append(value)
        input_file.close()
        target = open(OUTPUT_NAME, "w", encoding=ENC)
        for key in uniq:
            target.write("%s\t%s\n" % (key, " ".join(uniq[key])))
        target.close()

if __name__ == "__main__":
    main()
