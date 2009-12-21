#!/usr/bin/env python

'''
Small tool to show a readable version of the Java class path environment
variable.
'''

import sys
import os
import pprint

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        classpath = sys.argv[1]
    else:
        classpath = os.environ['CLASSPATH']
        
    pprint.pprint(classpath.split(':'))
    
