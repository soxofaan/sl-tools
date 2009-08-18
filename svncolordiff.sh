#!/bin/sh
svn diff --diff-cmd colordiff -x "-u --ignore-all-space -p" "$@" | less -R
