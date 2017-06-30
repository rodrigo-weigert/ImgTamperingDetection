#!/usr/bin/python3

# bsm.py - Calculates all the Binary Similarity Measures (BSMs) presented
# in the reference paper for this project. This script is used as a module,
# it is imported by extractFeatures.py.

import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Returns a binary image (for each channel, if RGB) of bit plane pl (0:least significant - 7: most significant).
# The binary image will have values 0-1, not 0-255.
# pl must be between 0 (less significant bit) and 7 (most significant bit), inclusive.
def getBitPlane(pixel, pl):
	if (pixel & (1 << pl)) == 0:
		return np.uint8(0)
	return np.uint8(1)

getBitPlane = np.vectorize(getBitPlane)


# Extracts a channel (R, G or B) from an RGB image.
def getChannel(img, channel):
	if channel == 'R':
		return img[:, :, 0]
	elif channel == 'G':
		return img[:, :, 1]
	else:
		return img[:, :, 2]

# Given a binary image (0-1), returns a matrix whose
# each position (i, j) holds the amount of neighboring pixels
# (4-neighborhood) with value 1 of pixel (i, j)
def countNeighbors(binImg):
	f4 = np.array([	[0, 1, 0],
					[1, 0, 1],
					[0, 1, 0] ], dtype=np.uint8)
	return cv2.filter2D(binImg, -1, f4, borderType=cv2.BORDER_CONSTANT)


# Given a pixel from a binary image and the number
# of pixels with value 1 in the 4-neighborhood of the pixel,
# returns the measure alpha_j of the pixel.
# alpha_1: 0 if pixel is 1, else the amount of pixels 0 in the neighborhood.
# alpha_2: 0 if pixel is 1, else the amount of pixels 1 in the neighborhood.
# alpha_3: 0 if pixel is 0, else the amount of pixels 0 in the neighborhood.
# alpha_4: 0 if pixel is 0, else the amount of pixels 1 in the neighborhood.
def pixel_alpha(pixel, neigh, j):
	if j == 1:
		if pixel == 0:
			return np.uint8(4-neigh)
		else:
			return np.uint8(0)
	elif j == 2:
		if pixel == 0:
			return np.uint8(neigh)
		else:
			return np.uint8(0)
	elif j == 3:
		if pixel == 0:
			return np.uint8(0)
		else:
			return np.uint8(4-neigh)
	else:
		if pixel == 0:
			return np.uint8(0)
		else:
			return np.uint8(neigh)

pixel_alpha = np.vectorize(pixel_alpha)

# Given a binary image (0-1) and a parameter j (1, 2, 3 or 4),
# obtains a matrix with the alpha_j measure for each pixel of the image.
# Returns a sum of the elements of this matrix.
def alpha(binImg, j):
	neigh = countNeighbors(binImg)
	return np.sum(pixel_alpha(binImg, neigh, j), dtype=np.uint64)

def alpha_vector(binImg):
	return np.maximum(np.array([alpha(binImg, 1), alpha(binImg, 2), alpha(binImg, 3), alpha(binImg, 4)], dtype=np.uint64), 1)

def co_occurance(alpha_v):
	return np.float64(alpha_v) / np.float64(np.sum(alpha_v))

# Ojala texture measures
def ojala_score(binImg):
	ofilter = np.array([[1, 2, 4],
					[128, 0, 8],
					[64, 32, 16] ], dtype=np.uint8)
	return cv2.filter2D(binImg, -1, ofilter, borderType=cv2.BORDER_CONSTANT)

# For calculating the normalized histogram of the ojala scores.
def histogram(mat):
	hist = np.bincount(mat.ravel(), minlength=256)
	hist = np.maximum(hist, 1)
	return hist/np.sum(hist)

# Calculating correlations of a single binary image.
def getIntraFeatures(binImg, alpha_v):
	a, b, c, d = alpha_v / (binImg.shape[0] * binImg.shape[1])
	m = [0] * 9
	m[0] = a/(a+b) + a/(a+c) + d/(b+d) + d/(c+d)
	m[1] = a*d / np.sqrt((a+b)*(a+c)*(b+d)*(c+d))
	m[2] = (2*(a+d)) / (2*(a+d)+b+c)
	m[3] = a / (a+2*(b+c))
	m[4] = (a+d) / (b+c)
	m[5] = a / (b+c)
	m[6] = np.sqrt((a/(a+b)) * (a/(a+c)))
	m[7] = (b+c) / (2*a+b+c)
	m[8] = (b*c) / (a+b+c+d)**2
	return m

# Correlations between two binary images.
def getInterFeatures(binImg1, binImg2, alpha_v1, alpha_v2):
	dm = [0] * 8
	p1 = co_occurance(alpha_v1)
	p2 = co_occurance(alpha_v2)

	dm[0] = np.sum(np.minimum(p1, p2))
	dm[1] = np.sum(np.abs(p1-p2))
	dm[2] = -np.sum(p1 * np.log(p2))
	dm[3] = -np.sum(p1 * np.log(p1/p2))

	s1 = histogram(ojala_score(binImg1))
	s2 = histogram(ojala_score(binImg2))
	
	dm[4] = np.sum(np.minimum(s1[1:], s2[1:]))
	dm[5] = np.sum(np.abs(s1[1:] - s2[1:]))
	dm[6] = -np.sum(s1[0:16] * np.log(s2[0:16]))
	dm[7] = -np.sum(s1[1:] * np.log(s1[1:]/s2[1:]))
	
	return dm

# Returns all the 102 features used by Bayram.
def getFeatures(img):	
	img_r = getChannel(img, 'R')
	img_b = getChannel(img, 'B')

	r_bitplane = []
	r_alphas = []
	features = []

	for i in range(2, 8):
		bp = getBitPlane(img_r, i)
		a = alpha_vector(bp)
		r_bitplane.append(bp)
		r_alphas.append(a)
		features.extend(getIntraFeatures(bp, a))
	for i in range(2, 7):
		bp1, bp2 = r_bitplane[i-2], r_bitplane[i-1]
		a1, a2 = r_alphas[i-2], r_alphas[i-1]
		features.extend(getInterFeatures(bp1, bp2, a1, a2))

	b_bitplane = getBitPlane(img_b, 4)
	b_alpha = alpha_vector(b_bitplane)
	features.extend(getInterFeatures(r_bitplane[4-3], b_bitplane, r_alphas[4-3], b_alpha))

	return features
