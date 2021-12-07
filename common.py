import os
import numpy as np
import time as tm
import subprocess
import datetime as dt

def getS(filename):
	if filename == None:
		return ""
	return (os.path.getsize(filename))/1000

def extraCompression(inputFN, zipFN):
	start = tm.time()
	p = subprocess.run(["zip", "-o", "-q", "nc.zip","./test.nc", "-9"])
	end = tm.time()
	return end - start

def extraCompressedRead(inputFN, zipFN):
	start = tm.time()
	p = subprocess.run(["unzip", "-o", "-q", "nc.zip"])
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
	outData = {"rig":[],"v":[],"rad":[],"eth":[],"efi":[],"ath":[],"afi":[],"time":[],"length":[], "lcr": 0, "ucr": 0, "ecr": 0, "extern_field": None, "geo_lat": None,"geo_lon": None, "geo_rad": None, "loc_lat": None, "loc_lon": None, "datetime": None, "starting_rig": None, "rig_step": None, "step_limit": None}
	with open("outfil_0", "r") as f:
		lines = f.readlines()
		numberOfLines = len(lines)
		bodyCutoff = (numberOfLines - 3)
		footerLine = (numberOfLines - 2)
		for i in range(0, numberOfLines):
			if i < 12:
				#print(lines[i])
				if i == 4:
					outData["extern_field"] = lines[i].split()[5]
				if i == 5:
					outData["geo_lat"] = float(lines[i].split()[3])
					outData["geo_lon"] = float(lines[i].split()[6])
					outData["geo_rad"] = float(lines[i].split()[10])
				if i == 6:
					outData["loc_lat"] = float(lines[i].split()[5])
					outData["loc_lon"] = float(lines[i].split()[8])
				if i == 7:
					sp = lines[i].split()
					(year, month, day, hour, minute, second) = int(sp[1]), int(sp[2]), int(sp[3]), int(sp[5]), int(sp[7]), int(sp[9])
					datetime = dt.datetime(year, month, day, hour, minute, second)
					outData["datetime"] = datetime
				if i == 8:
					outData["starting_rig"] = float(lines[i].split()[3])
					outData["rig_step"] = float(lines[i].split()[6])
				if i == 9:
					outData["step_limit"] = int(lines[i].split()[7])
				#print(outData)
			elif i < bodyCutoff:
				(rig,v,rad,eth,efi,ath,afi,time,length) = lines[i].split()
				outData["rig"].append(rig)
				outData["v"].append(v)
				outData["rad"].append(rad)
				outData["eth"].append(eth)
				outData["efi"].append(efi)
				outData["ath"].append(ath)
				outData["afi"].append(afi)
				outData["time"].append(time)
				outData["length"].append(length)
			elif i == footerLine:
				(lcr, ucr, ecr) = lines[i].split()
				outData["lcr"] = (lcr)
				outData["ucr"] = (ucr)
				outData["ecr"] = (ecr)
	print(outData)
	return outData
if __name__ == "__main__":
	loadData()
	







