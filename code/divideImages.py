#!/usr/bin/python3
import sys
import os
import numpy as np
import cv2

# divideImages.py - Divides images in a directory into several smaller blocks.
# ... (TODO: further explanation).

img_count = 0
directory = "classifier images"

def divideImg(img, nblocks):
	w, h = img.shape[0]//nblocks, img.shape[1]//nblocks
	corner_x = 0
	global img_count
	global directory

	if not os.path.exists(directory + "/edited"):
		os.makedirs(directory + "/edited")
	if not os.path.exists(directory + "/not_edited"):
		os.makedirs(directory + "/not_edited")
	
	while corner_x < img.shape[0]:
		corner_y = 0
		while corner_y < img.shape[1]:
			block = img[corner_x:corner_x+w, corner_y:corner_y+h]
			cv2.imshow("y/n/x/c?", block)
			key = cv2.waitKey(0)
			cv2.destroyAllWindows()
			
			if key == ord('y'):
				cv2.imwrite(directory + "/edited/" + str(img_count+1) + ".jpg", block)
				img_count = img_count + 1
				print("saved with class 'edited'")
			elif key == ord('n'):
				cv2.imwrite(directory + "/not_edited/" + str(img_count+1) + ".jpg", block)
				img_count = img_count + 1
				print("saved with class 'not_edited'")
			elif key == ord('x'):
				print("discarded")
			elif key == ord('c'):
				return

			corner_y = corner_y + h
		corner_x = corner_x + w

directory = sys.argv[1]
n = int(sys.argv[2])

for img_file in os.listdir(directory):
	img = cv2.imread(directory + "/" + img_file, cv2.IMREAD_COLOR)
	divideImg(img, n)
