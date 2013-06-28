#!/usr/bin/env python
'''
Print something to standard output and standard error.
Optionally, you can also specify a status code the process should exit with.

This is an extremely simple script,
with extreme comment-to-source-code ratio,
but it can be quite handy in one of those rare cases
where you need to test stdout/stderr redirection behavior.
'''

import sys

sys.stdout.write('Hello stdout\n')
sys.stderr.write('Hello stderr\n')

# Optionally exit with a given status code.
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    sys.exit((int)(sys.argv[1]))
