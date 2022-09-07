#!/bin/bash

# Use this script to update the styleguide and add it to a git commit
# Call this script in the documentation directory

# Clear the working dir from any aux files
TEX_CLEAN

# Add updated files (PARTS needs to be forced due to gitignore
git add styleguide.tex styleguide.pdf
git add -f PARTS/*

git commit -m 'Updated Styleguide.'

