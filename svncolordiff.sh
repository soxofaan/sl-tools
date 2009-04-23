#!/bin/sh
svn di --diff-cmd colordiff -x "-u -b -p" "$@" | less -r
