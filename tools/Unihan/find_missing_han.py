#!/usr/bin/env python3
"查找詞典中未編碼的 unicode9.0 漢字"
import fileinput

OUTPUT = "output.txt"

def get_words(files):
    "獲取漢字表"
    hans = set()
    for line in files:
        line = line.strip()
        if line:
            word = line.split("\t")[0]
            hans.add(word)
    return hans

def main():
    "主函數"
    hans = get_words(open("unichr.txt"))
    words = get_words(fileinput.input())
    target = open(OUTPUT, "w")
    for word in sorted(hans - words):
        print(word, file=target)
    target.close()

if __name__ == "__main__":
    main()
