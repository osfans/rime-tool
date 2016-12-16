#!/usr/bin/env python3

import re

d = dict()
for line in open("Unihan_IRGSources.txt"):
  line = line.strip()
  if not line:
    continue
  fields = line.split("\t", 2)
  if len(fields) == 3:
    z,s,y=fields
    z = chr(int(z[2:],16))
    if s == "kRSUnicode":
      print(z)
