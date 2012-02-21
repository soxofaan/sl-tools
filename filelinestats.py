#!/usr/bin/env python

'''
Collect text file size stats, like number of lines, average line length,
maximum line length, number of whitespace lines, ...
'''

# TODO: add walking through directories (or ignoring directories)
# TODO: detect and ignore binary files
# TODO: add option to sort (e.g. on max length)

import sys


def get_lines(filename):
    '''
    Get the lines of a text file (newlines will be stripped).

    @return list of the file's lines
    '''
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines


def collect_file_size_stats(filename):
    '''
    Collect file size stats.
    '''
    lines = get_lines(filename)
    line_lengths = [len(l) for l in lines]
    max_length = max(line_lengths)
    average_length = float(sum(line_lengths)) / len(lines)
    empty_line_fraction = float(len([l for l in lines if l.strip() == ''])) / len(lines)

    return max_length, average_length, empty_line_fraction


def main():

    filenames = sys.argv[1:]

    for filename in filenames:
        max_length, average_length, empty_line_fraction = collect_file_size_stats(filename)

        print 'avglen: {avg:5.1f}; maxlen: {max:5d}; empty: {empty:5.2f}%; {filename}: '.format(
            filename=filename,
            avg=average_length,
            max=max_length,
            empty=100 * empty_line_fraction
            )


if __name__ == '__main__':
    main()
