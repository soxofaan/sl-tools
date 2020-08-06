#!/usr/bin/env python
"""
Tool to search for file duplicates, based on file size and content hash/digest
"""

# TODO: add option to control size representation (human readable, kB, kiB, ...)
# TODO: add option to exclude paths/patterns from recursive directory exploring
# TODO: show progress bar?
# TODO: add option to only compare filesize (not content hash)
# TODO: add option to control the size of the content to hash
# TODO: add logging/verbosity

import hashlib
import os
import argparse


def main():
    # Handle command line interface
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("path", nargs="*")

    arguments = arg_parser.parse_args()

    # Determine which files to compare
    if len(arguments.path) < 1:
        seeds = '.'
    else:
        seeds = arguments.path
    file_list = get_file_list(seeds)

    # Phase 1: group on file size and keep only real groups (two items or more)
    size_groups = group_on_filesize(file_list)
    size_groups = remove_small_groups(size_groups, minimum_size=2)

    # Phase 2: also check file contents in each group
    content_groups = {}
    for size, group in size_groups.items():
        subgroups = group_on_content_hash(group)
        subgroups = remove_small_groups(subgroups, minimum_size=2)
        for hash, subgroup in subgroups.items():
            content_groups[(size, hash)] = subgroup

    # Report
    if len(content_groups) > 0:
        print("Found these possible duplicates:")
        for (size, hash), group in content_groups.items():
            print('--- size: {size} B, content hash: {hash} ---'.format(size=size, hash=hash))
            for file in group:
                print(file)
    else:
        print('No duplicates found')


def get_file_list(seeds):
    """
    Build file list based on given seeds: file names
    directory names (which will be explored recursively)

    @param seeds list of files or directories
    """

    file_list = []
    for seed in seeds:
        if os.path.isfile(seed):
            # just add files
            file_list.append(seed)
        elif os.path.isdir(seed):
            # Recursively explore directories
            for (dirpath, dirnames, filenames) in os.walk(seed):
                for filename in filenames:
                    file_list.append(os.path.join(dirpath, filename))
        else:
            raise RuntimeError('Could not find file/directory "{0}"'.format(seed))
    return file_list


def remove_small_groups(d, minimum_size=2):
    """
    Get a dictionary of lists and remove entries with small lists.

    @param d: dictionary of lists
    @param minimum_size: minimum size a list should have

    @return dictionary of lists with length equal or greater than given threshold
    """
    d2 = {}
    for key, data in d.items():
        if len(data) >= minimum_size:
            d2[key] = data
    return d2


def group_on_filesize(filenames):
    """
    Group a list of files on file size.

    @param filenames list of file paths

    @return dictionary mapping file size to list of files with that file size
    """
    map = {}
    for f in filenames:
        size = os.path.getsize(f)
        map[size] = map.get(size, []) + [f]
    return map


def group_on_content_hash(filenames):
    """
    Group a list of files on a hash/digest of their content (MD5)

    @param filenames list of file paths

    @return dictionary mapping hash to list of files with that hash
    """
    map = {}
    for f in filenames:
        md5 = md5hash(f)
        map[md5] = map.get(md5, []) + [f]
    return map


def md5hash(filename, size=5000):
    """
    Helper function to calculate MD5 hash of the file contents
    (up to a given number of bytes).

    @param filename file path of file to process
    @param size the maximum number of bytes to read
    """
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read(size)).hexdigest()


if __name__ == '__main__':
    main()
