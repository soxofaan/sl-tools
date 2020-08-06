#!/usr/bin/env python

'''
Pick a random subset from the standard input lines.
'''

import sys
import random
import optparse

if __name__ == '__main__':
    # Build option parser.
    optparser = optparse.OptionParser(
        usage="usage: %prog [options]",
        description='Pick a random subset from the standard input lines.'
    )
    optparser.add_option(
        "-n",
        dest="number", default='10', type="int",
        help="The number of lines to pick")

    # Get options.
    (options, arguments) = optparser.parse_args()

    # Get the lines.
    lines = sys.stdin.readlines()

    # Extract a random subset.
    subset = random.sample(lines, options.number)

    print(''.join(subset))

