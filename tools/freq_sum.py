#!/usr/bin/env python3
"""一個統計頻率的程式
https://github.com/rime/home/issues/18
"""

from collections import defaultdict

ENC = "utf-8"
ENCODINGS = ["utf-8-sig", "utf-16", "gbk", "gb18030"]
INPUT_NAME = "input.txt"
OUTPUT_NAME = "output.txt"

def write_dic(dic):
    "保存文件"
    lists = sorted(dic.items(), key=lambda x: x[1], reverse=True) #排序
    target_file = open(OUTPUT_NAME, "w", encoding=ENC) #輸出文件
    for word, freq in lists:
        print("%s\t%d" % (word, freq), file=target_file) #輸出
    target_file.close()

def try_enc(enc):
    "嘗試指定編碼"
    try:
        dic = defaultdict(int)
        input_file = open(INPUT_NAME, encoding=enc) #輸入文件
        for line in input_file:
            line = line.strip()
            if line:
                fields = line.rsplit("\t", 1)
                if len(fields) == 2 and fields[1].isdigit():#詞\t音\t頻 或 詞\t頻
                    word, freq = fields
                else:
                    word, freq = line, 1 #詞\t音 或 詞，默認詞頻爲1
                dic[word] += int(freq) #累加
        input_file.close()
        write_dic(dic)
        return True
    except UnicodeError:
        return False

def main():
    "嘗試編碼列表"
    for enc in ENCODINGS:
        if try_enc(enc):
            break

if __name__ == "__main__":
    main()
