#!/usr/bin/env python

import sys


def bin(v):
    """Convert a number to binary notation."""
    d = {'0': '000', '1': '001', '2': '010', '3': '011', '4': '100', '5': '101', '6': '110', '7': '111', 'L': ''}
    return ''.join([d[x] for x in oct(v).partition('o')[-1]])


def safe_chr(v):
    """Convert to ASCII printable char, or space when out of range."""
    if 32 <= v <= 126:
        return chr(v)
    else:
        return ' '


def ascii(v):
    """Convert to ASCII string"""
    s = ''
    while v:
        s = safe_chr(v % 256) + s
        v = int(v / 256)
    return s


def value_to_row(v):
    return [
        bin(v),
        oct(v),
        str(v),
        hex(v),
        repr(ascii(v)),
    ]


if __name__ == '__main__':
    for arg in sys.argv[1:]:

        # Build a table of rows with numer interpretations.
        rows = []
        rows.append([arg, 'to bin', 'to oct', 'to dec', 'to hex', 'to char'])

        bases = [
            ('bin', 2),
            ('oct', 8),
            ('dec', 10),
            ('hex', 16),
        ]

        for name, base in bases:
            try:
                # Get the value when interpreted for a given base.
                value = int(arg, base=base)
                rows.append(['from %s' % name] + value_to_row(value))
            except ValueError:
                pass

        # Display rows.

        # Calculate column widths.
        colq = len(rows[0])
        widths = [max([len(row[c]) for row in rows]) for c in range(colq)]

        for (r, row) in enumerate(rows):
            if r == 1:
                print('+' + '+'.join(['-' * (w + 2) for w in widths]) + '+')

            print('| ' + ' | '.join(row[c].rjust(widths[c]) for c in range(colq)) + ' |')
