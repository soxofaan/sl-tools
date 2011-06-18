#!/usr/bin/env python

'''
Script to list the used color expressions (hex codes) in
CSS or SVG files.
'''

import sys
import re
import pprint


def extract_colors_from_file(file_name):
	'''
	Extract the colors from a given file and retun as a set.
	'''
	color_hex_rep = re.compile(r'(#(?:[0-9a-fA-F]{3}){1,2})')
	colors = set()
	for line in open(file_name):
		matches = color_hex_rep.findall(line)
		colors.update(matches)		
	return colors

if __name__ == '__main__':
    
    files = sys.argv[1:]
    
    colors = set()
    for file in files:
    	colors.update(extract_colors_from_file(file))
    	
    pprint.pprint(colors)
