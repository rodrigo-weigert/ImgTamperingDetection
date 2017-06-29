#!/usr/bin/python3
import bsm
import os
import sys
import cv2

# gaussian.py - Receives input directory and output directory as argument,
# and also two numeric parameters (square kernel size and sigma for the gaussian blur)
# Applies gaussian blur to all the images of the input directory, saving the results
# in the output directory. It appends "Tp_" to the start of the original image
# file name, when saving its blurred version. This is for removeNames.py
# to consider the resulting images as tampered.

inDir, outDir = sys.argv[1], sys.argv[2]
kernelSize, sigma = int(sys.argv[3]), float(sys.argv[4])

total = len(os.listdir(inDir))
count = 0
for img_file in os.listdir(inDir):
	img = cv2.imread(inDir + "/" + img_file, cv2.IMREAD_COLOR)
	img2 = cv2.GaussianBlur(img, (kernelSize, kernelSize), sigma)
	cv2.imwrite(outDir + "/Tp_" + img_file, img2)
	count = count+1
	print("%d/%d" % (count, total))
