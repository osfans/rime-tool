#!/usr/bin/env python3
"去除PUA行"

import fileinput

def is_pua(char):
    """判斷是否爲pua字符"""
    num = ord(char)
    if 0xE000 <= num <= 0xF8FF or 0xF0000 <= num <= 0xFFFFD or 0x100000 <= num <= 0x10FFFD:
        return True
    return False

for line in fileinput.input():
    line = line.rstrip()
    if any(map(is_pua, line)):
        continue
    print(line)
