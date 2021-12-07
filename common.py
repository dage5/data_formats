import os
import numpy as np
import time as tm
import subprocess

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
