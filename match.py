#!/usr/bin/env python3
#一個篩選過濾的程式
#輸入input.txt，條件match.txt，輸出output.txt
#https://github.com/osfans/rime-tool/issues/4

input_file = "input.txt" #輸入input.txt
match_file = "match.txt" #條件match.txt
output_file = "output.txt" #輸出output.txt

enc = ""
s = set() #條件集合
d = list() #輸出結果列表
encodings = ["utf-8-sig", "utf-16", "gbk", "gb18030"] #嘗試編碼列表

def load_match(encoding):
  try:
    global s, enc
    s = set(line.strip() for line in open(match_file, encoding=encoding)) 
    enc = encoding
    return True
  except:
    return False

def load_input(encoding):
  try:
    global d, s, enc
    d = [line for line in open(input_file, encoding=encoding) if line.strip().rsplit("\t", 1)[0] in s]
    enc = encoding
    return True
  except:
    return False

any(map(load_match, encodings))
any(map(load_input, encodings))
print("file encoding:", enc)
open(output_file, "w", encoding = enc).writelines(d)
