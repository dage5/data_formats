import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://github.com/MAVENSDC/cdflib

GLOBAL_FN = "test.ascii"
GLOBAL_ZIP_NAME = "ascii.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]

def writeUncompressed():
	cn.rmAny(GLOBAL_FN)
	start = tm.time()
	cn.writeAscii(gData, aData, GLOBAL_FN)
	end = tm.time()
	return end - start

def read():
	start = tm.time()
	cn.loadData()
	end = tm.time()
	return end - start

def writeSmallFiles(intensity, rigidityL, rigidityU, rigidityE, dirName = "./inFiles/"):
	cn.rmAny(dirName)
	start = tm.time()
	os.makedirs(dirName, exist_ok = True)
	size = len(intensity)
	for i in range(0, size):
		with open(dirName + "rigidity_"+str(i)+".dat", "w") as f:
			f.write("{:f} {:.4f} {:.3f}".format(rigidityL[i], rigidityU[i], rigidityE[i]))
		with open(dirName + "intensity_"+str(i)+".dat", "w") as f:
			f.write("{:.5f}".format(intensity[i]))
	end = tm.time()
	return end - start

def readSmallFiles(size, dirName = "./inFiles/"):
	start = tm.time()
	intensity = []
	rigidityL = []
	rigidityU = []
	rigidityE = []
	
	for i in range(0, size):
		with open(dirName + "rigidity_"+str(i)+".dat", "r") as f:
			content = f.read()
			rl, ru, re = content.split()
			rigidityL.append(float(rl))
			rigidityU.append(float(ru))
			rigidityE.append(float(re))
		with open(dirName + "intensity_"+str(i)+".dat", "r") as f:
			intensity.append(float(f.read()))
	end = tm.time()
	return end - start

cn.test(writeUncompressed, "uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r")

cn.test(lambda: (writeUncompressed() + cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME)), "zip compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: (read() + cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME)), "zip compressed r")

(intensity, rigidityL, rigidityU, rigidityE) = cn.generateSFvalues(100)
cn.test(lambda: writeSmallFiles(intensity, rigidityL, rigidityU, rigidityE), "uncompressed sf w", "./inFiles/")
cn.test(lambda: readSmallFiles(100), "uncompressed sf r")





