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
	dset = g.create_dataset("Latitudes", data=lat, dtype='float32')
	dset = g.create_dataset("Longitudes", data=lon, dtype='float32')
	dset = g.create_dataset("FieldIntensity", data=fi, dtype='float32')
	dset = g.create_dataset("GSM_X", data=x, dtype='float32')
	dset = g.create_dataset("GSM_Y", data=y, dtype='float32')
	dset = g.create_dataset("GSM_Z", data=z, dtype='float32')
	f.close()
	end = tm.time()
	#print("Uncompressed:", getS(), "Time:", end-start, "size", sz)
	return end - start


def writeCompressed(scaleoffset = None):
	start = tm.time()
	f = h5py.File(GLOBAL_FN, "w")
	g = f.create_group('OutputFile')
	g.attrs['ExternalFieldModelName'] = "T05"
	g.attrs['Date'] = "2010-11-01T01:00:00TZD"
	if scaleoffset != None:
		dset = g.create_dataset("Latitudes", data=lat, dtype='float32', compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True )
		dset = g.create_dataset("Longitudes", data=lon, dtype='float32', compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
		dset = g.create_dataset("FieldIntensity", data=fi, dtype='float32', compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
		dset = g.create_dataset("GSM_X", data=x, dtype='float32', compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
		dset = g.create_dataset("GSM_Y", data=y, dtype='float32', compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
		dset = g.create_dataset("GSM_Z", data=z, dtype='float32', compression="gzip", compression_opts=9, scaleoffset = scaleoffset, shuffle = True)
	else:
		dset = g.create_dataset("Latitudes", data=lat, dtype='float32', compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("Longitudes", data=lon, dtype='float32', compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("FieldIntensity", data=fi, dtype='float32', compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("GSM_X", data=x, dtype='float32', compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("GSM_Y", data=y, dtype='float32', compression="gzip", compression_opts=9, shuffle = True)
		dset = g.create_dataset("GSM_Z", data=z, dtype='float32', compression="gzip", compression_opts=9, shuffle = True)
	f.close()
	end = tm.time()
	#print("Compressed: ", getS(), "Time:", end-start, "size", sz)
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
	#print("Reading time "+compressed+":", end-start, "size", sz)
	return end - start

#############################
"""def getS(specialCompress = None):
	filename = "mytestfile.hdf5"
	if specialCompress != None:
		filename = specialCompress
	return (os.path.getsize(filename))/1000
def extraCompression():
	start = tm.time()
	p = subprocess.run(["zip", "-o", "-q", "hdf.zip","./mytestfile.hdf5", "-9"])
	end = tm.time()
	#print("Extra compression:", getS("hdf.zip"), "Time:", end-start, "size", sz)
	return end - start

def extraCompressedRead(compressed):
	start = tm.time()
	p = subprocess.run(["unzip", "-o", "-q", "hdf.zip"])
	end = tm.time()
	#print("Reading time "+compressed+":", end-start, "size", sz)
	return end - start
def formatter(seconds):
	sec = np.floor(seconds)
	ms = (seconds - sec) * 1000
	return str(sec) + " s " + str(ms) + " ms"
def test(func, param = 0):
	time = 0
	times = []
	for i in range(0,10):
		if param == 0:
			ret = func()
		else:
			ret = func(param)
		time = time + ret
		times.append(ret)
	minimum = min(times)
	maximum = max(times)
	time = time - minimum - maximum
	i = i+1#range 0 to 10 ends with 9 but there are 10 iterations
	print(str(param),"AVG:", formatter(time / (i-2)), time / (i-2))
"""
"""
test(writeUncompressed)
test(read,"uncompressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")

test(writeCompressed)
test(read,"compressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")

test(writeCompressed, 2)
test(read,"lossy extra compressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")"""

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
