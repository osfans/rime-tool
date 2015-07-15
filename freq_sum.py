#!/usr/bin/env python3
#一個統計頻率的程式
#https://github.com/rime/home/issues/18

from collections import defaultdict

d = defaultdict(int)
enc = ""

def freq_sum(encoding):
  try:
    d.clear()
    f = open("input.txt", encoding=encoding) #輸入文件
    for line in f:
      line = line.strip()
      if line:
        fs = line.rsplit("\t", 1)
        if len(fs) == 2 and fs[1].isdigit():#詞\t音\t頻 或 詞\t頻
          word, freq = fs
        else:
          word, freq = line, 1 ##詞\t音 或 詞，默認詞頻爲1
        d[word] += int(freq) #累加
    f.close()
    global enc
    enc = encoding
    return True
  except:
    return False

any(map(freq_sum, ["utf-8-sig", "utf-16", "gbk", "gb18030"]))
print("file encoding:", enc)
l = sorted(d.items(), key = lambda x: x[1], reverse = True) #排序
t = open("output.txt", "w", encoding = enc) #輸出文件
for word, freq in l:
  print("%s\t%d" % (word, freq), file = t) #輸出

t.close()
