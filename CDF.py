import cdflib
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
#https://github.com/MAVENSDC/cdflib
sz = 181*361#1000000

lat = list(np.arange(-90,91,1,dtype=np.float64)) * 361
lon = list(np.arange(0,361,1,dtype=np.float64)) * 181
fi = np.random.uniform(size=sz)
x = np.random.uniform(size=sz)
y = np.random.uniform(size=sz)
z = np.random.uniform(size=sz)

settings = dict()
def getS(specialCompress = None):
    filename = "test.cdf"
    if specialCompress != None:
        filename = specialCompress
    return (os.path.getsize(filename))/1000
def writeUncompressed():
    start = tm.time()
    settings['Compressed'] = 0
    cdf_file = cdflib.cdfwrite.CDF('test.cdf', cdf_spec=settings,delete=True)
    globalAttrs={}
    globalAttrs['ExternalFieldModelName']={0: 'T05'}
    globalAttrs['Date']={0: '2010-11-01T01:00:00TZD'}
    cdf_file.write_globalattrs(globalAttrs)
    varinfo = {}
    varinfo["Variable"] = "Latitudes"
    varinfo["Data_Type"] = cdflib.cdfwrite.CDF.CDF_REAL4 #'CDF_FLOAT'
    varinfo["Num_Elements"] = 1
    varinfo["Rec_Vary"] = 0
    varinfo["Dim_Sizes"] = [sz]
    varinfo["Compress"] = 0
    cdf_file.write_var(varinfo, var_data=lat )
    varinfo["Variable"] = "Longitudes"
    cdf_file.write_var(varinfo, var_data=lon )
    varinfo["Variable"] = "FieldIntensity"
    cdf_file.write_var(varinfo, var_data=fi )
    varinfo["Variable"] = "GSM_X"
    cdf_file.write_var(varinfo, var_data=x )
    varinfo["Variable"] = "GSM_Y"
    cdf_file.write_var(varinfo, var_data=y )
    varinfo["Variable"] = "GSM_Z"
    cdf_file.write_var(varinfo, var_data=z )
    cdf_file.close()
    end = tm.time()
    print("Uncompressed:", getS(), "Time:", end-start, "size", sz)
    return end - start

def writeCompressed():
    start = tm.time()
    settings['Compressed'] = 9
    cdf_file = cdflib.cdfwrite.CDF('test.cdf', cdf_spec=settings,delete=True)
    globalAttrs={}
    globalAttrs['ExternalFieldModelName']={0: 'T05'}
    globalAttrs['Date']={0: '2010-11-01T01:00:00TZD'}
    cdf_file.write_globalattrs(globalAttrs)
    varinfo = {}
    varinfo["Variable"] = "Latitudes"
    varinfo["Data_Type"] = cdflib.cdfwrite.CDF.CDF_REAL4 #'CDF_FLOAT'
    varinfo["Num_Elements"] = 1
    varinfo["Rec_Vary"] = 0
    varinfo["Dim_Sizes"] = [sz]
    varinfo["Compress"] = 9
    cdf_file.write_var(varinfo, var_data=lat )
    varinfo["Variable"] = "Longitudes"
    cdf_file.write_var(varinfo, var_data=lon )
    varinfo["Variable"] = "FieldIntensity"
    cdf_file.write_var(varinfo, var_data=fi )
    varinfo["Variable"] = "GSM_X"
    cdf_file.write_var(varinfo, var_data=x )
    varinfo["Variable"] = "GSM_Y"
    cdf_file.write_var(varinfo, var_data=y )
    varinfo["Variable"] = "GSM_Z"
    cdf_file.write_var(varinfo, var_data=z )
    cdf_file.close()
    end = tm.time()
    print("Compressed:", getS(), "Time:", end-start, "size", sz)
    return end - start
def read(compressed):
    start = tm.time()
    cdf_file = cdflib.cdfread.CDF('test.cdf')
    attrs = cdf_file.globalattsget()
    fieldModel = attrs['ExternalFieldModelName']
    date = attrs['Date']
    #print(fieldModel, date)
    lat = cdf_file.varget("Latitudes")
    lon = cdf_file.varget("Longitudes")
    fi = cdf_file.varget("FieldIntensity")
    x = cdf_file.varget("GSM_X")
    y = cdf_file.varget("GSM_Y")
    z = cdf_file.varget("GSM_Z")
    cdf_file.close()
    end = tm.time()
    print("Reading time "+compressed+":", end-start, "size", sz)
    return end - start


def extraCompression():
    start = tm.time()
    p = subprocess.run(["zip", "-o", "cdf.zip","./test.cdf", "-9"])
    end = tm.time()
    print("Extra compression:", getS("cdf.zip"), "Time:", end-start, "size", sz)
    return end - start

def extraCompressedRead(compressed):
    start = tm.time()
    p = subprocess.run(["unzip", "cdf.zip"])
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

#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
