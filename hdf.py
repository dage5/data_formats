import h5py
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://www.christopherlovell.co.uk/blog/2016/04/27/h5py-intro.html
#https://docs.h5py.org/en/stable/high/file.html

F_TYPE = 'float64'

GLOBAL_FN = "mytestfile.hdf5"
GLOBAL_ZIP_NAME = "hdf.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]

def writeUncompressed():
	start = tm.time()
	f = h5py.File(GLOBAL_FN, "w")
	g = f.create_group('OutputFile')
	
	for arrayData in aData:
		g.create_dataset(arrayData, data=aData[arrayData], dtype=F_TYPE)

	
	for attrData in gData:
		g.attrs[attrData] = gData[attrData]
	
	f.close()
	end = tm.time()
	return end - start


def writeCompressed(scaleoffset = None):
	start = tm.time()
	f = h5py.File(GLOBAL_FN, "w")
	g = f.create_group('OutputFile')
	if scaleoffset != None:
		for arrayData in aData:
			g.create_dataset(arrayData, data=aData[arrayData], dtype=F_TYPE, compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
	else:
		for arrayData in aData:
			g.create_dataset(arrayData, data=aData[arrayData], dtype=F_TYPE, compression="gzip", compression_opts=9, shuffle = True)
	
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

cn.test(writeUncompressed, "uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r")


cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")

cn.test(lambda: writeCompressed(), "compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: read(), "compressed r")

cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")

cn.test(lambda: writeCompressed(2), "lossy compressed w", GLOBAL_FN)
cn.test(lambda: read(), "lossy compressed r")

cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip lossy compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip lossy compressed r")


#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
