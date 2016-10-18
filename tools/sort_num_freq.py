#!/usr/bin/env python3
"""先按字數再按詞頻排序
fhx請求
"""

from collections import defaultdict

ENC = "utf-8"
ENCODINGS = ["utf-8-sig", "utf-16", "gbk", "gb18030"]
INPUT_NAME = "input.txt"
OUTPUT_NAME = "output.txt"

def open_file(filename):
    "嘗試解碼文件"
    for enc in ENCODINGS:
        try:
            input_file = open(filename, encoding=enc)
            return input_file
        except UnicodeError:
            continue

def write_dic(dic):
    "保存文件"
    lists = sorted(dic.items(), key=lambda x: (len(x[0].split("\t")[0]), -x[1])) #排序
    target_file = open(OUTPUT_NAME, "w", encoding=ENC) #輸出文件
    for word_code, freq in lists:
        print(word_code + ("" if freq == -1 else "\t" + str(freq)), file=target_file) #輸出
    target_file.close()

def main():
    "主程序"
    input_file = open_file(INPUT_NAME)
    if input_file:
        dic = defaultdict(int)
        for line in input_file:
            line = line.strip()
            if line:
                fields = line.rstrip().split("\t")
                word = ""
                if len(fields) == 3 and fields[2].isdigit():#詞\t音\t頻
                    word, code, freq = fields
                elif len(fields) == 2:
                    word, code = fields
                    freq = -1
                if word:
                    dic[word + "\t" + code] += int(freq) #累加
        input_file.close()
        write_dic(dic)

if __name__ == "__main__":
    main()
