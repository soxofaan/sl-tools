#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess

def split(path):
    """
    Split a path in its components and return it as a list.
    """
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

def parent(a, b):
    """
    Is a parent of b?
    """
    if len(a)>=len(b):
        return False
    for (x,y) in zip(a,b):
        if x!= y:
            return False
    return True


def find_directories(root='.', needle='.svn'):
    '''
    Search in root for files or folders with the name needle.
    '''
    p = subprocess.Popen(['find', root, '-name', needle], stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    # Split in lines
    dirs = stdout.split('\n')
    # Split in path components
    dirs = [split(dir.strip()) for dir in dirs]
    # Make sure needle is a component.
    dirs = [l for l in dirs if needle in l]
    # Sort (so that shorter paths come first)
    dirs.sort()
    return dirs


def main():
    needle = '.svn'
    dirs = find_directories('.', needle)

    roots = []

    for l in dirs:
        i = l.index(needle)
        candidate = l[:i]
        # Check if the candidate already has a parent. 
        for root in roots:
            if root == candidate or parent(root, candidate):
                break
        else:
            roots.append(candidate)

    for root in roots:
        print os.path.join(*root)


if __name__ == '__main__':
    main()
