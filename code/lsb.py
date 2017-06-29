#!/usr/bin/python3

# lsb.py - This script wasn't used in the final phase of
# the project, only in the partial report.
# It receives via argument an 8-bit integer (mask) and one or more image files.
# It converts to grayscale and applies the bitwise-AND operation between the mask and every pixel of the images.
# Then it normalizes and displays the result. This allows for one to see the bit planes
# and the least significant bit patterns of the images, for instance.
# Optionally it receives as first argument (before "mask") the flag --color, which
# tells the program to not convert to grayscale and instead use the 3 color channels for the operations.


import cv2
import numpy as np
import sys

def printUsage():
	print("Usage: %s [--color] mask FILES" % sys.argv[0])


def applyMask(pixel, mask):
	return pixel & mask


if len(sys.argv) < 3:
	printUsage()
	exit()


mode = cv2.IMREAD_GRAYSCALE
s = 2

if sys.argv[1] == "--color":
	mode = cv2.IMREAD_COLOR
	s = 3

applyMask = np.vectorize(applyMask)

try:
	mask = np.uint8(sys.argv[s-1])
	for i in range(s, len(sys.argv)):
		img = cv2.imread(sys.argv[i], mode)
		img = applyMask(img, np.uint8(mask))
		img2 = np.copy(img)
		cv2.normalize(img, img2, 0, 255, cv2.NORM_MINMAX)
		cv2.imshow(sys.argv[i] + " - mask: " + "{0:08b}".format(mask), img2)
except:
	printUsage()
	exit()

cv2.waitKey()
cv2.destroyAllWindows()

