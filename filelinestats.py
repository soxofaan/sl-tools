#!/usr/bin/env python

'''
Collect text file size stats, like number of lines, average line length,
maximum line length, number of whitespace lines, ...
'''

# TODO: detect and ignore binary files
# TODO: add option to sort (e.g. on max length)

import os
import optparse


def get_lines(filename):
    '''
    Get the lines of a text file (newlines will be stripped).

    @return list of the file's lines
    '''
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines


class FileSizeStat(object):
    '''
    Simple container for file size stats of a file.
    '''

    filename = None
    max_length = None
    average_length = None
    empty_line_fraction = None

    def __init__(self, filename=None):
        '''
        Collect file size stats.
        '''
        self.filename = filename

        lines = get_lines(self.filename)
        line_lengths = [len(l) for l in lines]
        if len(line_lengths) > 0:
            self.max_length = max(line_lengths)
            self.average_length = float(sum(line_lengths)) / len(lines)
            self.empty_line_fraction = float(len([l for l in lines if l.strip() == ''])) / len(lines)

    def render(self):
        cols = []
        if self.average_length != None:
            cols.append('avglen: {avg:5.1f}'.format(avg=self.average_length))
        else:
            cols.append('avglen:   nan')
        if self.max_length != None:
            cols.append('maxlen: {max:5d}'.format(max=self.max_length))
        else:
            cols.append('maxlen:   nan')
        if self.empty_line_fraction != None:
            cols.append('empty: {empty:5.2f}%'.format(empty=self.empty_line_fraction))
        else:
            cols.append('empty:    nan')

        cols.append(self.filename)

        return '; '.join(cols)


def main():

    cli_parser = optparse.OptionParser(usage='%prog [options] paths')
    cli_parser.add_option(
        '-r', '--recursive',
        dest='recursive', action='store_true', default=False,
        help='Recurse through given directories and process all files, instead of ignoring directories.'
        )

    (options, paths) = cli_parser.parse_args()

    for path in paths:

        if os.path.isfile(path):
            # Collect and render stats for single file
            fss = FileSizeStat(path)
            print fss.render()
        elif os.path.isdir(path) and options.recursive:
            # Recurse through directory.
            for (dirpath, dirnames, filenames) in os.walk(path):
                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    fss = FileSizeStat(path)
                    print fss.render()


if __name__ == '__main__':
    main()
