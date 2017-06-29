#!/usr/bin/python3

# randomSample.py - receives by argument an input directory of images, an output
# directory and a number N.
# Selects randomly N images from the input directory and saves in the output directory.

import sys
import os
from random import shuffle
from shutil import copy

inDir, outDir, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
files = os.listdir(inDir)
shuffle(files)
for i in range(N):
	copy(inDir + "/" + files[i], outDir + "/" + files[i])
