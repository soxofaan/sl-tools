#!/usr/bin/env python

import sys


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
                self._char2pos[char] = (r,c)
                self._pos2char[(r,c)] = char

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
        
    def search_shift_couples(self, words, shifts=[(0,-2), (0,-1), (0,1), (0,2)], verbosity=True):
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
    for line in f:
        if len(line) == word_length + 1:
            words.append(line.strip().lower())
    f.close()
    return words


            

if __name__ == '__main__':

    try:
        word_length = int(sys.argv[1])
    except:
        word_length = 5

    words = get_words('/usr/share/dict/words', word_length)
    keyboard = Keyboard(layout='querty')
    shifts=[(0,-2), (0,-1), (0,1), (0,2)]
    
    keyboard.search_shift_couples(words, shifts=shifts, verbosity=True)

