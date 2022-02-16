import numpy as np
import os, sys
import time as tm
#from hurry.filesize import size, si
import subprocess
import common as cn
#https://github.com/MAVENSDC/cdflib

iters = int(sys.argv[1])

GLOBAL_FN = "test.ascii"
GLOBAL_ZIP_NAME = "ascii.zip"

GLOBAL_SF_FN = "./inFiles/"
GLOBAL_SF_ZIP_NAME = "ascii_sf.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]

SMALL_FILE_SIZE = int(sys.argv[2])
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
			f.write("{:.2f} {:.2f} {:.2f}".format(arrayData["lcr"][i], arrayData["ucr"][i], arrayData["ecr"][i]))
		with open(dirName + "intensity_"+str(i)+".dat", "w") as f:
			f.write("{:.6f}".format(arrayData["intens"][i]))
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

cn.test(lambda: writeUncompressed(), "uncompressed w", iters, GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r", iters)

cn.test(lambda: (writeUncompressed() + cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME)), "zip compressed w", iters, GLOBAL_ZIP_NAME)
cn.test(lambda: (cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME) + read()), "zip compressed r", iters)

cn.test(lambda: writeSmallFiles(globalData, arrayData), "uncompressed sf w", iters, "./inFiles/")
cn.test(lambda: readSmallFiles(SMALL_FILE_SIZE), "uncompressed sf r", iters)

cn.test(lambda: (writeSmallFiles(globalData, arrayData) + cn.extraCompression(GLOBAL_SF_FN, GLOBAL_SF_ZIP_NAME)), "zip compressed sf w", iters, GLOBAL_SF_ZIP_NAME)

cn.test(lambda: (cn.extraCompressedRead(GLOBAL_SF_FN, GLOBAL_SF_ZIP_NAME) + readSmallFiles(SMALL_FILE_SIZE)), "zip compressed sf r", iters)





