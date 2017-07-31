#!/usr/bin/python3
import sys
import numpy as np
import bsm
import cv2

try:
	img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
	if img is None:
		sys.exit(2)
except IndexError:
	sys.exit(1)

f = bsm.getFeatures(img)

mean = np.load("data/mean.npy")
sd = np.load("data/sd.npy")
eig = np.load("data/eigen.npy")

f = (f - mean)/sd

result = np.matmul(f, eig)

for x in result:
	print(x)
