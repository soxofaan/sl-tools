#!/usr/bin/env python

import sys

qwerty_layout = [
    'qwertyuiop',
    'asdfghjkl',
    'zxcvbnm',
    ]

class OutOfKeyboardError(Exception):
    pass

class Keyboard(object):
    def __init__(self, layout=qwerty_layout):
        # Dicts for character to position mappings
        self._char2pos = {}
        self._pos2char = {}
        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                self._char2pos[char] = (r,c)
                self._pos2char[(r,c)] = char

        print self._char2pos
        print self._pos2char

    def translate(self, word, shift):
        result = ''
        try:
            for char in word:
                r, c = self._char2pos[char.lower()]
                result += self._pos2char[(r + shift[0], c + shift[1])]
            return result
        except KeyError:
            raise OutOfKeyboardError


def get_words(word_length=4):
    words = []
    dict = open('/usr/share/dict/words', 'r')
    for line in dict:
        if len(line) == word_length + 1:
            words.append(line.strip().lower())
    dict.close()
    return words


if __name__ == '__main__':

    k = Keyboard()

    #print 'set ->', k.translate('set', (0,1))
    #print 'set ->', k.translate('set', (-1,-1))

    try:
        word_length = int(sys.argv[1])
    except:
        word_length = 5

    words = get_words(word_length)
    # print words

    hits = []

    #shifts = [ (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
    shifts = [ (0,-3), (0,-2), (0,-1), (0,1), (0,2), (0,3)]
    for word in words:
        print word, '\r',
        for shift in shifts:
            try:
                result = k.translate(word, shift)
            except OutOfKeyboardError:
                continue
            if result in words:
                hits.append((word, shift, result))
                print word, shift, result

