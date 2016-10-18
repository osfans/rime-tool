#!/usr/bin/env python3
"""一個字符集過濾的程式，篩選輸出指定字符集的行
輸入input.txt，輸出output.txt
"""

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

def in_charset(line, charset="gb2312"):
    "檢查是否屬於charset字符集"
    try:
        line.encode(charset)
        return True
    except:
        return False

def main():
    "讀取文件並篩選"
    input_file = open_file(INPUT_NAME)
    if input_file:
        lines = [line for line in input_file if in_charset(line.strip().rsplit("\t", 1)[0])]
        if lines:
            open(OUTPUT_NAME, "w", encoding=ENC).writelines(lines)

if __name__ == "__main__":
    main()
