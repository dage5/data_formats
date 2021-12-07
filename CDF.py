import cdflib
import numpy as np
import os
import time as tm
from hurry.filesize import size, si
import subprocess
import common as cn
#https://github.com/MAVENSDC/cdflib
"""sz = 181*361#1000000

lat = list(np.arange(-90,91,1,dtype=np.float64)) * 361
lon = list(np.arange(0,361,1,dtype=np.float64)) * 181
fi = np.random.uniform(size=sz)
x = np.random.uniform(size=sz)
y = np.random.uniform(size=sz)
z = np.random.uniform(size=sz)"""

GLOBAL_FN = "test.cdf"
GLOBAL_ZIP_NAME = "cdf.zip"

(gData, aData) = cn.loadData()
sz = gData["arr_len"]
#{"arr_len": 0", rig":[],"v":[],"rad":[],"eth":[],"efi":[],"ath":[],"afi":[],"time":[],"length":[], "lcr": 0, "ucr": 0, "ecr": 0, "extern_field": None, "geo_lat": None,"geo_lon": None, "geo_rad": None, "loc_lat": None, "loc_lon": None, "datetime": None, "starting_rig": None, "rig_step": None, "step_limit": None}

settings = dict()
def writeUncompressed():
	start = tm.time()
	settings['Compressed'] = 0
	cdf_file = cdflib.cdfwrite.CDF(GLOBAL_FN, cdf_spec=settings,delete=True)
	#####
	globalAttrs={}
	globalAttrs['extern_field']={0: gData["extern_field"]}
	globalAttrs['datetime']={0: gData["datetime"].isoformat()}
	globalAttrs['arr_len']={0: gData["arr_len"]}
	globalAttrs['lcr']={0: gData["lcr"]}
	globalAttrs['ucr']={0: gData["ucr"]}
	globalAttrs['ecr']={0: gData["ecr"]}
	globalAttrs['geo_lat']={0: gData["geo_lat"]}
	globalAttrs['geo_lon']={0: gData["geo_lon"]}
	globalAttrs['geo_rad']={0: gData["geo_rad"]}
	globalAttrs['loc_lat']={0: gData["loc_lat"]}
	globalAttrs['loc_lon']={0: gData["loc_lon"]}
	globalAttrs['starting_rig']={0: gData["starting_rig"]}
	globalAttrs['rig_step']={0: gData["rig_step"]}
	globalAttrs['step_limit']={0: gData["step_limit"]}
	#######
	cdf_file.write_globalattrs(globalAttrs)
	varinfo = {}
	varinfo["Variable"] = "rig"
	varinfo["Data_Type"] = cdflib.cdfwrite.CDF.CDF_REAL8 #'CDF_FLOAT'
	varinfo["Num_Elements"] = 1
	varinfo["Rec_Vary"] = 0
	varinfo["Dim_Sizes"] = [sz]
	varinfo["Compress"] = 0
	cdf_file.write_var(varinfo, var_data=aData["rig"])
	varinfo["Variable"] = "v"
	cdf_file.write_var(varinfo, var_data=aData["v"] )
	varinfo["Variable"] = "rad"
	cdf_file.write_var(varinfo, var_data=aData["rad"] )
	varinfo["Variable"] = "eth"
	cdf_file.write_var(varinfo, var_data=aData["eth"])
	varinfo["Variable"] = "efi"
	cdf_file.write_var(varinfo, var_data=aData["efi"])
	varinfo["Variable"] = "ath"
	cdf_file.write_var(varinfo, var_data=aData["ath"])
	varinfo["Variable"] = "afi"
	cdf_file.write_var(varinfo, var_data=aData["afi"])
	varinfo["Variable"] = "time"
	cdf_file.write_var(varinfo, var_data=aData["time"])
	varinfo["Variable"] = "length"
	cdf_file.write_var(varinfo, var_data=aData["length"])
	cdf_file.close()
	end = tm.time()
	#print("Uncompressed:", getS(), "Time:", end-start, "size", sz)
	return end - start

