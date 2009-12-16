'''
Created on Dec 16, 2009

@author: slippens

Observe data from the standard input (words, lines, numerical data)
and build a histogram from it
'''
import optparse
import sys


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

    def ordered_items(self):
        '''
        Return an ordered list of histogram items
        (from highest count to lowest count).
        '''
        items = self.items()
        items.sort(lambda a, b:-cmp(a[1], b[1]))
        return items

    def ascii_plot(self, sorted=True, limit=None, out=sys.stdout):
        '''
        Make a plot in text (ASCII) format.
        '''
        if sorted:
            items = self.ordered_items()
        else:
            items = self.iteritems()
        max_count = max(self.values())
        total_count = sum(self.values())
        for obj, count in items[:limit]:
            bar = '#' * int(20.0 * count / max_count)
            out.write('%20s %5d (%5.2f%%) %s\n' % (bar, count, 100.0 * count / total_count, str(obj)))



if __name__ == '__main__':

    optparser = optparse.OptionParser(
        usage="usage: %s [options] [files]",
        description='Observe data and build a histogram.')

    # Get options.
    (options, arguments) = optparser.parse_args()

    histogram = ObjectHistogram()

    if len(arguments) == 0:
        histogram.observe_words_from_file(sys.stdin)
    else:
        for file_name in arguments:
            f = open(file_name)
            histogram.observe_words_from_file(f)
            f.close()

    histogram.ascii_plot(limit=20)



