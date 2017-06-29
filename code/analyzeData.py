#!/usr/bin/python3

# analyzeData.py - Analyzes a .dat file (in the format which is output by
# separateImages.py and processData.py), counting the number of instances of 
# each class (tampered and authentic). This information helps us determine the quality 
# of our classifiers. The name of the file is passed as an argument.

import numpy as np
import sys

filename = sys.argv[1]
f = open(filename, "rb")

data = np.loadtxt(filename)

tampered = np.int(np.sum(data[:, 0]))
total = data.shape[0]
authentic = total - tampered

print("authentic: %d (%1.3f %%), tampered: %d (%1.3f %%), total: %d" % (authentic, 100*authentic/total, tampered, 100*tampered/total, total))


