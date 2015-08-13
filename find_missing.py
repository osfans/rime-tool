#!/usr/bin/env python3
#
import sys

if len(sys.argv) == 1:
  print("查找詞典中未編碼的字")
  print("Usage: %s schema_file [freq dict_file]" % sys.argv[0])
  exit(0)

else:
  filename = sys.argv[1]
  freq = 1000
  dict_file = "brise/essay.txt"
  if len(sys.argv) > 2:
    freq = int(sys.argv[2])
  elif len(sys.argv) == 4:
    dict_file = sys.argv[3]

a=set()
for line in open(dict_file):
  fs=line.strip().split()
  if len(fs) == 2:
    w, f = fs
    if int(f) >= freq:
      for i in w: a.add(i)

b=set()
for line in open(filename):
  if "\t" in line:
    fs = line.split("\t")
    for i in fs[0]: b.add(i)

for i in sorted(a - b):
  print(i)
