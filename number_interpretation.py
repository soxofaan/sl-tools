#!/usr/bin/env python

import functools
import itertools
import sys
from typing import List, Iterator


def _decompose(v: int, base: int = 256) -> Iterator[int]:
    """Break down an integer value into factors for powers of given base"""
    assert base > 0
    s = -1 if v < 0 else 1
    v = abs(v)
    while v:
        v, m = divmod(v, base)
        yield s * m


def decompose_little_endian(value: int, base: int = 256) -> List[int]:
    return list(_decompose(value, base))


def decompose_big_endian(value: int, base: int = 256) -> List[int]:
    return list(reversed(list(_decompose(value, base))))


def to_latin1(v: int):
    """Big endian Latin-1 encoding of given integer"""
    assert v >= 0
    return bytes(decompose_big_endian(v, base=256)).decode('latin-1')


def to_utf8_le(v: int):
    """Little endian UTF-8 encoding of given integer"""
    assert v >= 0
    return bytes(decompose_little_endian(v, base=256)).decode('utf-8')


def to_utf8_be(v: int):
    """Big endian UTF-8 encoding of given integer"""
    assert v >= 0
    return bytes(decompose_big_endian(v, base=256)).decode('utf-8')


PARSERS = [
    ('bin', functools.partial(int, base=2)),
    ('oct', functools.partial(int, base=8)),
    ('dec', functools.partial(int, base=10)),
    ('hex', functools.partial(int, base=16)),
    # TODO: add a "from ascii" parser
]

REPRESENTERS = [
    ('bin', lambda v: bin(v).split('b', 1)[-1]),
    ('oct', lambda v: oct(v).split('o', 1)[-1]),
    ('dec', str),
    ('hex', lambda v: hex(v).split('x', 1)[-1]),
    ('latin1', lambda v: repr(to_latin1(v))),
    ('utf8 LE', lambda v: repr(to_utf8_le(v))),
    ('utf8 BE', lambda v: repr(to_utf8_be(v))),
]


def build_table(arg: str) -> List[List[str]]:
    """Build number interpretation table from given number-like string"""

    table = [
        [str(arg)] + ["to {n}".format(n=name) for name, rep in REPRESENTERS]
    ]

    for name, parser in PARSERS:
        try:
            value = parser(arg)
        except ValueError as e:
            continue
        row = ['from {n}'.format(n=name)]
        for _, rep in REPRESENTERS:
            try:
                row.append(rep(value))
            except ValueError:
                row.append('')
        table.append(row)

    return table


def render_row(row: List[str], widths: List[int], sep: str = '|', pad: str = ' ') -> str:
    return sep + sep.join(pad + c.rjust(w) + pad for c, w in zip(row, widths)) + sep


def render_table(rows: List[List[str]]) -> Iterator[str]:
    # Find width of each column
    widths = [
        max(map(len, col))
        for col in itertools.zip_longest(*rows, fillvalue='')
    ]
    yield render_row(rows[0], widths)
    yield render_row(['-' * w for w in widths], widths, sep='+', pad='-')
    for row in rows[1:]:
        yield render_row(row, widths)


def main():
    for arg in sys.argv[1:]:
        table = build_table(arg)
        print("\n".join(render_table(table)))
        print()


if __name__ == '__main__':
    main()
