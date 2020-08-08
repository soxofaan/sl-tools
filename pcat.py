#!/usr/bin/python

import sys
import pickle

for fileName in sys.argv[1:]:
    f = open(fileName, "r")
    unpickler = pickle.Unpickler(f)
    while True:
        try:
            obj = unpickler.load()
            print(obj)
        except EOFError:
            f.close()
            break

