#!/bin/bash

# Utility script to toggle the display of hidden files and folders
# in OS X Finder.
#
# Based on http://artofgeek.com/2009/09/16/toggle-display-of-hidden-files-in-finder-with-keyboard-shortcut

# Clean way to close/quit Finder, allowing it to do cleanup stuff
# and it will also helpfuly fail when Finder is in the middle of something.
# The often suggested way of "killal Finder" is not that clean.
osascript -e 'tell application "Finder" to quit'

# Get the current state of hidden files displaying.
SHOWHIDDEN=$(defaults read com.apple.finder AppleShowAllFiles)
# Toggle the display state.
if [ $SHOWHIDDEN -eq 1 ]; then
    defaults write com.apple.finder AppleShowAllFiles -bool FALSE
else
    defaults write com.apple.finder AppleShowAllFiles -bool TRUE
fi

# Bring Finder back to the foreground.
osascript -e 'tell application "Finder" to activate'

