import json
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import math
import subprocess

sz = 181*361#1000000


lat = list(np.round(np.arange(-90,91,1,dtype=np.float64),16)) * 361
lon = list(np.round(np.arange(0,361,1,dtype=np.float64),16)) * 181
fi = list(np.random.uniform(size=sz))
x = list(np.random.uniform(size=sz))
y = list(np.random.uniform(size=sz))
z = list(np.random.uniform(size=sz))
latC = list(np.round(lat,2))
lonC = list(np.round(lon,2))
fiC = list(np.round(fi,2))
xC = list(np.round(x,2))
yC = list(np.round(y,2))
zC = list(np.round(z,2))

def init():
    global lat,lon,fi,x,y,z
    lat = (list(np.round(np.arange(-90,91,1,dtype=np.float64),16)) * 361)
    lon = (list(np.round(np.arange(0,361,1,dtype=np.float64),16)) * 181)
    fi = list(np.random.uniform(size=sz))
    x = list(np.random.uniform(size=sz))
    y = list(np.random.uniform(size=sz))
    z = list(np.random.uniform(size=sz))
    
def compress():
    global latC,lonC,fiC,xC,yC,zC
    latC = list(np.round(lat,2))#[ round(elem, 2) for elem in lat ]
    lonC = list(np.round(lon,2))#[ round(elem, 2) for elem in lon ]
    fiC = list(np.round(fi,2))#[ round(elem, 2) for elem in fi ]
    xC = list(np.round(x,2))#[ round(elem, 2) for elem in x ]
    yC = list(np.round(y,2))#[ round(elem, 2) for elem in y ]
    zC = list(np.round(z,2))#[ round(elem, 2) for elem in z ]

def getS(specialCompress = None):
    filename = "test.json"
    if specialCompress != None:
        filename = specialCompress
    return (os.path.getsize(filename))/1000
def writeJsonCompressed():
    init()
    start = tm.time()
    compress()
    outfile = dict()
    outfile['ExternalFieldModelName'] = "T05"
    outfile['Date'] = "2010-11-01T01:00:00TZD"
    outfile['Latitudes'] = latC
    outfile['Longitudes'] = lonC
    outfile['FieldIntensity'] = fiC
    outfile['GSM_X'] = xC
    outfile['GSM_Y'] = yC
    outfile['GSM_Z'] = zC
    ofile = json.dumps(outfile, separators=(',', ':'))
    f = open("test.json", "w")
    f.write(ofile)
    f.close()
    end = tm.time()
    print("Compressed:", getS(), "Time:", end-start, "size", sz)
    return end - start

def writeJsonPretty():
    init()
    start = tm.time()
    outfile = dict()
    outfile['ExternalFieldModelName'] = "T05"
    outfile['Date'] = "2010-11-01T01:00:00TZD"
    outfile['Latitudes'] = lat
    outfile['Longitudes'] = lon
    outfile['FieldIntensity'] = fi
    outfile['GSM_X'] = x
    outfile['GSM_Y'] = y
    outfile['GSM_Z'] = z
    ofile = json.dumps(outfile)
    f = open("test.json", "w")
    f.write(ofile)
    f.close()
    end = tm.time()
    print("Uncompressed:", getS(), "Time:", end-start, "size", sz)
    return end - start

def readJson(compressed):
    start = tm.time()
    f = open("test.json", "r")
    outfile = json.loads(f.read())
    fieldModel = outfile['ExternalFieldModelName']
    date = outfile['Date']
    lat = np.array(outfile["Latitudes"])
    lon = np.array(outfile["Longitudes"])
    fi = np.array(outfile["FieldIntensity"])
    x = np.array(outfile["GSM_X"])
    y = np.array(outfile["GSM_Y"])
    z = np.array(outfile["GSM_Z"])
    end = tm.time()
    print("Reading time "+compressed+":", end-start, "size", sz)
    return end - start
def extraCompression():
    start = tm.time()
    p = subprocess.run(["zip", "-o", "json.zip","./test.json", "-9"])
    end = tm.time()
    print("Extra compression:", getS("json.zip"), "Time:", end-start, "size", sz)
    return end - start

def extraCompressedRead(compressed):
    start = tm.time()
    p = subprocess.run(["unzip", "json.zip"])
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

   
test(writeJsonPretty)
test(readJson,"uncompressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")

test(writeJsonCompressed)
test(readJson,"compressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")

#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
