#!/usr/bin/env python

import sys
import os
import subprocess

def main():
    # Process id to start from
    if len(sys.argv) == 1:
        pid = os.getpid()
    elif len(sys.argv) == 2:
        pid = int(sys.argv[1])
    else:
        raise ValueError('Zero or one argument expected')

    # Print header.
    print("{pid:>8s} {cmd}".format(pid='PID', cmd='CMD'))

    while pid > 0:
        # Get command an parent process id
        command = ['ps', '-p', str(pid), '-o',  'ppid=', '-o', 'command=']
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        stdout = stdout.strip()
        if len(stdout) == 0:
            raise ValueError('No process info for pid {pid}'.format(pid=pid))
        ppid, command = stdout.split(None, 1)
        ppid = int(ppid)

        # Show command
        print("{pid:8d} {cmd}".format(pid=pid, cmd=command))

        # Go up the chain
        pid = ppid

if __name__ == '__main__':
    main()