#!/usr/bin/env python

"""
Prettify (indent) JSON data.

Run modes:

    # Read from input file and write to output file
    json-prettify.py input.json output.json

    # Read from input file and write to standard output
    json-prettify.py input.json

    # Read from standard input and write to standard output
    json-prettify

"""

import sys
import json
import collections
import io


def json_prettify(input_src=sys.stdin, output_sink=sys.stdout):
    """
    Read JSON data from file like input_src
    and write prettified/indented JSON to file like output_sink
    """

    if isinstance(input_src, str):
        input_src = open(input_src, 'r')

    # Load JSON data (and preserve key order).
    data = json.load(input_src, object_pairs_hook=collections.OrderedDict)

    # Write prettified JSON.
    if isinstance(output_sink, str):
        output_sink = open(output_sink, 'w')

    json.dump(data, output_sink, indent=4)


def test_json_prettify():
    input_src = io.StringIO('{"x":123,"y":{"a":2,"b":4}}')
    output_sink = io.StringIO()

    json_prettify(input_src, output_sink)

    result = output_sink.getvalue()
    expected = '\n'.join([
        '{',
        '    "x": 123, ',
        '    "y": {',
        '        "a": 2, ',
        '        "b": 4',
        '    }',
        '}'
    ])
    assert expected == result, repr((expected, result))

if __name__ == '__main__':
    json_prettify(*sys.argv[1:])

