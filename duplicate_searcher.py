'''
Created on Feb 2, 2010

@author: slippens

Small tool for looking for file duplicates.

Checking is done based on file contents, not file name.
'''

import os
import stat

class Index(dict):
    '''
    An index of files and their file sizes.
    Implemented as a dictionary mapping file sizes to lists of the corresponding
    files
    '''
    def __init__(self):
        dict.__init__(self)

    def add(self, filename):
        '''Add a file to the index.'''
        size = os.path.getsize(filename)
        self[size] = self.get(size, []) + [filename]


    def walk(self, top):
        '''
        Walk recursively through a folder and add all files to the index.
        '''
        for (dirpath, dirnames, filenames) in os.walk(top):
            for filename in filenames:
                self.add(os.path.join(dirpath, filename))

    def get_same_size_files(self):
        '''
        Extract entries of the index where there are multiple files with the
        same file size.
        
        @return: a Index dictionary with only entries with two or more files.  
        '''
        d = {}
        for size, files in self.iteritems():
            if len(files) > 1:
                d[size] = files
        return d


if __name__ == '__main__':

    index = Index()
    index.walk('.')

    d = index.get_same_size_files()
    for size, files in d.iteritems():
        print 'Have same size of %d bytes:' % size
        print ', '.join(files)    
    
