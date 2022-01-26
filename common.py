import os, random, shutil, sys
import numpy as np
import time as tm
import subprocess
import datetime as dt
import ctypes

def rmAny(path):
	if os.path.exists(path):
		if os.path.isdir(path):
			shutil.rmtree(path)
		else:
			os.remove(path)
	else:
		sys.exit("Exiting! File " + path + " does not exist!")

def get_size(start_path = '.'):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			# skip if it is symbolic link
			if not os.path.islink(fp):
				total_size += os.path.getsize(fp)
	return total_size

def getS(filename):
	if filename == None:
		return ""
	if(os.path.isdir(filename)):
		return float(get_size(filename)/1000)
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
		#pridat aj vela malych suborov
		#pomerat pri hdf aj ten druhy kompresny filter
		#statistika nie 10 ale 1000+ merani, brat median
		#neskor urobit aj ramdisk meranie (mozno docker)
		os.system('sudo sh -c "sync; echo 1 > /proc/sys/vm/drop_caches"')
		os.system('sudo sh -c "sync; echo 2 > /proc/sys/vm/drop_caches"')
		os.system('sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"')
		ret = func()
		time = time + ret
		times.append(ret)
	minimum = min(times)
	maximum = max(times)
	time = time - minimum - maximum
	i = i+1#range 0 to 10 ends with 9 but there are 10 iterations
	print("Test:",testName,"has AVGtime:", formatter(time / (i-2)), "size:", getS(filename), "k bytes")

def writeAscii(gData, aData, fName):
	with open(fName, "w") as f:
		header = """\n\n
                ASYMPTOTIC COORDINATES
   calculated by model of exter.field {extern_field}   
 Station with geo.latitude:   {geo_lat:.3f}  & longitude:   {geo_lon:.3f} & radius :  {geo_rad:.5f}
 Direction of trajectory with latitude:    {loc_lat:.3f} & longitude:    {loc_lon:.3f}
 Datum: 1201  1 31  time:  0 hod  0 min  0 sec
 Starting rigidity :   {starting_rig:.4f} GV Epsilon= {rig_step:.4f}
 Limit of total number of steps : {step_limit} 

 rig : v : rad : eth : efi : ath : afi : time : length\n""".format(extern_field = gData["extern_field"], geo_lat = gData["geo_lat"], geo_lon = gData["geo_lon"], geo_rad = gData["geo_rad"], loc_lat = gData["loc_lat"], loc_lon = gData["loc_lon"], starting_rig = gData["starting_rig"], rig_step = gData["rig_step"], step_limit = gData["step_limit"])
		f.write(header)
		for i in range(0, len(aData["rig"])):
			st = ""+"{:10.6f}".format(aData["rig"][i])+"   "+"{:.10f}".format(aData["v"][i])+"   "+"{:.6f}".format(aData["rad"][i])+"   "+"{:7.3f}".format(aData["eth"][i])+"   "+"{:7.3f}".format(aData["efi"][i])+"   "+"{:7.3f}".format(aData["ath"][i])+"   "+"{:7.3f}".format(aData["afi"][i])+"    "+"{:.6f}".format(aData["time"][i])+"       "+"{:9.2f}".format(aData["length"][i])+"\n"
			f.write(st)
		f.write("  CUTOFF s rigidities P(S),P(C),P(M) are:\n")
		f.write("     "+"{:.5f}".format(gData["lcr"])+"     "+"{:.5f}".format(gData["ucr"])+"     "+"{:.5f}".format(gData["ecr"])+"\n\n")
	
def loadData(fName = "outfil_0"):
	arrayData = {"rig":[],"v":[],"rad":[],"eth":[],"efi":[],"ath":[],"afi":[],"time":[],"length":[]}
	globalData = {"arr_len": 0, "lcr": 0, "ucr": 0, "ecr": 0, "extern_field": None, "geo_lat": None,"geo_lon": None, "geo_rad": None, "loc_lat": None, "loc_lon": None, "datetime": None, "starting_rig": None, "rig_step": None, "step_limit": None}
	with open(fName, "r") as f:
		lines = f.readlines()
		numberOfLines = len(lines)
		globalData["arr_len"] = int(numberOfLines - (12 + 3))
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
					globalData["datetime"] = datetime.isoformat()
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

def generateSFvalues(size):
	random.seed(9)
	intensity = []
	rigidityL = []
	rigidityU = []
	rigidityE = []
	intensity = []
	for i in range(0, size):
		randI = float(random.randint(-100,15)) * 0.1215
		rigidityL.append(float(i) * randI)
		rigidityU.append(float(i) + randI)
		rigidityE.append(float(i) - randI)
		intensity.append(float(i)*randI + randI)
	return (intensity, rigidityL, rigidityU, rigidityE)

if __name__ == "__main__":
	#gData, aData = loadData()
	#writeAscii(gData, aData)
	(intensity, rigidityL, rigidityU, rigidityE) = generateSFvalues(100)
#	writeSmallFiles(intensity, rigidityL, rigidityU, rigidityE)
#	generateSmallFiles(100)
#	readSmallFiles(100)
	







