import cdflib
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://github.com/MAVENSDC/cdflib
sz = 181*361#1000000

lat = list(np.arange(-90,91,1,dtype=np.float64)) * 361
lon = list(np.arange(0,361,1,dtype=np.float64)) * 181
fi = np.random.uniform(size=sz)
x = np.random.uniform(size=sz)
y = np.random.uniform(size=sz)
z = np.random.uniform(size=sz)

GLOBAL_FN = "test.cdf"
GLOBAL_ZIP_NAME = "cdf.zip"

settings = dict()
def writeUncompressed():
	start = tm.time()
	settings['Compressed'] = 0
	cdf_file = cdflib.cdfwrite.CDF(GLOBAL_FN, cdf_spec=settings,delete=True)
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
	#print("Uncompressed:", getS(), "Time:", end-start, "size", sz)
	return end - start

def writeCompressed():
	start = tm.time()
	settings['Compressed'] = 9
	cdf_file = cdflib.cdfwrite.CDF(GLOBAL_FN, cdf_spec=settings,delete=True)
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
	#print("Compressed:", getS(), "Time:", end-start, "size", sz)
	return end - start
def read():
	start = tm.time()
	cdf_file = cdflib.cdfread.CDF(GLOBAL_FN)
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
	#print("Reading time "+compressed+":", end-start, "size", sz)
	return end - start

cn.test(writeUncompressed, "uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r")

cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")

cn.test(writeCompressed, "compressed w", GLOBAL_FN)
cn.test(lambda: read(), "compressed r")

cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip lossy compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip lossy compressed r")


#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
