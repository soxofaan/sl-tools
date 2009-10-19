#!/usr/bin/python
# author : Stefaan Lippens
# date   : 1 june 2004
# bit version of unix commando "od"

import getopt, sys, os


#(default) settings:
bytesperline = 10
humanbitorder = False
bytespacer = ' '
printbytecounter = True

def usage():
    """print usage pattern of script"""
    print "usage: bd [-h | --help] [-H] [-n] [-b] filename"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hHs:n:b:", ["help"])
except getopt.GetoptError:
    # print help information and exit:
    print "invalid option"
    usage()
    sys.exit(2)

#process commandline options
for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    if o == "-H":
        humanbitorder=True
    if o== "-s":
        bytespacer = a
    if o=="-n":
        if a=="0" or a=="o":
            printbytecounter = False
        else:
            printbytecounter = True
    if o=="-b":
        try:
            bytesperline = int(a)
            if bytesperline <=0:
                raise ValueError
        except ValueError:
            bytesperline = 10
        
#check for 1 input filename
if len(args)!=1:
    print "1 filename needed"
    usage()
    sys.exit(2)
inputfilename = args[0]

#(try to) open file
try:
    input = open(inputfilename,"r")
except IOError:
    print "could't open inputfile '%s' for reading" % inputfilename
    sys.exit(2)


#read file and print bits
try:
    bytes = input.read(bytesperline)
    bytecounter = 0
    while bytes:
        if printbytecounter:
            line = "%-4d:" % bytecounter
        else:
            line = ''
        for byte in bytes:
            val = ord(byte)
            bitcode=['']*8
            for b in range(8):
                bitcode[b] = str(val % 2)
                val //= 2
            if humanbitorder:
                bitcode.reverse()
            line +=  ''.join(bitcode) + bytespacer
        print line
        bytes = input.read(bytesperline)
        bytecounter += bytesperline
except IOError:
    pass


input.close()
