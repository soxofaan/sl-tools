#!/bin/sh
cvs diff -bup "$@" | colordiff | less -r
