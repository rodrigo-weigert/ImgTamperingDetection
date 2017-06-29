#!/usr/bin/python3
import sys

# separateImages.py - Used to separate tampered images which underwent
# specific processes (as identified by its name - see http://forensics.idealtest.org/casiav2/).
# It takes as input a .dat file containing the names of the images and their features (one image per line),
# exactly as it is output by extractFeatures.py. It also receives as arguments parameters to indicates what images to select.

ANY = "A"
IMG_SOURCE = 1
OP_TYPE = 2
RG_SIZE = 3
POST_PROC = 4

filename = sys.argv[1]
imgsource = sys.argv[2]
optype = sys.argv[3]
rgsize = sys.argv[4]
postproc = sys.argv[5]

#Gera o arquivo seletivo
newfile = "Tp_" + imgsource + "_" + optype + "_" + rgsize + "_" + postproc + ".dat"

outputfile = open(newfile, "w")

with open(filename) as f:
	lines = f.readlines()

for line in lines:
	selected = True
	features = line.split(" ", 1)
	image = features[0].split("_")
	if image[IMG_SOURCE] != imgsource:
		selected = False
	if optype[0] != ANY and image[OP_TYPE][0] != optype[0]:
		selected = False
	if optype[1] != ANY and image[OP_TYPE][1] != optype[1]:
		selected = False
	if optype[2] != ANY and image[OP_TYPE][2] != optype[2]:
		selected = False
	if rgsize != ANY and image[RG_SIZE] != rgsize:
		selected = False
	if postproc != ANY and image[POST_PROC] != postproc:
		selected = False
	if selected:
		print("Selected " + features[0] + ".")
		outputfile.write(line)
outputfile.close()
