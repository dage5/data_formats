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

def writeUncompressed():
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN, "w", format="NETCDF4")
	tempgrp = rootgrp.createGroup('OutputFile')
	tempgrp.createDimension('lat', sz)
	Latitudes = tempgrp.createVariable('Latitudes', F_TYPE, 'lat')
	Longitudes = tempgrp.createVariable('Longitudes', F_TYPE, 'lat')
	FieldIntensity = tempgrp.createVariable('FieldIntensity', F_TYPE, 'lat')
	GSM_X = tempgrp.createVariable('GSM_X', F_TYPE, 'lat')
	GSM_Y = tempgrp.createVariable('GSM_Y', F_TYPE, 'lat')
	GSM_Z = tempgrp.createVariable('GSM_Z', F_TYPE, 'lat')
	Latitudes[:] = lat
	Longitudes[:] = lon
	FieldIntensity[:] = fi
	GSM_X[:] = x
	GSM_Y[:] = y
	GSM_Z[:] = z
	rootgrp.date = "2010-11-01T01:00:00TZD"
	rootgrp.externalFieldModel = "T05"
	rootgrp.close()
	end = tm.time()
	return end - start


def writeCompressed(scaleoffset = None):
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN, "w", format="NETCDF4")
	tempgrp = rootgrp.createGroup('OutputFile')
	tempgrp.createDimension('lat', len(lat))
	if scaleoffset != None:
		Latitudes = tempgrp.createVariable('Latitudes', F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
		Longitudes = tempgrp.createVariable('Longitudes', F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
		FieldIntensity = tempgrp.createVariable('FieldIntensity', F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
		GSM_X = tempgrp.createVariable('GSM_X', F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
		GSM_Y = tempgrp.createVariable('GSM_Y', F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
		GSM_Z = tempgrp.createVariable('GSM_Z', F_TYPE, 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
	else:
		Latitudes = tempgrp.createVariable('Latitudes', F_TYPE, 'lat',zlib=True,complevel=9, shuffle=True)
		Longitudes = tempgrp.createVariable('Longitudes', F_TYPE, 'lat',zlib=True,complevel=9, shuffle=True)
		FieldIntensity = tempgrp.createVariable('FieldIntensity', F_TYPE, 'lat',zlib=True,complevel=9, shuffle=True)
		GSM_X = tempgrp.createVariable('GSM_X', F_TYPE, 'lat',zlib=True,complevel=9, shuffle=True)
		GSM_Y = tempgrp.createVariable('GSM_Y', F_TYPE, 'lat',zlib=True,complevel=9, shuffle=True)
		GSM_Z = tempgrp.createVariable('GSM_Z', F_TYPE, 'lat',zlib=True,complevel=9, shuffle=True)
	Latitudes[:] = lat
	Longitudes[:] = lon
	FieldIntensity[:] = fi
	GSM_X[:] = x
	GSM_Y[:] = y
	GSM_Z[:] = z
	rootgrp.date = "2010-11-01T01:00:00TZD"
	rootgrp.externalFieldModel = "T05"
	rootgrp.close()
	end = tm.time()
	return end - start

def read():
	start = tm.time()
	rootgrp = Dataset(GLOBAL_FN, "r")
	tempgrp = rootgrp.groups['OutputFile']
	lat = tempgrp.variables['Latitudes'][:]
	lon = tempgrp.variables['Longitudes'][:]
	fi = tempgrp.variables['FieldIntensity'][:]
	x = tempgrp.variables['GSM_X'][:]
	y = tempgrp.variables['GSM_Y'][:]
	z = tempgrp.variables['GSM_Z'][:]
	date = rootgrp.date
	fieldModel = rootgrp.externalFieldModel
	rootgrp.close()
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