def writeCompressed():
	start = tm.time()
	settings['Compressed'] = 9
	cdf_file = cdflib.cdfwrite.CDF(GLOBAL_FN, cdf_spec=settings,delete=True)
	#####
	globalAttrs={}
	globalAttrs['extern_field']={0: gData["extern_field"]}
	globalAttrs['datetime']={0: gData["datetime"].isoformat()}
	globalAttrs['arr_len']={0: gData["arr_len"]}
	globalAttrs['lcr']={0: gData["lcr"]}
	globalAttrs['ucr']={0: gData["ucr"]}
	globalAttrs['ecr']={0: gData["ecr"]}
	globalAttrs['geo_lat']={0: gData["geo_lat"]}
	globalAttrs['geo_lon']={0: gData["geo_lon"]}
	globalAttrs['geo_rad']={0: gData["geo_rad"]}
	globalAttrs['loc_lat']={0: gData["loc_lat"]}
	globalAttrs['loc_lon']={0: gData["loc_lon"]}
	globalAttrs['starting_rig']={0: gData["starting_rig"]}
	globalAttrs['rig_step']={0: gData["rig_step"]}
	globalAttrs['step_limit']={0: gData["step_limit"]}
	#######
	cdf_file.write_globalattrs(globalAttrs)
	varinfo = {}
	varinfo["Variable"] = "rig"
	varinfo["Data_Type"] = cdflib.cdfwrite.CDF.CDF_REAL8 #'CDF_FLOAT'
	varinfo["Num_Elements"] = 1
	varinfo["Rec_Vary"] = 0
	varinfo["Dim_Sizes"] = [sz]
	varinfo["Compress"] = 9
	cdf_file.write_var(varinfo, var_data=aData["rig"])
	varinfo["Variable"] = "v"
	cdf_file.write_var(varinfo, var_data=aData["v"] )
	varinfo["Variable"] = "rad"
	cdf_file.write_var(varinfo, var_data=aData["rad"] )
	varinfo["Variable"] = "eth"
	cdf_file.write_var(varinfo, var_data=aData["eth"])
	varinfo["Variable"] = "efi"
	cdf_file.write_var(varinfo, var_data=aData["efi"])
	varinfo["Variable"] = "ath"
	cdf_file.write_var(varinfo, var_data=aData["ath"])
	varinfo["Variable"] = "afi"
	cdf_file.write_var(varinfo, var_data=aData["afi"])
	varinfo["Variable"] = "time"
	cdf_file.write_var(varinfo, var_data=aData["time"])
	varinfo["Variable"] = "length"
	cdf_file.write_var(varinfo, var_data=aData["length"])
	cdf_file.close()
	end = tm.time()
	#print("Compressed:", getS(), "Time:", end-start, "size", sz)
	return end - start
def read():
	start = tm.time()
	cdf_file = cdflib.cdfread.CDF(GLOBAL_FN)
	attrs = cdf_file.globalattsget()
	###
	arrayData = {"rig":[],"v":[],"rad":[],"eth":[],"efi":[],"ath":[],"afi":[],"time":[],"length":[]}
	globalData = {"arr_len": 0, "lcr": 0, "ucr": 0, "ecr": 0, "extern_field": None, "geo_lat": None,"geo_lon": None, "geo_rad": None, "loc_lat": None, "loc_lon": None, "datetime": None, "starting_rig": None, "rig_step": None, "step_limit": None}
	##
	globalData["arr_len"] = attrs['arr_len']
	globalData["lcr"] = attrs['lcr']
	globalData["ucr"] = attrs['ucr']
	globalData["ecr"] = attrs['ecr']
	globalData["extern_field"] = attrs['extern_field']
	globalData["geo_lat"] = attrs['geo_lat']
	globalData["geo_lon"] = attrs['geo_lon']
	globalData["geo_rad"] = attrs['geo_rad']
	globalData["loc_lat"] = attrs['loc_lat']
	globalData["loc_lon"] = attrs['loc_lon']
	globalData["datetime"] = attrs['datetime']
	globalData["starting_rig"] = attrs['starting_rig']
	globalData["rig_step"] = attrs['rig_step']
	globalData["step_limit"] = attrs['step_limit']

	arrayData["rig"] = cdf_file.varget("rig")
	arrayData["v"] = cdf_file.varget("v")
	arrayData["rad"] = cdf_file.varget("rad")
	arrayData["eth"] = cdf_file.varget("eth")
	arrayData["efi"] = cdf_file.varget("efi")
	arrayData["ath"] = cdf_file.varget("ath")
	arrayData["afi"] = cdf_file.varget("afi")
	arrayData["time"] = cdf_file.varget("time")
	arrayData["length"] = cdf_file.varget("length")
	#print(arrayData["rig"])
	cdf_file.close()
	end = tm.time()
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
