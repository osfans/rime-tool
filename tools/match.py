#!/usr/bin/env python3
"""一個篩選過濾的程式
輸入input.txt，條件match.txt，輸出output.txt
https://github.com/osfans/rime-tool/issues/4
"""

INPUT_NAME = "input.txt" #輸入input.txt
MATCH_NAME = "match.txt" #條件match.txt
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

def load_match():
    "讀取條件集合"
    match_file = open_file(MATCH_NAME)
    if match_file:
        match_set = set(line.strip() for line in match_file)
        match_file.close()
        return match_set

def main():
    "讀取文件並篩選"
    input_file = open_file(INPUT_NAME)
    if input_file:
        match_set = load_match()
        lines = [line for line in input_file if line.strip().rsplit("\t", 1)[0] in match_set]
        if lines:
            open(OUTPUT_NAME, "w", encoding=ENC).writelines(lines)

if __name__ == "__main__":
    main()
