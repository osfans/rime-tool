#!/usr/bin/env python3
"去除重複的編碼行"

import sys

if len(sys.argv) == 1:
    print(__doc__)
    print("Usage: %s filename" % sys.argv[0])
    exit(0)

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
    for filename in sys.argv[1:]:
        uniq = set()
        input_f = open_file(filename)
        lines = []
        for line in input_f:
            key = line.rstrip().rsplit("\t", 1)[0] #比較前N-1列
            if (line and line[0] in "#\n ") or (key not in uniq):
                lines.append(line)
                uniq.add(key)
        input_f.close()
        output_f = open(filename, "w", encoding=ENC)
        output_f.writelines(lines)
        output_f.close()

if __name__ == "__main__":
    main()
