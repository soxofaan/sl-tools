#!/usr/bin/env python

import sys
import random
import optparse

if __name__ == '__main__':
    # Build command line parser.
    optparser = optparse.OptionParser(
        usage="usage: %prog inputfile outputfile1 outputfile2 outputfile3 ...",
        description='Split the lines from a input file randomly over the given output files.'
    )
    optparser.add_option(
        '-s', '--seed',
        dest='seed', default=None,
        help='The seed of the random generator.')

    # Get options from command line.
    (options, arguments) = optparser.parse_args()

    # Check arguments.
    if len(arguments) < 3:
        optparser.error('At least 3 file names should be given')

    # Seed random generator if required.
    if options.seed != None:
        random.seed(int(options.seed))

    # Open input and output files
    input_file = file(arguments[0], 'r')
    output_files = [file(f, 'w') for f in arguments[1:]]

    # Write lines from input to output files randomly.
    for line in input_file:
        random.choice(output_files).write(line)

    # close the files.
    input_file.close()
    for f in output_files:
        f.close()
