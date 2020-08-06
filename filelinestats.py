#!/usr/bin/env python

"""
Collect text file size stats, like number of lines, average line length,
maximum line length, number of whitespace lines, ...
"""

# TODO: detect and ignore binary files

import os
import sys
import optparse
from operator import attrgetter


def get_lines(filename):
    '''
    Get the lines of a text file (newlines will be stripped).

    @return list of the file's lines
    '''
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines


def median(l):
    '''Calculate median value of a given list.'''
    l = sorted(l)
    n = len(l)
    if n % 2 == 1:
        return l[(n - 1) / 2]
    else:
        return 0.5 * (l[n / 2 - 1] + l[n / 2])


class FileSizeStat(object):
    '''
    Simple container for file size stats of a file.
    '''

    filename = None
    line_qty = None
    non_empty_line_qty = None
    max_length = None
    average_length = None
    median_length = None
    empty_line_fraction = None

    @staticmethod
    def get_sort_fields():
        '''
        Get attribute that can be used to sort stat entries.

        @return list of attribute names
        '''
        return ['line_qty', 'non_empty_line_qty', 'max_length', 'average_length', 'median_length',
                'empty_line_fraction']

    def __init__(self, filename=None):
        '''
        Collect file size stats.
        '''
        self.filename = filename

        lines = get_lines(self.filename)
        self.line_qty = len(lines)
        if self.line_qty > 0:
            self.non_empty_line_qty = len([l for l in lines if l.strip() != ''])
            line_lengths = [len(l) for l in lines]
            self.max_length = max(line_lengths)
            self.average_length = float(sum(line_lengths)) / self.line_qty
            self.median_length = median(line_lengths)
            self.empty_line_fraction = float(self.line_qty - self.non_empty_line_qty) / self.line_qty

    def render(self):
        cols = []

        cols.append('lineqty: {qty:5d}'.format(qty=self.line_qty))
        if self.non_empty_line_qty != None:
            cols.append('nonemptylineqty: {qty:5d}'.format(qty=self.non_empty_line_qty))
        else:
            cols.append('nonemptylineqty: nan')
        if self.average_length != None:
            cols.append('avglen: {avg:5.1f}'.format(avg=self.average_length))
        else:
            cols.append('avglen:   nan')
        if self.median_length != None:
            cols.append('medianlen: {avg:5.1f}'.format(avg=self.median_length))
        else:
            cols.append('medianlen:   nan')
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


def generate_file_paths(paths, recurse):
    '''
    Generator for file paths from a list of file and directory paths
    (which will be scanned recursively if asked for).
    '''
    for path in paths:
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            if recurse:
                for (dirpath, dirnames, filenames) in os.walk(path):
                    for filename in filenames:
                        yield os.path.join(dirpath, filename)
            else:
                pass
        else:
            sys.stderr.write('Warning: ignoring invalid path "%s".\n' % path)


def main():
    possible_sort_fields = FileSizeStat.get_sort_fields()

    cli_parser = optparse.OptionParser(usage='%prog [options] paths')
    cli_parser.add_option(
        '-r', '--recursive',
        dest='recursive', action='store_true', default=False,
        help='Recurse through given directories and process all files, instead of ignoring directories.'
    )
    cli_parser.add_option(
        '-s', '--sort',
        dest='sort_field', action='store', default=None,
        help='Sort field to sort stats on (possible fields: %s).' % (', '.join(possible_sort_fields))
    )

    (options, paths) = cli_parser.parse_args()

    if options.sort_field == None:
        # No sorting: render stats immediately.
        for path in generate_file_paths(paths, options.recursive):
            print(FileSizeStat(path).render())
    elif options.sort_field in possible_sort_fields:
        # Sorting: first collect stats and render after sorting
        stats = [FileSizeStat(path) for path in generate_file_paths(paths, options.recursive)]
        stats.sort(key=attrgetter(options.sort_field))
        for fss in stats:
            print(fss.render())
    else:
        cli_parser.error('Invalid sort field "%s"\n' % options.sort_field)


if __name__ == '__main__':
    main()
