#!/bin/bash

pdoc src/pipetex/* --docformat google -o ~/Documents/Code/MaxWeise.github.io/
cd ~/Documents/Code/MaxWeise.github.io/
git add *
git commit -m 'Updated API Documentation'
git push
cd ~/Documents/Code/pipetex/

