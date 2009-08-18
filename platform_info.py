#!/usr/bin/env python

'''
Use the platform module to query information about the platform:
call all public functions in the module.
'''

import platform

for name in dir(platform):
    if not name.startswith('_'):
        try:
            print "%s(): %s" % (name, platform.__dict__[name]())
        except TypeError:
            pass
