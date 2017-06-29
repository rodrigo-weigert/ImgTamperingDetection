#!/usr/bin/python3
import bsm
import os
import sys
import cv2

# extractFeatures.py - uses bsm.py module to extract all the 102 features
# from the images of a directory, which is received by argument.
# Outputs one line per image, containing its name followed by the features.

directory = sys.argv[1]

totalFiles = len(os.listdir(directory))
count = 0

for img_file in os.listdir(directory):
	img = cv2.imread(directory + "/" + img_file, cv2.IMREAD_COLOR)
	print(img_file + " ", end='')
	for feature in bsm.getFeatures(img):
		print(feature, end=' ')
	print()
	count = count+1
	print(str(count) + "/" + str(totalFiles) + " (%.2f %%)" % (100 * count/totalFiles), file=sys.stderr)
