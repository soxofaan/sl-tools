#!/usr/bin/env python

'''
Shuffle the lines from standard input.
'''

import sys
import random
import optparse

if __name__ == '__main__':
    # Build option parser.
    optparser = optparse.OptionParser(
        usage="usage: %prog [options]",
        description='Shuffle the lines from standard input.'
    )

    # Get options.
    (options, arguments) = optparser.parse_args()

    # Get the lines.
    lines = sys.stdin.readlines()

    #TODO: last line could lack a newline, which forks things up.

    # Shuffle the nuffle.
    random.shuffle(lines)

    print(''.join(lines))

