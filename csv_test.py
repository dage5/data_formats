import csv
import pandas as pd 
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess

sz = 181*361#1000000

lat = list(np.arange(-90,91,1,dtype=np.float32)) * 361
lon = list(np.arange(0,361,1,dtype=np.float32)) * 181
fi = list((np.array(np.random.uniform(size=sz),dtype=np.float64)))#,2))
x = list((np.array(np.random.uniform(size=sz),dtype=np.float64)))
y = list((np.array(np.random.uniform(size=sz),dtype=np.float64)))
z = list((np.array(np.random.uniform(size=sz),dtype=np.float64)))

csv_columns = ['Latitudes','Longitudes','FieldIntensity','GSM_X','GSM_Y','GSM_Z']
def getS(specialCompress = None):
    filename = "test.csv"
    if specialCompress != None:
        filename = specialCompress
    return (os.path.getsize(filename))/1000
def writeCSVcompressed():
    start = tm.time()
    outfile = dict()
    #outfile['ExternalFieldModelName'] = "T05"
    #outfile['Date'] = "2010-11-01T01:00:00TZD"
    outfile['Latitudes'] = lat
    outfile['Longitudes'] = lon
    outfile['FieldIntensity'] = fi
    outfile['GSM_X'] = x
    outfile['GSM_Y'] = y
    outfile['GSM_Z'] = z
    #print(outfile)
    df = pd.DataFrame(data=outfile)
    df.to_csv("test.csv",index=False,float_format="%.2f")
    end = tm.time()
    print("Compressed:", getS(), "Time:", end-start, "size", sz)
    return end - start
def writeCSVuncompressed():
    start = tm.time()
    outfile = dict()
    #outfile['ExternalFieldModelName'] = "T05"
    #outfile['Date'] = "2010-11-01T01:00:00TZD"
    outfile['Latitudes'] = lat
    outfile['Longitudes'] = lon
    outfile['FieldIntensity'] = fi
    outfile['GSM_X'] = x
    outfile['GSM_Y'] = y
    outfile['GSM_Z'] = z
    #print(outfile)
    df = pd.DataFrame(data=outfile)
    df.to_csv("test.csv",index=False)
    end = tm.time()
    print("Uncompressed:", getS(), "Time:", end-start, "size", sz)
    return end - start

def read(compressed):
    start = tm.time()
    csvFile = pd.read_csv('test.csv')
    lat = csvFile['Latitudes'].values
    lon = csvFile['Longitudes'].values
    fi = csvFile['FieldIntensity'].values
    x = csvFile['GSM_X'].values
    y = csvFile['GSM_Y'].values
    z = csvFile['GSM_Z'].values
    end = tm.time()
    print("Reading time "+compressed+":", end-start, "size", sz)
    return end - start


def extraCompression():
    start = tm.time()
    p = subprocess.run(["zip", "-o", "csv.zip","./test.csv", "-9"])
    end = tm.time()
    print("Extra compression:", getS("csv.zip"), "Time:", end-start, "size", sz)
    return end - start

def extraCompressedRead(compressed):
    start = tm.time()
    p = subprocess.run(["unzip", "csv.zip"])
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


test(writeCSVuncompressed)
test(read,"uncompressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")

test(writeCSVcompressed)
test(read,"compressed")

test(extraCompression)
test(extraCompressedRead,"extra compressed")

#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
