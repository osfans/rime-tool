#!/usr/bin/env python3
#一個統計頻率的程式
#https://github.com/rime/home/issues/18

from collections import defaultdict
f = open("input.txt") #輸入文件
t = open("output.txt", "w") #輸出文件

d = defaultdict(int)
for line in f:
  line = line.strip()
  if line:
    fs = line.split()
    if len(fs) == 2:
      word, freq = fs
      d[word] += int(freq) #累加
l = sorted(d.items(), key = lambda x: x[1], reverse = True) #排序
for word, freq in l:
  print("%s\t%d" % (word, freq), file = t) #輸出

f.close()
t.close()
