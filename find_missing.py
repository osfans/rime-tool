#!/usr/bin/env python3
"查找詞典中未編碼的字"
import sys

if len(sys.argv) == 1:
    print(__doc__)
    print("Usage: %s schema_file [freq dict_file]" % sys.argv[0])
    exit(0)

DICT_FILE = "brise/essay.txt"
FREQ = 1000

def get_dict(dict_file, word_freq):
    "獲取詞典字表"
    words = set()
    for line in open(dict_file):
        fields = line.strip().split("\t")
        if len(fields) == 2:
            word, freq = fields
            if int(freq) >= word_freq:
                for char in word:
                    words.add(char)
    return words

def get_words(filename):
    "獲取當前字表"
    words = set()
    for line in open(filename):
        if "\t" in line:
            fields = line.split("\t")
            word = fields[0]
            for char in word:
                words.add(char)
    return words

def main():
    "主函數"
    filename = sys.argv[1]
    word_freq = int(sys.argv[2]) if len(sys.argv) >= 3 else FREQ
    dict_file = sys.argv[3] if len(sys.argv) == 4 else DICT_FILE
    dict_set = get_dict(dict_file, word_freq)
    word_set = get_words(filename)
    for word in sorted(dict_set - word_set):
        print(word)

if __name__ == "__main__":
    main()
