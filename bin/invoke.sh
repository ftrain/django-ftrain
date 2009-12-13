#!/bin/bash

# Quick hack to run a custom manage_* script based on uname; thus I
# can have manage_home, manage_work, etc, although it would make far
# more sense to modify settings based on hostname and hack my own
# settings.py file.

./manage_`uname -n`.py $1 $2 $3 $4 $5;