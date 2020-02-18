#!/usr/bin/env python
"""
Print process family tree,
starting from given PIDs (or own PID when none given)
going up the ancestor path.
"""

import sys
import os
import subprocess


def get_pid_ancestors(pid=None):
    """Generator of (pid, command) pairs, going up the ancestor tree"""
    pid = pid or os.getpid()
    while pid > 0:
        out = subprocess.check_output(['ps', '-p', str(pid), '-oppid=', '-ocommand='])
        ppid, command = out.decode('utf-8').strip().split(' ', 1)
        yield pid, command
        pid = int(ppid)


def print_pid_family_tree(pid=None, print=print):
    print('     PID COMMAND')
    for pid, command in reversed(list(get_pid_ancestors(pid))):
        print('{p:8d} {c}'.format(p=pid, c=command))


def main():
    pids = [int(a) for a in sys.argv[1:]] or [os.getpid()]
    for pid in pids:
        print_pid_family_tree(pid)


if __name__ == '__main__':
    main()
