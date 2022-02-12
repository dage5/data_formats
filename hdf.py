import h5py
import numpy as np
import os, sys
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://www.christopherlovell.co.uk/blog/2016/04/27/h5py-intro.html
#https://docs.h5py.org/en/stable/high/file.html
iters = int(sys.argv[1])

F_TYPE = 'float64'

GLOBAL_FN = "mytestfile.hdf5"
GLOBAL_ZIP_NAME = "hdf.zip"

GLOBAL_FN_SMALL = "small.hdf5"
GLOBAL_ZIP_NAME_SMALL = "hdf_small.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]

SMALL_FILE_SIZE = int(sys.argv[2])
(globalData, arrayData) = cn.generateSFvalues(SMALL_FILE_SIZE)

def writeSmall(cfName = "gzip", compression = False, scaleoffset = None):
	cn.rmAny(GLOBAL_FN_SMALL)
	start = tm.time()
	f = h5py.File(GLOBAL_FN_SMALL, "w")
	g = f.create_group('OutputFile')
	if compression == True:
		cprsLvl = 9 if cfName == "gzip" else None
		for data in arrayData:
			g.create_dataset(data, data=arrayData[data], dtype=F_TYPE, compression=cfName, compression_opts=cprsLvl, shuffle = True, scaleoffset = scaleoffset)
	else:
		for data in arrayData:
			g.create_dataset(data, data=arrayData[data], dtype=F_TYPE, scaleoffset = scaleoffset)
	for attrData in globalData:
		g.attrs[attrData] = globalData[attrData]
	f.close()
	end = tm.time()
	return end - start

def readSmall():
	start = tm.time()
	f = h5py.File(GLOBAL_FN_SMALL, "r")
	oFile = f.get('OutputFile')
	globData = {"len": size}
	arrData = {"intens":[],"lcr":[],"ucr":[],"ecr":[]}
	for data in arrData:
		arrData[data] = oFile.get(data)[:]
	for data in globData:
		globData[data] = oFile.attrs[data]
	f.close()
	end = tm.time()
	return end - start

def write(cfName = "gzip", compression = False, scaleoffset = None):
	cn.rmAny(GLOBAL_FN)
	start = tm.time()
	f = h5py.File(GLOBAL_FN, "w")
	g = f.create_group('OutputFile')
	if compression == True:
		cprsLvl = 9 if cfName == "gzip" else None
		for arrayData in aData:
			g.create_dataset(arrayData, data=aData[arrayData], dtype=F_TYPE, compression=cfName, compression_opts=cprsLvl, shuffle = True, scaleoffset = scaleoffset)
	else:
		for arrayData in aData:
			g.create_dataset(arrayData, data=aData[arrayData], dtype=F_TYPE, scaleoffset = scaleoffset)
	for attrData in gData:
		g.attrs[attrData] = gData[attrData]
	f.close()
	end = tm.time()
	return end - start

def read():
	start = tm.time()
	f = h5py.File(GLOBAL_FN, "r")
	oFile = f.get('OutputFile')
	arrData = {"rig":[],"v":[],"rad":[],"eth":[],"efi":[],"ath":[],"afi":[],"time":[],"length":[]}
	globData = {"arr_len": 0, "lcr": 0, "ucr": 0, "ecr": 0, "extern_field": None, "geo_lat": None,"geo_lon": None, "geo_rad": None, "loc_lat": None, "loc_lon": None, "datetime": None, "starting_rig": None, "rig_step": None, "step_limit": None}
	for arrayData in arrData:
		arrData[arrayData] = oFile.get(arrayData)[:]
	for attrData in globData:
		globData[attrData] = oFile.attrs[attrData]
	f.close()
	end = tm.time()
	return end - start

cn.test(lambda: write(), "uncompressed w", iters, GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r", iters)

cn.test(lambda: write(None, False, 2), "lossy uncompressed w", iters, GLOBAL_FN)
cn.test(lambda: read(), "lossy uncompressed r", iters)

#cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", iters, GLOBAL_ZIP_NAME)
#cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r", iters)

cn.test(lambda: write("gzip", True, None), "gzip compressed w", iters, GLOBAL_FN)
cn.test(lambda: read(), "gzip compressed r", iters)

#cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", iters, GLOBAL_ZIP_NAME)
#cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r", iters)

cn.test(lambda: write("gzip", True, 2), "gzip lossy compressed w", iters, GLOBAL_FN)
cn.test(lambda: read(), "gzip lossy compressed r", iters)

cn.test(lambda: write("lzf", True, None), "lzf compressed w", iters, GLOBAL_FN)
cn.test(lambda: read(), "lzf compressed r", iters)

cn.test(lambda: write("lzf", True, 2), "lzf lossy compressed w", iters, GLOBAL_FN)
cn.test(lambda: read(), "lzf lossy compressed r", iters)

#cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip lossy compressed w", iters, GLOBAL_ZIP_NAME)
#cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip lossy compressed r", iters)

cn.test(lambda: writeSmall(), "uncompressed sf w", iters, GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "uncompressed sf w", iters)

cn.test(lambda: writeSmall(None, False, 2), "lossy uncompressed sf w", iters, GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "lossy uncompressed sf w", iters)

cn.test(lambda: writeSmall("gzip", True, None), "gzip compressed sf w", iters, GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "gzip compressed sf w", iters)

cn.test(lambda: writeSmall("gzip", True, 2), "gzip lossy compressed sf w", iters, GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "gzip lossy compressed sf w", iters)

cn.test(lambda: writeSmall("lzf", True, None), "lzf compressed sf w", iters, GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "lzf compressed sf w", iters)

cn.test(lambda: writeSmall("lzf", True, 2), "lzf lossy compressed sf w", iters, GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "lzf lossy compressed sf w", iters)






