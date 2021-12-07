import h5py
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://www.christopherlovell.co.uk/blog/2016/04/27/h5py-intro.html
#https://docs.h5py.org/en/stable/high/file.html
sz = 181*361#1000000

F_TYPE = 'float64'

lat = list(np.arange(-90,91,1,dtype=np.float64)) * 361
lon = list(np.arange(0,361,1,dtype=np.float64)) * 181
fi = np.random.uniform(size=sz)
x = np.random.uniform(size=sz)
y = np.random.uniform(size=sz)
z = np.random.uniform(size=sz)

GLOBAL_FN = "mytestfile.hdf5"
GLOBAL_ZIP_NAME = "hdf.zip"

def writeUncompressed():
	start = tm.time()
	f = h5py.File(GLOBAL_FN, "w")
	g = f.create_group('OutputFile')
	g.attrs['ExternalFieldModelName'] = "T05"
	g.attrs['Date'] = "2010-11-01T01:00:00TZD"
	dset = g.create_dataset("Latitudes", data=lat, dtype=F_TYPE)
	dset = g.create_dataset("Longitudes", data=lon, dtype=F_TYPE)
	dset = g.create_dataset("FieldIntensity", data=fi, dtype=F_TYPE)
	dset = g.create_dataset("GSM_X", data=x, dtype=F_TYPE)
	dset = g.create_dataset("GSM_Y", data=y, dtype=F_TYPE)
	dset = g.create_dataset("GSM_Z", data=z, dtype=F_TYPE)
	f.close()
	end = tm.time()
	return end - start


def writeCompressed(scaleoffset = None):
	start = tm.time()
	f = h5py.File(GLOBAL_FN, "w")
	g = f.create_group('OutputFile')
	g.attrs['ExternalFieldModelName'] = "T05"
	g.attrs['Date'] = "2010-11-01T01:00:00TZD"
	if scaleoffset != None:
		dset = g.create_dataset("Latitudes", data=lat, dtype=F_TYPE, compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True )
		dset = g.create_dataset("Longitudes", data=lon, dtype=F_TYPE, compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
		dset = g.create_dataset("FieldIntensity", data=fi, dtype=F_TYPE, compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
		dset = g.create_dataset("GSM_X", data=x, dtype=F_TYPE, compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
		dset = g.create_dataset("GSM_Y", data=y, dtype=F_TYPE, compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
		dset = g.create_dataset("GSM_Z", data=z, dtype=F_TYPE, compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
	else:
		dset = g.create_dataset("Latitudes", data=lat, dtype=F_TYPE, compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("Longitudes", data=lon, dtype=F_TYPE, compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("FieldIntensity", data=fi, dtype=F_TYPE, compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("GSM_X", data=x, dtype=F_TYPE, compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("GSM_Y", data=y, dtype=F_TYPE, compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("GSM_Z", data=z, dtype=F_TYPE, compression="gzip", compression_opts=9, shuffle = True)
	f.close()
	end = tm.time()
	return end - start

def read():
	start = tm.time()
	f = h5py.File(GLOBAL_FN, "r")
	oFile = f.get('OutputFile')
	fieldModel = oFile.attrs['ExternalFieldModelName']
	date = oFile.attrs['Date']
	lat = np.array(oFile.get("Latitudes"))
	lon = np.array(oFile.get("Longitudes"))
	fi = np.array(oFile.get("FieldIntensity"))
	x = np.array(oFile.get("GSM_X"))
	y = np.array(oFile.get("GSM_Y"))
	z = np.array(oFile.get("GSM_Z"))
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
