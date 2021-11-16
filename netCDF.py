from netCDF4 import Dataset
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
#https://pyhogs.github.io/intro_netcdf4.html
sz = 181*361#1000000

lat = list(np.arange(-90,91,1,dtype=np.float64)) * 361
lon = list(np.arange(0,361,1,dtype=np.float64)) * 181
fi = np.random.uniform(size=sz)
x = np.random.uniform(size=sz)
y = np.random.uniform(size=sz)
z = np.random.uniform(size=sz)

def getS(specialCompress = None):
    filename = "test.nc"
    if specialCompress != None:
        filename = specialCompress
    return (os.path.getsize(filename))/1000
def writeUncompressed():
    start = tm.time()
    rootgrp = Dataset("test.nc", "w", format="NETCDF4")
    tempgrp = rootgrp.createGroup('OutputFile')
    tempgrp.createDimension('lat', len(lat))
    Latitudes = tempgrp.createVariable('Latitudes', 'f4', 'lat')
    Longitudes = tempgrp.createVariable('Longitudes', 'f4', 'lat')
    FieldIntensity = tempgrp.createVariable('FieldIntensity', 'f4', 'lat')
    GSM_X = tempgrp.createVariable('GSM_X', 'f4', 'lat')
    GSM_Y = tempgrp.createVariable('GSM_Y', 'f4', 'lat')
    GSM_Z = tempgrp.createVariable('GSM_Z', 'f4', 'lat')
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
    print("Uncompressed:", getS(), "Time:", end-start, "size", sz)
    return end - start


def writeCompressed(scaleoffset = None):
    start = tm.time()
    rootgrp = Dataset("test.nc", "w", format="NETCDF4")
    tempgrp = rootgrp.createGroup('OutputFile')
    tempgrp.createDimension('lat', len(lat))
    if scaleoffset != None:
        Latitudes = tempgrp.createVariable('Latitudes', 'f4', 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
        Longitudes = tempgrp.createVariable('Longitudes', 'f4', 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
        FieldIntensity = tempgrp.createVariable('FieldIntensity', 'f4', 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
        GSM_X = tempgrp.createVariable('GSM_X', 'f4', 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
        GSM_Y = tempgrp.createVariable('GSM_Y', 'f4', 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
        GSM_Z = tempgrp.createVariable('GSM_Z', 'f4', 'lat',zlib=True,complevel=9,least_significant_digit=2, shuffle=True)
    else:
        Latitudes = tempgrp.createVariable('Latitudes', 'f4', 'lat',zlib=True,complevel=9, shuffle=True)#,least_significant_digit=2)
        Longitudes = tempgrp.createVariable('Longitudes', 'f4', 'lat',zlib=True,complevel=9, shuffle=True)#,least_significant_digit=2)
        FieldIntensity = tempgrp.createVariable('FieldIntensity', 'f4', 'lat',zlib=True,complevel=9, shuffle=True)#,least_significant_digit=2)
        GSM_X = tempgrp.createVariable('GSM_X', 'f4', 'lat',zlib=True,complevel=9, shuffle=True)#,least_significant_digit=2)
        GSM_Y = tempgrp.createVariable('GSM_Y', 'f4', 'lat',zlib=True,complevel=9, shuffle=True)#,least_significant_digit=2)
        GSM_Z = tempgrp.createVariable('GSM_Z', 'f4', 'lat',zlib=True,complevel=9, shuffle=True)#,least_significant_digit=2)
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
    print("Compressed:", getS(), "Time:", end-start, "size", sz)
    return end - start

def read(compressed):
    start = tm.time()
    rootgrp = Dataset("test.nc", "r")
    tempgrp = rootgrp.groups['OutputFile']
    lat = tempgrp.variables['Latitudes'][:]
    lon = tempgrp.variables['Longitudes'][:]
    fi = tempgrp.variables['FieldIntensity'][:]
    x = tempgrp.variables['GSM_X'][:]
    y = tempgrp.variables['GSM_Y'][:]
    z = tempgrp.variables['GSM_Z'][:]
    date = rootgrp.date
    fieldModel = rootgrp.externalFieldModel
    #print(date,fieldModel)
    rootgrp.close()
    end = tm.time()
    print("Reading time "+compressed+":", end-start, "size", sz)
    return end - start
    #print(x)

def extraCompression():
    start = tm.time()
    p = subprocess.run(["zip", "-o", "nc.zip","./test.nc", "-9"])
    end = tm.time()
    print("Extra compression:", getS("nc.zip"), "Time:", end-start, "size", sz)
    return end - start

def extraCompressedRead(compressed):
    start = tm.time()
    p = subprocess.run(["unzip", "nc.zip"])
    end = tm.time()
    print("Reading time "+compressed+":", end-start, "size", sz)
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
    print("AVG:", formatter(time / (i-2)), time / (i-2))

test(writeUncompressed)
test(read,"uncompressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")

test(writeCompressed)
test(read,"compressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")

test(writeCompressed, 2)
test(read,"lossy compressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")


#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
