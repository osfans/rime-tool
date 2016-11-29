#!/usr/bin/env python3
"中華大辭典(https://github.com/g0v/moedict-data-csld)處理工具：從中獲取繁體拼音數據，供opencc使用"

import fileinput
import re
from collections import OrderedDict

ZHUYIN = "ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦˊˇˋ˙"
PINYIN = "bpmfdtnlgkhjqxZCSrzcsiuvaoeEAIOUMNKGR2345"
TRANS = str.maketrans(ZHUYIN, PINYIN)

def zy2py(zhuyin):
    "將注音轉換爲拼音"
    erhua = zhuyin.endswith('ㄦ')
    zhuyin = re.sub("ㄦ$", "", zhuyin)\
        .replace("〡", "ㄧ").replace("｜", "ㄧ").replace("丨", "ㄧ")\
        .replace("·", "˙").replace("‧", "˙")

    zhuyin = zhuyin.translate(TRANS)
    zhuyin = re.sub(r"^(.*)(\d)(.*)$", r"\1\3\2", zhuyin)
    zhuyin = re.sub(r"(\D)$", r"\g<1>1", zhuyin)
    zhuyin = zhuyin.replace("iE", "ie").replace("vE", "ve").replace("E", "ê") \
        .replace("R", "er") \
        .replace("M", "an").replace("N", "en") \
        .replace("K", "ang").replace("G", "eng") \
        .replace("A", "ai").replace("I", "ei").replace("O", "ao").replace("U", "ou") \
        .replace("Z", "zh").replace("C", "ch").replace("S", "sh") \
        .replace("ien", "in").replace("uen", "un").replace("ven", "vn").replace("ung", "ong") \
        .replace("uei", "ui").replace("iou", "iu")

    zhuyin = re.sub(r"^([zcs]h?|r)(\d)$", r"\1i\2", zhuyin)
    zhuyin = re.sub("^iu", "you", zhuyin)
    zhuyin = re.sub("^ui", "wei", zhuyin)
    zhuyin = re.sub("^un", "wen", zhuyin)
    zhuyin = re.sub(r"^i([n\d])", r"yi\1", zhuyin)
    zhuyin = re.sub(r"^i(\D)", r"y\1", zhuyin)
    zhuyin = re.sub(r"^u(\d)", r"wu\1", zhuyin)
    zhuyin = re.sub(r"^u(\D)", r"w\1", zhuyin)
    zhuyin = re.sub("^v", "yu", zhuyin)
    zhuyin = re.sub("^ong", "weng", zhuyin)
    zhuyin = re.sub("^yung", "yong", zhuyin)
    zhuyin = re.sub("([jqx])vng", r"\1iong", zhuyin)
    zhuyin = re.sub("([jqx])v", r"\1u", zhuyin)
    zhuyin = re.sub("([aeiou])(ng?|r)([1234])", r"\1\3\2", zhuyin)
    zhuyin = re.sub("([aeo])([iuo])([1234])", r"\1\3\2", zhuyin)
    zhuyin = zhuyin.replace("5", "")
    tones = """    - xform a1 ā
    - xform a2 á
    - xform a3 ǎ
    - xform a4 à
    - xform e1 ē
    - xform e2 é
    - xform e3 ě
    - xform e4 è
    - xform o1 ō
    - xform o2 ó
    - xform o3 ǒ
    - xform o4 ò
    - xform i1 ī
    - xform i2 í
    - xform i3 ǐ
    - xform i4 ì
    - xform u1 ū
    - xform u2 ú
    - xform u3 ǔ
    - xform u4 ù
    - xform v1 ǖ
    - xform v2 ǘ
    - xform v3 ǚ
    - xform v4 ǜ
    - xform v ü
    - xform ê4 ề""".split("\n")
    for line in tones:
        fields = line.split(" ")
        zhuyin = zhuyin.replace(fields[6], fields[7])
    if erhua:
        zhuyin += "r"
    return zhuyin

def main():
    "主程序"
    word_pinyin_dict = OrderedDict()
    for line in fileinput.input():
        fields = re.sub('".*?"', "", line).split(",")
        if len(fields) == 44:
            zhuyin = fields[12] if fields[12] else fields[10]
            pinyin = "'".join(map(zy2py, re.split("[ 　，‵′]", zhuyin)))
            word = fields[5]
            if word not in word_pinyin_dict:
                word_pinyin_dict[word] = []
            word_pinyin_dict[word].append(pinyin)

    for word in word_pinyin_dict:
        print("%s\t%s" % (word, " ".join(word_pinyin_dict[word])))

if __name__ == "__main__":
    main()
