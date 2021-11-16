import msgpack
import numpy as np
import os
import time as tm
from hurry.filesize import size, si

sz = 181*361#1000000

lat = list(np.arange(-90,91,1,dtype=np.float64)) * 361
lon = list(np.arange(0,361,1,dtype=np.float64)) * 181
fi = list(np.random.uniform(size=sz))
x = list(np.random.uniform(size=sz))
y = list(np.random.uniform(size=sz))
z = list(np.random.uniform(size=sz))
#print(lat)
def getS():
    return (os.path.getsize("msg.pack"))/1000
def writeMsgPack():
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
    ofile = msgpack.packb(outfile, use_bin_type=True)
    f = open("msg.pack", "w+b")
    f.write(ofile)
    f.close()
    end = tm.time()
    print("Uncompressed:", getS(), "Time:", end-start, "size", sz)
    return end - start
def writeMsgPackCompressed():
    start = tm.time()
    outfile = dict()
    outfile['ExternalFieldModelName'] = "T05"
    outfile['Date'] = "2010-11-01T01:00:00TZD"
    outfile['Latitudes'] = list(np.round(lat,2))
    outfile['Longitudes'] = list(np.round(lon,2))
    outfile['FieldIntensity'] = list(np.round(fi,2))
    outfile['GSM_X'] = list(np.round(x,2))
    outfile['GSM_Y'] = list(np.round(y,2))
    outfile['GSM_Z'] = list(np.round(z,2))
    ofile = msgpack.packb(outfile, use_bin_type=True)
    f = open("msg.pack", "w+b")
    f.write(ofile)
    f.close()
    end = tm.time()
    print("Compressed:", getS(), "Time:", end-start, "size", sz)
    return end - start

def read(com):
    start = tm.time()
    f = open("msg.pack", "r+b")
    ofile = msgpack.unpackb(f.read())
    f.close()
    end = tm.time()
    print(com+":", getS(), "Time:", end-start, "size", sz)
    return end - start
    #print(ofile)
 
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


    
test(writeMsgPack)
test(read,"Uncompressed")
#test(writeMsgPackCompressed)
#test(read,"Compressed")
#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
