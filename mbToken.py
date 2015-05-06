#!/usr/bin/env python3

import sqlite3
import sys
sys.path.append('sqlite-fts-python')

import sqlitefts as fts

class Tokenizer(fts.Tokenizer):
    def tokenize(self, text):
        pos = 0
        for t in text.split(' '):
            byteLen = len(t.encode('utf-8'))
            yield t, pos, pos + byteLen
            pos += byteLen + 1

def reg(conn):
    fts.register_tokenizer(conn, 'mb', fts.make_tokenizer_module(Tokenizer()))
