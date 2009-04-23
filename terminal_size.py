#!/usr/bin/env python

import os, sys

def terminal_size():
    '''Best effort guess of terminal size: returns (height, width).'''
    try:
        # Try to get size from ioctl system call (Unix only).
        import struct, fcntl, termios
        # Dummy string, determining answer buffer size
        # (for struct of two unsigend short ints) for ioctl call.
        dummy_string = struct.pack('HH', 0, 0)
        # File descriptor of standard output.
        file_descriptor = sys.stdout.fileno()
        # The ioctl call to get terminal size.
        answer = fcntl.ioctl(file_descriptor, termios.TIOCGWINSZ, dummy_string)
        # Unpack answer to height and width values.
        height, width = struct.unpack('HH', answer)
    except (ImportError, IOError):
        try:
            # Try to get size from environment variables.
            height, width = int(os.environ['LINES']), int(os.environ['COLUMNS'])
        except KeyError:
            # No info found: just use some sensible defaults.
            height, width = (25, 80)
    return height, width

if __name__ == '__main__':
    print terminal_size()
