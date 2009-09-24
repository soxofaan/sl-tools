#!/usr/bin/env python
import re

import sys
import optparse


class OutOfKeyboardError(Exception):
    pass

class Keyboard(object):
    '''
    Object that manages a mapping between characters and postions
    and provides a hand shift translation method for words.
    '''
    _layouts = {
        'querty': [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm',
        ],
        'azerty': [
            'azertyuiop',
            'qsdfghjklm',
            'wxcvbn',
        ]
    }

    def __init__(self, layout='querty'):
        '''
        Initialize a Keyboard object with the given layout.
        '''
        # Dicts for character to position mappings
        self._char2pos = {}
        self._pos2char = {}
        for r, row in enumerate(self._layouts[layout]):
            for c, char in enumerate(row):
                self._char2pos[char] = (r, c)
                self._pos2char[(r, c)] = char

    def translate(self, word, shift):
        '''
        Translate a word by the given hand shift.
        
        @param word: the word to translate
        @param shift: a tuple (x, y) with x the horizontal shift and y the 
            vertical shift
        '''
        result = ''
        try:
            for char in word:
                r, c = self._char2pos[char.lower()]
                result += self._pos2char[(r + shift[0], c + shift[1])]
            return result
        except KeyError:
            raise OutOfKeyboardError

    def search_shift_couples(self, words, shifts=[(0, 1), (0, 2)], verbosity=True):
        '''
        Search for word couples that can be translated into each other
        with a simple shift.
        '''
        hits = []

        for word in words:
            if verbosity == True:
                print word, '\r',
            for shift in shifts:
                try:
                    result = self.translate(word, shift)
                except OutOfKeyboardError:
                    continue
                if result in words:
                    hits.append((word, shift, result))
                    if verbosity:
                        print word, shift, result
        return hits



def get_words(dictionary_file, word_length=4):
    '''
    Get words of a given length from a dictionary file.
    '''
    words = []
    f = open(dictionary_file, 'r')
    rep = re.compile('^[a-z]+$')
    for line in f:
        word = line.strip().lower()
        if len(word) == word_length and rep.match(word):
            words.append(word)
    f.close()
    return words




if __name__ == '__main__':

    # Build command line option parser.
    optparser = optparse.OptionParser(
        usage="usage: %prog [options]",
        description='Search for keyboard hand shift word couples.'
    )
    optparser.add_option(
        '-w', '--word-length',
        metavar='W',
        dest="word_length", type='int', default=5,
        help="The word length to use."
    )
    optparser.add_option(
        '-d', '--dictionary',
        metavar='DICTIONARY',
        dest="dictionary_file", default='/usr/share/dict/words',
        help="The dictionary to read words from."
    )
    optparser.add_option(
        '-k', '--layout',
        metavar='LAYOUT',
        dest="keyboard_layout", default='querty',
        help="The keyboard layout to use (options: %s)." % (', '.join(Keyboard._layouts.keys()))
    )
    # Get options.
    (options, arguments) = optparser.parse_args()

    assert len(arguments) == 0

    words = get_words(options.dictionary_file, options.word_length)
    keyboard = Keyboard(layout=options.keyboard_layout)
    shifts = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]

    keyboard.search_shift_couples(words, shifts=shifts, verbosity=True)

