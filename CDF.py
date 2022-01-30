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

GLOBAL_FN_SMALL = "small.cdf"
GLOBAL_ZIP_NAME_SMALL = "cdf_small.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]

SMALL_FILE_SIZE = 65160
(globalData, arrayData) = cn.generateSFvalues(SMALL_FILE_SIZE)

settings = dict()

def writeSmall(compressionLvl):
	cn.rmAny(GLOBAL_FN_SMALL)
	start = tm.time()
	settings['Compressed'] = compressionLvl
	cdf_file = cdflib.cdfwrite.CDF(GLOBAL_FN_SMALL, cdf_spec=settings,delete=True)
	globalAttrs={}
	for attrData in globalData:
		globalAttrs[attrData] = {0: globalData[attrData]}
	cdf_file.write_globalattrs(globalAttrs)
	varinfo = {}
	varinfo["Data_Type"] = cdflib.cdfwrite.CDF.CDF_REAL8 #'CDF_FLOAT'
	varinfo["Num_Elements"] = 1
	varinfo["Rec_Vary"] = 0
	varinfo["Dim_Sizes"] = [SMALL_FILE_SIZE]
	varinfo["Compress"] = compressionLvl
	for attrData in arrayData:
		varinfo["Variable"] = attrData
		cdf_file.write_var(varinfo, var_data=arrayData[attrData])
	cdf_file.close()
	end = tm.time()
	return end - start

def readSmall():
	start = tm.time()
	cdf_file = cdflib.cdfread.CDF(GLOBAL_FN_SMALL)
	attrs = cdf_file.globalattsget()
	globData = {"len": size}
	arrData = {"intens":[],"lcr":[],"ucr":[],"ecr":[]}
	for arrayData_ in arrData:
		arrData[arrayData_] = cdf_file.varget(arrayData_)
	for attrData_ in globData:
		globData[attrData_] = attrs[attrData_]
	cdf_file.close()
	end = tm.time()
	#print(globData["len"], arrData["intens"])
	return end - start

def write(compressionLvl):
	cn.rmAny(GLOBAL_FN)
	start = tm.time()
	settings['Compressed'] = compressionLvl
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
	varinfo["Compress"] = compressionLvl
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

cn.test(lambda: write(0), "uncompressed w", GLOBAL_FN)
cn.test(lambda: read(), "uncompressed r")

#cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
#cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")

cn.test(lambda: write(9), "compressed w", GLOBAL_FN)
cn.test(lambda: read(), "compressed r")

#cn.test(lambda: cn.extraCompression(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed w", GLOBAL_ZIP_NAME)
#cn.test(lambda: cn.extraCompressedRead(GLOBAL_FN, GLOBAL_ZIP_NAME), "zip compressed r")

cn.test(lambda: writeSmall(0), "uncompressed sf w", GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "uncompressed sf r")

cn.test(lambda: writeSmall(9), "compressed sf w", GLOBAL_FN_SMALL)
cn.test(lambda: readSmall(), "compressed sf r")



