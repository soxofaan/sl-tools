#!/bin/sh
cvs diff -bup "$@" | colordiff | less -R
