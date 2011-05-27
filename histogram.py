#!/usr/bin/env python

'''
Created on Dec 16, 2009

@author: Stefaan Lippens

Observe data from the standard input (words, lines, numerical data)
and build a histogram from it
'''

import optparse
import sys
import operator


class ObjectHistogram(dict):
    '''
    Basic histogram builder for observing general objects.
    '''

    def __init__(self):
        dict.__init__(self)

    def observe(self, x):
        '''
        Add an observation to the histogram.
        '''
        self[x] = self.get(x, 0) + 1

    def observe_lines_from_file(self, source):
        '''
        Observe the lines from a file-like source.
        '''
        for line in source:
            self.observe(line)

    def observe_words_from_file(self, source):
        '''
        Observe the words from a file-like source.
        '''
        for line in source:
            for word in line.split():
                self.observe(word)

    def observe_from_sources(self, sources, observe_lines=False):
        '''
        Observe data from a list of sources.

        @param sources a list of sources: file-like objects
            or a file name string.
        @param observe_lines whether or not lines (instead of
            words) should be observed.
        '''
        for source in sources:
            if isinstance(source, str):
                f = open(source, 'r')
            else:
                f = source
            if observe_lines:
                self.observe_lines_from_file(f)
            else:
                self.observe_words_from_file(f)
            if isinstance(source, str):
                f.close()


    def ordered_items(self):
        '''
        Return an ordered list of histogram items
        (from highest count to lowest count).
        '''
        items = self.items()
        items.sort(lambda a, b:-cmp(a[1], b[1]))
        return items

    def ascii_plot(self, keysort=False, limit=None, out=sys.stdout):
        '''
        Make a plot in text (ASCII) format.
        '''
        if keysort:
            items = sorted(self.items(), key=operator.itemgetter(0), reverse=False)
        else:
            items = sorted(self.items(), key=operator.itemgetter(1), reverse=True)
        max_count = max(self.values())
        total_count = sum(self.values())
        for obj, count in items[:limit]:
            bar = '#' * int(20.0 * count / max_count)
            label = str(obj).rstrip()
            out.write('%20s %5d (%5.2f%%) %s\n' % (bar, count, 100.0 * count / total_count, label))



if __name__ == '__main__':

    optparser = optparse.OptionParser(
        usage="usage: %s [options] [files]",
        description='Observe data and build a histogram.')

    optparser.add_option(
        '-L', '--lines',
        dest='observe_lines', action='store_true', default=False,
        help='Observe lines instead of words.',
    )
    optparser.add_option(
        '-n', '--limit', metavar='N',
        dest='limit', type='int', action='store', default=None,
        help='Limit the histogram to a number of entries.',
    )
    optparser.add_option(
        '-k', '--keysort',
        dest='keysort', action='store_true', default=False,
        help='Sort the entries on their key, instead of frequency.',
    )

    # Get options.
    (options, arguments) = optparser.parse_args()

    histogram = ObjectHistogram()

    if len(arguments) == 0:
        arguments = [sys.stdin]

    histogram.observe_from_sources(arguments, observe_lines=options.observe_lines)

    histogram.ascii_plot(limit=options.limit, keysort=options.keysort)



