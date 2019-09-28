#!/usr/bin/env python
##############################################################################
# Copyright 2009 Stefaan Lippens
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

'''
Wrapper around ImageMagick convert for easier batch conversion jobs.
'''

import os
import sys
import glob
import re
import optparse

__version__ = '0.4'

# Build the option parser
optparser = optparse.OptionParser(
    usage="usage: %prog [options] imagefilenames",
    description='Resize a batch of image files (e.g. for creating thumbnails or low quality copies for putting on the web). This is in essence a wrapper script that calls ImageMagick\'s convert. The default behaviour is to resize (while maintaining aspect ratio) only if the input image is larger than the target size. Usage example: "%prog -s 500 -o tmp/ -ejpg -q 75 *.jpg *.png", which will resize all JPEG and PNG images from the current directory to 500x500 pixels and save them as JPEG images of quality 75 in directory tmp.',
    version="%prog " + __version__)
optparser.add_option(
    "-s", "--size", metavar="S",
    dest="size", default='500',
    help="Target size (e.g. '500' or '400x300')")
optparser.add_option(
    "-o", "--prefix", metavar="PREFIX",
    dest="prefix", default='',
    help="Prefix for output files, can also be used to define the output directory. Default=''.")
optparser.add_option(
    "-x", "--suffix", metavar="SUFFIX",
    dest="suffix", default='',
    help="Suffix for output files (before the extension). Default=''.")
optparser.add_option(
    "-e", "--filetype", metavar="EXTENSION",
    dest="extension", default=None,
    help="Output file type, (omit to keep original file type).")
optparser.add_option(
    "-q", "--quality", metavar="Q",
    dest="quality", type="int", default=85,
    help="Output (jpeg/png) quality, from 0 (lowest) to 100 (highest).")
optparser.add_option(
    "-a", "--convertarg", metavar="STRING",
    dest="convertargs", action="append", default = [],
    help='Add additional convert arguments/options (see ImageMagick manual or "convert -h"). The arguments should be enclosed in quotes, to avoid interfering with the argument parsing of this wrapper script. For example: -a "-gamma 1.4" --convertarg "-flip"')
optparser.add_option(
    "-n", "--dry-run",
    action="store_true", dest="dryrun", default=False,
    help="Dry run: show what would happen, but don't call convert." )
optparser.add_option(
    "-u", "--upsizetoo",
    action="store_true", dest="upsizetoo", default=False,
    help="Also resize images if they are smaller than the given target size. Disabled by default.")
optparser.add_option(
    "-f", "--forcesize",
    action="store_true", dest="forcesize", default=False,
    help="Do not maintain aspect ratio for resizing. Disabled by default")
optparser.add_option(
    "-i", "--ignoreerrors",
    action="store_true", dest="ignoreerrors", default=False,
    help="Enable ingoring convert errors.")

# Use the option parser to parse the command line arguments
(options, inputImages) = optparser.parse_args()

# if no input images are given: show help and exit
if len(inputImages) == 0:
    print("Error: no input images given", file=sys.stderr)
    optparser.print_help()
    sys.exit()

# process the given options
size = options.size.split('x',1)
if len(size)==1:
    targetWidth = int(size[0])
    targetHeight = int(size[0])
else:
    targetWidth = int(size[0])
    targetHeight = int(size[1])

# the common convert arguments
convertBaseArgv = ['convert']
if options.upsizetoo:
    convertBaseArgv += ['-resize', '%sx%s' % (targetWidth, targetHeight)]
else:
    convertBaseArgv += ['-resize', '%sx%s>' % (targetWidth, targetHeight)]
convertBaseArgv += ['-quality', str(options.quality)]
for convertarg in options.convertargs:
    convertBaseArgv += convertarg.split()


# check if files could be overwritten
if options.prefix == '' and options.suffix == '':
    print("Warning: the input files will/could be overwritten.")
    if not options.dryrun:
        print("Proceed? y/[n]")
        answer = sys.stdin.read(1)
        if answer.lower() != 'y':
            sys.exit()

# handle output directory
targetDir = os.path.split(options.prefix)[0]
if targetDir != '':
    if not os.path.exists(targetDir):
        print("Warning: the output directory '%s' does not exists." % targetDir)
        if not options.dryrun:
            print("Create it? y/[n]")
            answer = sys.stdin.read(1)
            if answer.lower() == 'y':
                os.mkdir(targetDir, 0o755)
            else:
                sys.exit()
    elif not os.path.isdir(targetDir):
        print("Error: '%s' is not a directory" % targetDir, file=sys.stderr)
        sys.exit()

# handle extension
if options.extension != None and options.extension[0] != '.':
    options.extension = '.' + options.extension

# the main loop (the real work)
for inputImage in inputImages:
    inputImageDir, inputImageFilename = os.path.split(inputImage)
    inputImageFilename, inputImageExt = os.path.splitext(inputImageFilename)
    outputImageExt = options.extension or inputImageExt
    outputImage = os.path.join(inputImageDir, options.prefix + inputImageFilename + options.suffix + outputImageExt)
    argv = convertBaseArgv + [inputImage, outputImage]
    command = " ".join(argv)
    print(command)
    if not options.dryrun:
        result = os.spawnvp(os.P_WAIT, argv[0], argv)
        if result != 0 and not options.ignoreerrors:
            print("Error: convert exited with non zero error code", file=sys.stderr)
            sys.exit()
