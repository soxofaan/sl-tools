#!/usr/bin/env python

import itertools
import sys
from typing import List, Iterator


def safe_chr(v: int):
    """Convert to ASCII printable char, or space when out of range."""
    if 32 <= v <= 126:
        return chr(v)
    else:
        return ' '


def ascii(v: int):
    """Convert to ASCII string"""
    # TODO: also do UTF8?
    s = ''
    while v:
        s = safe_chr(v % 256) + s
        v = int(v / 256)
    return s


def value_to_row(v: int):
    return [
        bin(v),
        oct(v),
        str(v),
        hex(v),
        repr(ascii(v)),
    ]


def build_table(arg: str) -> List[List[str]]:
    """Build number interpretation table from given number-like string"""
    rows = [
        [arg, 'to bin', 'to oct', 'to dec', 'to hex', 'to char']
    ]

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
            rows.append(['from {n}'.format(n=name)] + value_to_row(value))
        except ValueError:
            pass

    return rows


def render_row(row: List[str], widths: List[int], sep: str = '|', pad: str = ' ') -> str:
    return sep + sep.join(pad + c.rjust(w) + pad for c, w in zip(row, widths)) + sep


def render_table(rows: List[List[str]]) -> Iterator[str]:
    # Find width of each column
    widths = [
        max(map(len, col))
        for col in itertools.zip_longest(*rows, fillvalue='')
    ]
    yield render_row(rows[0], widths)
    yield render_row(['-'*w for w in widths], widths, sep='+', pad='-')
    for row in rows[1:]:
        yield render_row(row, widths)


def main():
    for arg in sys.argv[1:]:
        table = build_table(arg)
        print("\n".join(render_table(table)))
        print()


if __name__ == '__main__':
    main()
