#!/usr/bin/python3

import numpy as np
import sys


datafile = open(sys.argv[1], "r")
data = np.loadtxt(datafile)
datafile.close()

data = data[:, 1:]
mean = np.mean(data, axis=0)
sd = np.std(data, axis=0)

np.save("mean.npy", mean)
np.save("sd.npy", sd)

scaled = np.apply_along_axis(lambda col : (col - np.mean(col))/np.std(col), 0, data)
cov = np.cov(scaled, rowvar=False)
(eigval, eigvec) = np.linalg.eig(cov)

np.save("eigen.npy", eigvec[:, 0:32])

