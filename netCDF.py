from netCDF4 import Dataset
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://pyhogs.github.io/intro_netcdf4.html
#https://unidata.github.io/netcdf4-python/

F_TYPE = 'f8'

GLOBAL_FN = "test.nc"
GLOBAL_ZIP_NAME = "nc.zip"

GLOBAL_FN_SMALL = "small.nc"
GLOBAL_ZIP_NAME_SMALL = "nc_small.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]

SMALL_FILE_SIZE = 65160
(globalData_, arrayData_) = cn.generateSFvalues(SMALL_FILE_SIZE)

def writeSmall(compression = False, lsf=None):
	cn.rmAny(GLOBAL_FN_SMALL)
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN_SMALL, "w", format="NETCDF4")
	tempgrp = rootgrp.createGroup('OutputFile')
	tempgrp.createDimension('lat', SMALL_FILE_SIZE)
	if compression:
		for arrayData in arrayData_:
			#todo pohrat sa z hodnotou least_significant_digit pre rozne udaje - ovplyvnuje presnost dost vyrazne
			temp = tempgrp.createVariable(arrayData, F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=lsf, shuffle=True)
			temp[:] = arrayData_[arrayData]
	else:
		for arrayData in arrayData_:
			temp = tempgrp.createVariable(arrayData, F_TYPE, 'lat',least_significant_digit=lsf, shuffle=True)
			temp[:] = arrayData_[arrayData]
	for attrData in globalData_:
		setattr(rootgrp, attrData, globalData_[attrData])
	rootgrp.close()
	end = tm.time()
	return end - start

def readSmall():
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN_SMALL, "r")
	tempgrp = rootgrp.groups['OutputFile']
	globData = {"len": size}
	arrData = {"intens":[],"lcr":[],"ucr":[],"ecr":[]}
	for arrayData in arrData:
		arrData[arrayData] = tempgrp.variables[arrayData][:]
	for attrData in globData:
		globData[attrData] = getattr(rootgrp, attrData)
	rootgrp.close()
	end = tm.time()
	#print(arrData["rig"])
	return end - start

def write(compression = False, lsf=None):
	cn.rmAny(GLOBAL_FN)
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN, "w", format="NETCDF4")
	tempgrp = rootgrp.createGroup('OutputFile')
	tempgrp.createDimension('lat', sz)
	if compression:
		for arrayData in aData:
			#todo pohrat sa z hodnotou least_significant_digit pre rozne udaje - ovplyvnuje presnost dost vyrazne
			temp = tempgrp.createVariable(arrayData, F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=lsf, shuffle=True)
			temp[:] = aData[arrayData]
	else:
		for arrayData in aData:
			temp = tempgrp.createVariable(arrayData, F_TYPE, 'lat',least_significant_digit=lsf, shuffle=True)
			temp[:] = aData[arrayData]
	for attrData in gData:
		setattr(rootgrp, attrData, gData[attrData])
	rootgrp.close()
	end = tm.time()
	return end - start

def read():
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN, "r")
	tempgrp = rootgrp.groups['OutputFile']
	arrData = {"rig":[],"v":[],"rad":[],"eth":[],"efi":[],"ath":[],"afi":[],"time":[],"length":[]}
	globData = {"arr_len": 0, "lcr": 0, "ucr": 0, "ecr": 0, "extern_field": None, "geo_lat": None,"geo_lon": None, "geo_rad": None, "loc_lat": None, "loc_lon": None, "datetime": None, "starting_rig": None, "rig_step": None, "step_limit": None}
	for arrayData in arrData:
		arrData[arrayData] = tempgrp.variables[arrayData][:]
	for attrData in globData:
		globData[attrData] = getattr(rootgrp, attrData)
	rootgrp.close()
	end = tm.time()
	#print(arrData["rig"])
	return end - start


cn.test(lambda: write(), "uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r")

cn.test(lambda: write(False, 2), "lossy uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "lossy uncompressed r")

#cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
#cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")

cn.test(lambda: write(True, None), "compressed w", GLOBAL_FN)
cn.test(lambda: read(), "compressed r")

#cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
#cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")

cn.test(lambda: write(True, 2), "lossy compressed w", GLOBAL_FN)
cn.test(lambda: read(), "lossy compressed r")

#cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip lossy compressed w", GLOBAL_ZIP_NAME)
#cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip lossy compressed r")

cn.test(lambda: writeSmall(), "uncompressed sf w", GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "uncompressed sf r")

cn.test(lambda: writeSmall(False, 2), "lossy uncompressed sf w", GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "uncompressed sf r")

cn.test(lambda: writeSmall(True, None), "compressed sf w", GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "compressed sf r")

cn.test(lambda: writeSmall(True, 2), "lossy compressed sf w", GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "lossy compressed sf r")











