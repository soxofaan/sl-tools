#!/bin/sh
svn diff --diff-cmd colordiff -x "-u -b -p" "$@" | less -r
