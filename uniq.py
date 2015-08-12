#!/usr/bin/env python3
import sys

if len(sys.argv) == 1:
  print("Usage: %s filename" % sys.argv[0])
  exit

for fn in sys.argv[1:]:
  s = ""
  uniq=set()
  f = open(fn, "r")
  for line in f:
    if line.startswith("#") or line.startswith("\n") or line.startswith(" ") or (line not in uniq):
      s+=line
      uniq.add(line)
  f.close()
  t = open(fn, "w")
  t.write(s)
  t.close()
