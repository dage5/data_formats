import numpy as np

all_labels = ["text","netCDF","HDF5","CDF","text*","netCDF*","HDF5 gzip*","HDF5 lzf*","CDF*"]

uncompressed_labels = ["text","netCDF","HDF5","CDF"]
uncompressed_lossy_labels = ["netCDF","HDF5"]
compressed_labels = ["text","netCDF","HDF5 gzip","HDF5 lzf","CDF"]
compressed_lossy_labels = ["netCDF","HDF5 gzip","HDF5 lzf"]
#text,netCDF,HDF5,CDF
normal_uncompressed_sz = np.array([
[983.77,681.83,678.50,678.32],
[float("NaN"),682.66,129.98,float("NaN")]
])

#text,netCDF,gzip,lzf,CDF
normal_compressed_sz = np.array([
[180.13,336.73,333.93,398.15,199.50],#not lossy
[float("NaN"),85.69,116.28,119.44, float("NaN")]#lossy
])

#text	netCDF	HDF5	CDF
small_uncompressed_sz = np.array([
[1625.71,1926.68,1924.48,1922.84],#not lossy
[float("NaN"),1927.58,441.984,float("NaN")]#lossy
])

#text,netCDF,gzip,lzf,CDF
small_compressed_sz = np.array([
[23080.59,1518.63,1654.44,1779.79,798.22],#not lossy
[float("NaN"),480.67,442.61,442.12,float("NaN")]#lossy
])
##########################
#text	netCDF	HDF5	CDF
normal_uncompressed_ram = np.array([
[34.83,7.38,5.22,2.88],#read
[19.12,4.18,2.25,2.20],#write
[float("NaN"),8.02,12.38,float("NaN")],#read lossy
[float("NaN"),4.28,4.22,float("NaN")]#write lossy
])
#text,netCDF,gzip,lzf,CDF
normal_compressed_ram = np.array([
[282.63,24.42,17.40,9.19,30.62],#read
[38.59,6.41,5.29,3.60,6.26],#write
[float("NaN"),22.25,15.30,13.05,float("NaN")],#read lossy
[float("NaN"),5.69,4.78,4.34,float("NaN")]#write lossy
])

#text	netCDF	HDF5	CDF
small_uncompressed_ram = np.array([
[1615.27,8.93,7.54,6.22],#read
[1430.97,2.67,1.55,2.12],#write
[float("NaN"),11.27,25.94,float("NaN")],#read lossy
[float("NaN"),2.77,7.02,float("NaN")]#write lossy
])
#text,netCDF,gzip,lzf,CDF
small_compressed_ram = np.array([
[3488.90,119.16,50.24,20.08,125.53],#read
[2498.23,9.78,10.24,3.27,15.39],#write
[float("NaN"),99.50,33.43,28.87,float("NaN")],#read lossy
[float("NaN"),8.33,8.38,7.19,float("NaN")]#write lossy
])
##########################
#text	netCDF	HDF5	CDF
normal_uncompressed_ssd = np.array([
[35.32,8.09,5.51,3.46],
[24.44,8.84,5.20,5.25],
[float("NaN"),8.85,12.63,float("NaN")],
[float("NaN"),9.00,5.56,float("NaN")],
])
#text,netCDF,gzip,lzf,CDF
normal_compressed_ssd = np.array([
[285.68,26.15,18.56,9.79,32.23],
[46.76,9.46,7.08,5.74,5.25],
[float("NaN"),23.92,16.04,13.56,float("NaN")],
[float("NaN"),7.38,7.08,5.84,float("NaN")],
])

#text	netCDF	HDF5	CDF
small_uncompressed_ssd = np.array([
[3301.75,10.46,8.85,7.33],
[15568.44,8.57,5.59,6.04],
[float("NaN"),12.52,27.51,float("NaN")],
[float("NaN"),8.48,8.77,float("NaN")],
])
#text,netCDF,gzip,lzf,CDF
small_compressed_ssd = np.array([
[6103.37,134.13,56.63,22.36,123.67],
[4477.46,14.79,13.96,8.24,17.30],
[float("NaN"),110.56,36.11,30.53,float("NaN")],
[float("NaN"),10.54,10.19,8.93,float("NaN")],
])
