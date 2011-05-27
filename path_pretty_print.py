#!/usr/bin/env python

'''
Simple tool to pretty print the environment
variable $PATH and the Python path ($PYTHONPATH).
'''

import os
import sys
import pprint

def main():
    print('os.environ["PATH"] (aka $PATH):')
    pprint.pprint(os.environ['PATH'].split(':'))

    print('sys.path:')
    pprint.pprint(sys.path)

if __name__ == '__main__':
    main()
