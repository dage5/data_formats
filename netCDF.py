from netCDF4 import Dataset
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://pyhogs.github.io/intro_netcdf4.html
#https://unidata.github.io/netcdf4-python/
sz = 181*361#1000000

F_TYPE = 'f8'

lat = list(np.arange(-90,91,1,dtype=np.float64)) * 361
lon = list(np.arange(0,361,1,dtype=np.float64)) * 181
fi = np.random.uniform(size=sz)
x = np.random.uniform(size=sz)
y = np.random.uniform(size=sz)
z = np.random.uniform(size=sz)

GLOBAL_FN = "test.nc"
GLOBAL_ZIP_NAME = "nc.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]

def writeUncompressed():
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN, "w", format="NETCDF4")
	tempgrp = rootgrp.createGroup('OutputFile')
	tempgrp.createDimension('lat', sz)
	
	for arrayData in aData:
		temp = tempgrp.createVariable(arrayData, F_TYPE, 'lat')
		temp[:] = aData[arrayData]
	
	for attrData in gData:
		setattr(rootgrp, attrData, gData[attrData])
	
	rootgrp.close()
	end = tm.time()
	return end - start


def writeCompressed(scaleoffset = None):
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN, "w", format="NETCDF4")
	tempgrp = rootgrp.createGroup('OutputFile')
	tempgrp.createDimension('lat', sz)
	if scaleoffset != None:
		for arrayData in aData:
			#todo pohrat sa z hodnotou least_significant_digit pre rozne udaje - ovplyvnuje presnost dost vyrazne
			temp = tempgrp.createVariable(arrayData, F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
			temp[:] = aData[arrayData]
	else:
		for arrayData in aData:
			temp = tempgrp.createVariable(arrayData, F_TYPE, 'lat',zlib=True,complevel=9, shuffle=True)
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
