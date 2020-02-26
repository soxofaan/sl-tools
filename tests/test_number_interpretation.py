import pytest

from number_interpretation import decompose_little_endian, decompose_big_endian, to_latin1, to_utf8_le, to_utf8_be, \
    build_table


@pytest.mark.parametrize(
    ['value', 'base', 'expected'], [
        (0, 2, []),
        (1, 2, [1]),
        (3, 2, [1, 1]),
        (4, 2, [0, 0, 1]),
        (31, 2, [1, 1, 1, 1, 1]),
        (12345, 10, [5, 4, 3, 2, 1]),
        (1000, 8, [0, 5, 7, 1]),
        (1000, 16, [8, 14, 3]),
        (12345, 100, [45, 23, 1]),
        (-1, 2, [-1]),
        (-7, 2, [-1, -1, -1]),
        (-12345, 10, [-5, -4, -3, -2, -1]),
        (-1000, 16, [-8, -14, -3]),
    ]
)
def test_decompose_little_endian(value, base, expected):
    assert decompose_little_endian(value, base) == expected


@pytest.mark.parametrize(
    ['value', 'base', 'expected'], [
        (0, 2, []),
        (4, 2, [1, 0, 0]),
        (12345, 10, [1, 2, 3, 4, 5]),
        (1000, 8, [1, 7, 5, 0]),
        (1000, 16, [3, 14, 8]),
        (12345, 100, [1, 23, 45]),
        (-1, 2, [-1]),
        (-12345, 10, [-1, -2, -3, -4, -5]),
    ]
)
def test_decompose_big_endian(value, base, expected):
    assert decompose_big_endian(value, base) == expected


def test_to_latin1_single_byte():
    for b in range(1, 256):
        assert to_latin1(b) == chr(b)


def test_to_latin1():
    assert to_latin1(89 * 256 + 111) == 'Yo'


def test_to_utf8_le():
    assert to_utf8_le((128 + 64 + 216 // 64) + (128 + (216 % 64)) * 256) == chr(216)


def test_to_utf8_be():
    assert to_utf8_be((128 + 64 + 216 // 64) * 256 + (128 + (216 % 64))) == chr(216)


def test_build_table():
    table = build_table('10')
    assert table[0][:3] == ['10', 'to bin', 'to oct']
    assert table[1:] == [
        ['from bin', '10', '2', '2', '2', "'\\x02'", "'\\x02'", "'\\x02'"],
        ['from oct', '1000', '10', '8', '8', "'\\x08'", "'\\x08'", "'\\x08'"],
        ['from dec', '1010', '12', '10', 'a', "'\\n'", "'\\n'", "'\\n'"],
        ['from hex', '10000', '20', '16', '10', "'\\x10'", "'\\x10'", "'\\x10'"],
    ]
