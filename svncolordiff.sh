#!/bin/sh
svn di --diff-cmd colordiff "$@" | less -r
