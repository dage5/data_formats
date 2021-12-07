import os
import numpy as np
import time as tm
import subprocess
import datetime as dt
import ctypes

def getS(filename):
	if filename == None:
		return ""
	return (os.path.getsize(filename))/1000

def extraCompression(inputFN, zipFN):
	start = tm.time()
	p = subprocess.run(["zip", "-o", "-q", zipFN, inputFN, "-9"])
	end = tm.time()
	return end - start

def extraCompressedRead(inputFN, zipFN):
	start = tm.time()
	p = subprocess.run(["unzip", "-o", "-q", zipFN])
	end = tm.time()
	return end - start

def formatter(seconds):
	out = ""
	sec = np.floor(seconds)
	ms = (seconds - sec) * 1000
	if(sec > 0):
		out = str(sec) + " s " + "{:.2f}".format(ms) + " ms"
	else:
		out = "{:.2f}".format(ms) + " ms"
	return out

def test(func, testName, filename = None):
	time = 0
	times = []
	for i in range(0,10):
		ret = func()
		time = time + ret
		times.append(ret)
	minimum = min(times)
	maximum = max(times)
	time = time - minimum - maximum
	i = i+1#range 0 to 10 ends with 9 but there are 10 iterations
	print("Test:",testName,"has AVGtime:", formatter(time / (i-2)), "size:", getS(filename), "k bytes")
	
def loadData():
	arrayData = {"rig":[],"v":[],"rad":[],"eth":[],"efi":[],"ath":[],"afi":[],"time":[],"length":[]}
	globalData = {"arr_len": 0, "lcr": 0, "ucr": 0, "ecr": 0, "extern_field": None, "geo_lat": None,"geo_lon": None, "geo_rad": None, "loc_lat": None, "loc_lon": None, "datetime": None, "starting_rig": None, "rig_step": None, "step_limit": None}
	with open("outfil_0", "r") as f:
		lines = f.readlines()
		numberOfLines = len(lines)
		globalData["arr_len"] = numberOfLines - (12 + 3)
		bodyCutoff = (numberOfLines - 3)
		footerLine = (numberOfLines - 2)
		for i in range(0, numberOfLines):
			if i < 12:
				#print(lines[i])
				if i == 4:
					globalData["extern_field"] = lines[i].split()[5]
				if i == 5:
					globalData["geo_lat"] = float(lines[i].split()[3])
					globalData["geo_lon"] = float(lines[i].split()[6])
					globalData["geo_rad"] = float(lines[i].split()[10])
				if i == 6:
					globalData["loc_lat"] = float(lines[i].split()[5])
					globalData["loc_lon"] = float(lines[i].split()[8])
				if i == 7:
					sp = lines[i].split()
					(year, month, day, hour, minute, second) = [int(i) for i in (sp[1], sp[2], sp[3], sp[5], sp[7], sp[9])]
					datetime = dt.datetime(year, month, day, hour, minute, second)
					globalData["datetime"] = datetime
				if i == 8:
					globalData["starting_rig"] = float(lines[i].split()[3])
					globalData["rig_step"] = float(lines[i].split()[6])
				if i == 9:
					globalData["step_limit"] = int(lines[i].split()[7])
				#print(outData)
			elif i < bodyCutoff:
				(rig,v,rad,eth,efi,ath,afi,time,length) = [float(i) for i in lines[i].split()]
				arrayData["rig"].append(rig)
				arrayData["v"].append(v)
				arrayData["rad"].append(rad)
				arrayData["eth"].append(eth)
				arrayData["efi"].append(efi)
				arrayData["ath"].append(ath)
				arrayData["afi"].append(afi)
				arrayData["time"].append(time)
				arrayData["length"].append(length)
			elif i == footerLine:
				(lcr, ucr, ecr) = [float(i) for i in lines[i].split()]
				globalData["lcr"] = (lcr)
				globalData["ucr"] = (ucr)
				globalData["ecr"] = (ecr)
	#print(outData["rig"])
	return (globalData, arrayData)
if __name__ == "__main__":
	loadData()
	







