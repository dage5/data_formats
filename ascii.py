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

settings = dict()
def writeUncompressed():
	start = tm.time()
	cn.writeAscii(gData, aData, GLOBAL_FN)
	end = tm.time()
	return end - start

def read():
	start = tm.time()
	cn.loadData()
	end = tm.time()
	return end - start

cn.test(writeUncompressed, "uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r")

cn.test(lambda: (writeUncompressed() + cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME)), "zip compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: (read() + cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME)), "zip compressed r")


#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
