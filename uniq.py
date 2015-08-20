#!/usr/bin/env python3
"去除重複的編碼行"

import sys

if len(sys.argv) == 1:
    print("Usage: %s filename" % sys.argv[0])
    exit(0)

for fn in sys.argv[1:]:
    s = ""
    uniq = set()
    f = open(fn, "r")
    for line in f:
        if (line and line[0] in "#\n ") or (line not in uniq):
            s += line
            uniq.add(line)
    f.close()
    t = open(fn, "w")
    t.write(s)
    t.close()
