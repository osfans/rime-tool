#!/usr/bin/env python3
"去除重複的編碼行"

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
        uniq = set()
        lines = []
        for line in input_file:
            key = line.rstrip().rsplit("\t", 1)[0] #比較前N-1列
            if (line and line[0] in "#\n ") or (key not in uniq):
                lines.append(line)
                uniq.add(key)
        input_file.close()
        open(OUTPUT_NAME, "w", encoding=ENC).writelines(lines)

if __name__ == "__main__":
    main()
