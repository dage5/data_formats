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

SMALL_FILE_SIZE = 65160
(globalData, arrayData) = cn.generateSFvalues(SMALL_FILE_SIZE)

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

def writeSmallFiles(globalData, arrayData, dirName = "./inFiles/"):
	cn.rmAny(dirName)
	start = tm.time()
	os.makedirs(dirName, exist_ok = True)
	size = globalData["len"]
	for i in range(0, size):
		with open(dirName + "rigidity_"+str(i)+".dat", "w") as f:
			f.write("{:f} {:.4f} {:.3f}".format(arrayData["lcr"][i], arrayData["ucr"][i], arrayData["ecr"][i]))
		with open(dirName + "intensity_"+str(i)+".dat", "w") as f:
			f.write("{:.5f}".format(arrayData["intens"][i]))
	end = tm.time()
	return end - start

def readSmallFiles(size, dirName = "./inFiles/"):
	start = tm.time()
	globalData = {"len": size}
	arrayData = {"intens":[],"lcr":[],"ucr":[],"ecr":[]}
	for i in range(0, size):
		with open(dirName + "rigidity_"+str(i)+".dat", "r") as f:
			content = f.read()
			rl, ru, re = content.split()
			arrayData["lcr"].append(float(rl))
			arrayData["ucr"].append(float(ru))
			arrayData["ecr"].append(float(re))
		with open(dirName + "intensity_"+str(i)+".dat", "r") as f:
			arrayData["intens"].append(float(f.read()))
	end = tm.time()
	return end - start

cn.test(writeUncompressed, "uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r")

#cn.test(lambda: (writeUncompressed() + cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME)), "zip compressed w", GLOBAL_ZIP_NAME)
#cn.test(lambda: (read() + cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME)), "zip compressed r")

cn.test(lambda: writeSmallFiles(globalData, arrayData), "uncompressed sf w", "./inFiles/")
cn.test(lambda: readSmallFiles(SMALL_FILE_SIZE), "uncompressed sf r")





