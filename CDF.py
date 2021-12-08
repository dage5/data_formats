import cdflib
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://github.com/MAVENSDC/cdflib

GLOBAL_FN = "test.cdf"
GLOBAL_ZIP_NAME = "cdf.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]

settings = dict()
def writeUncompressed():
	start = tm.time()
	settings['Compressed'] = 0
	cdf_file = cdflib.cdfwrite.CDF(GLOBAL_FN, cdf_spec=settings,delete=True)
	globalAttrs={}
	for attrData in gData:
		globalAttrs[attrData] = {0: gData[attrData]}
	cdf_file.write_globalattrs(globalAttrs)
	varinfo = {}
	varinfo["Data_Type"] = cdflib.cdfwrite.CDF.CDF_REAL8 #'CDF_FLOAT'
	varinfo["Num_Elements"] = 1
	varinfo["Rec_Vary"] = 0
	varinfo["Dim_Sizes"] = [sz]
	varinfo["Compress"] = 0
	for attrData in aData:
		varinfo["Variable"] = attrData
		cdf_file.write_var(varinfo, var_data=aData[attrData])
	
	cdf_file.close()
	end = tm.time()
	return end - start

def writeCompressed():
	start = tm.time()
	settings['Compressed'] = 9
	cdf_file = cdflib.cdfwrite.CDF(GLOBAL_FN, cdf_spec=settings,delete=True)
	globalAttrs={}
	for attrData in gData:
		globalAttrs[attrData] = {0: gData[attrData]}
	cdf_file.write_globalattrs(globalAttrs)
	varinfo = {}
	varinfo["Data_Type"] = cdflib.cdfwrite.CDF.CDF_REAL8
	varinfo["Num_Elements"] = 1
	varinfo["Rec_Vary"] = 0
	varinfo["Dim_Sizes"] = [sz]
	varinfo["Compress"] = 9
	for attrData in aData:
		varinfo["Variable"] = attrData
		cdf_file.write_var(varinfo, var_data=aData[attrData])
	
	cdf_file.close()
	end = tm.time()
	return end - start
def read():
	start = tm.time()
	cdf_file = cdflib.cdfread.CDF(GLOBAL_FN)
	attrs = cdf_file.globalattsget()
	arrData = {"rig":[],"v":[],"rad":[],"eth":[],"efi":[],"ath":[],"afi":[],"time":[],"length":[]}
	globData = {"arr_len": 0, "lcr": 0, "ucr": 0, "ecr": 0, "extern_field": None, "geo_lat": None,"geo_lon": None, "geo_rad": None, "loc_lat": None, "loc_lon": None, "datetime": None, "starting_rig": None, "rig_step": None, "step_limit": None}
	
	for arrayData in arrData:
		arrData[arrayData] = cdf_file.varget(arrayData)
	
	for attrData in globData:
		globData[attrData] = attrs[attrData]
	
	cdf_file.close()
	end = tm.time()
	return end - start

cn.test(writeUncompressed, "uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r")

cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")

cn.test(writeCompressed, "compressed w", GLOBAL_FN)
cn.test(lambda: read(), "compressed r")

cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")


#print(lat)
#print(lon)
#print(fi)
#print(x)
#print(y)
#print(z)
