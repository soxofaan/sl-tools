#!/usr/bin/env python

import os
import re

def split(path):
    """return a path splitted in a list of path components."""
    l = []
    while True:
        path, tail = os.path.split(path)
        l.insert(0, tail)
        if path == '/':
            l.insert(0,'/')
            break
        if path == '':
            break
    return l

def parent(a,b):
    """ is a parent of b?"""
    if len(a)>=len(b):
        return False
    for (x,y) in zip(a,b):
        if x!= y:
            return False
    return True


locatepipe = os.popen('locate .svn', 'r')
dirs = locatepipe.readlines()
locatepipe.close()

roots = []

dirs = [split(dir.strip()) for dir in dirs]
dirs = [l for l in dirs if '.svn' in l]

dirs.sort()

for l in dirs:
    i = l.index('.svn')
    candidate = l[:i]
    for root in roots:
        if root == candidate or parent(root, candidate):
            break
    else:
        roots.append(candidate)


for root in roots:
    print os.path.join(*root)
