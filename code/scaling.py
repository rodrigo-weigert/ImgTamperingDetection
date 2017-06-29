#!/usr/bin/python3
import bsm
import os
import sys
import cv2

# scaling.py - Receives input directory and output directory as argument,
# and also one numeric parameter (scaling factor S)
# Scales the image by S in both axis, saving the results
# in the output directory. It appends "Tp_" to the start of the original image
# file name, when saving its blurred version. This is for removeNames.py
# to consider the resulting images as tampered.

inDir, outDir = sys.argv[1], sys.argv[2]
factor = float(sys.argv[3])

total = len(os.listdir(inDir))
count = 0
for img_file in os.listdir(inDir):
	img = cv2.imread(inDir + "/" + img_file, cv2.IMREAD_COLOR)
	img2 = cv2.resize(img, None, fx=factor, fy=factor)
	cv2.imwrite(outDir + "/Tp_" + img_file, img2)
	count = count+1
	print("%d/%d" % (count, total))
