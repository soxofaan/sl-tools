#!/usr/bin/env python
##############################################################################
# Copyright 2008 Stefaan Lippens
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
##############################################################################

"""
Script to make it esier to add svn-ignore rules.
"""

import sys
import os
import subprocess

def svn_propget_svnignore(path):
    '''fetch the svn:ignore property of given path'''
    p = subprocess.Popen(['svn', 'propget', 'svn:ignore', path], stdout=subprocess.PIPE)
    p.wait()
    data = p.stdout.read().strip()
    return data

def svn_propset_svnignore(path, value):
    '''set the svn:ignore property of the given path'''
    p = subprocess.Popen(['svn', 'propset', 'svn:ignore', value, path])
    p.wait()


def main():

    if len(sys.argv) < 2:
        print 'Usage: %s filenames' % sys.argv[0]
        sys.exit()

    for path in sys.argv[1:]:
        print path

        dirpath, filename = os.path.split(path)
        svnignore_data = svn_propget_svnignore(dirpath)

        if filename not in svnignore_data.split('\n'):
            svnignore_data += '\n' + filename
            svn_propset_svnignore(dirpath, svnignore_data)

if __name__ == '__main__':
    main()
