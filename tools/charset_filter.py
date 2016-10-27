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

def is_visible(char):
    "判斷是否爲可顯示字符"
    code_point = ord(char)
    if (
            #(0x3400 <= code_point <= 0x4DBF) or # CJK Unified Ideographs Extension A
            (0x20000 <= code_point <= 0x2A6DF) or # CJK Unified Ideographs Extension B
            (0x2A700 <= code_point <= 0x2B73F) or # CJK Unified Ideographs Extension C
            (0x2B740 <= code_point <= 0x2B81F) or # CJK Unified Ideographs Extension D
            (0x2B820 <= code_point <= 0x2CEAF) or # CJK Unified Ideographs Extension E
            (0x2F800 <= code_point <= 0x2FA1F) # CJK Compatibility Ideographs Supplement
    ):
        return False
    return True

def in_charset(line, charset="visible"):
    "檢查是否屬於charset字符集"
    if charset == "visible":
        return all(map(is_visible, line))
    try:
        line.encode(charset)
        return True
    except UnicodeError:
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
