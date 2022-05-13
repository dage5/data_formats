import numpy as np
import matplotlib.pyplot as plt
import data as d
import matplotlib.ticker as ticker
np.set_printoptions(precision=3, suppress=True)
#plt.rc('font', size=16)
#plt.rc('legend', fontsize=10)

def autolabel(rects, ax, data_max):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        h_fmt = '{:.2f}'
        rot = 90
        offst = (0, 1)
        if (height > 50):
            h_fmt = '{:.1f}'

        if (height > data_max/2):
            offst = (0, -45)
        ax.annotate(h_fmt.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=offst,  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, rotation = rot)

colors = ['lightcoral','greenyellow','cyan','peachpuff']#['green','blue']#
markers = ["+", "x"]#["+", "+", "x", "x"]#
def plot_(labels, data, markers, colors, label_names, filename, ylabel, title, limit_y = True, figsize = [6.25,2.6], linestyle = ":"):
    fig = plt.figure(tight_layout = True, dpi = 250, figsize=figsize)


    x = np.arange(len(labels))
    width = 0.2
    print(labels, x)
    ax = plt.gca()
    data_max = np.nanmax(np.array(data))
    print(data_max)
    
    for i in range(0, len(data)):
        print(label_names[i], data[i])
        #data[i] = data[i][np.logical_not(np.isnan(data[i]))]
        #plt.plot(labels, data[i], marker = markers[i%2], color=colors[i], label = label_names[i], linestyle=linestyle, markersize=9, lw=0, mew=1.5)
        x_pos = x + width*(i) - (width*len(data))/2 + width/2 #+ (width*len(labels)) #- (width/len(data))
        #print(x_pos)#, width*(i+1), (width*len(data))/2)
        data[i][data[i] == 0] = np.nan
        rects = plt.bar(x_pos, data[i], width, label = label_names[i], color=colors[i], edgecolor="gray", linewidth = 1)#,align='edge')
        autolabel(rects, ax, data_max)
    print("-----------------------------")
    plt.legend(fontsize=8, borderpad=0.1, framealpha=0.5)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(title,fontsize=11.5)
    if limit_y:
        ax.set_ylim(ymin=0)
    #ax.set_xlim(xmin=0, xmax=len(labels)-1)
    #ax.set_xticklabels(labels)

    ax.xaxis.set_major_locator(ticker.FixedLocator(x))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(labels))
    
    ax.yaxis.grid(which='minor', alpha=0.3, linestyle=':')
    ax.grid(which='major', alpha=0.6, linestyle='--')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=8))
    plt.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    plt.setp(ax.get_yticklabels(), rotation=55, horizontalalignment='right')

    plt.savefig(filename, bbox_inches='tight')
    plt.cla()
    plt.clf()
    plt.close('all')

#markers = ["s", "+", "x", "D", "1", "8", "p", "*"]

label_names = ["write normal", "read normal", "write small", "read small", "lossy write normal", "lossy read normal", "lossy write small", "lossy read small"]
################################xx
##########
"""data = [
    ((d.normal_uncompressed_ram[0])/(100*((-d.normal_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0])))[0:3],
    ((d.normal_uncompressed_ram[1])/(100*((-d.normal_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0])))[0:3],
    ((d.small_uncompressed_ram[0])/(100*((-d.small_uncompressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0])))[0:3],
    ((d.small_uncompressed_ram[1])/(100*((-d.small_uncompressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0])))[0:3],
]
print(data)
plot_(["netCDF","HDF5","CDF"], data, markers, label_names, '2_0_uncompressed_rps.png', "[%/s]", "Size reduction per second without compression", False)
"""
################################xx
data = [
    83484/d.normal_uncompressed_ram[0],
    83484/d.normal_uncompressed_ram[1],
    180000/d.small_uncompressed_ram[0],
    180000/d.small_uncompressed_ram[1],
]

plot_(d.uncompressed_labels, data, markers, colors, label_names, '0_0_uncompressed_fps.png', "Processing speed [element/s]", "Number of elements processed without compression")


data = [
    83484/d.normal_uncompressed_ram[2],
    83484/d.normal_uncompressed_ram[3],
    180000/d.small_uncompressed_ram[2],
    180000/d.small_uncompressed_ram[3],
]

plot_(d.uncompressed_labels, data, markers, colors, label_names, '0_1_lossy_uncompressed_fps.png', "Processing speed [element/s]", "Number of elements processed without compression - lossy format")

data = [
    83484/d.normal_compressed_ram[0],
    83484/d.normal_compressed_ram[1],
    180000/d.small_compressed_ram[0],
    180000/d.small_compressed_ram[1],
]

plot_(d.compressed_labels, data, markers, colors, label_names, '0_2_compressed_fps.png', "Processing speed [element/s]", "Number of elements processed with compression")

data = [
    83484/d.normal_compressed_ram[2],
    83484/d.normal_compressed_ram[3],
    180000/d.small_compressed_ram[2],
    180000/d.small_compressed_ram[3],
]

plot_(d.compressed_labels, data, markers, colors, label_names, '0_3_lossy_compressed_fps.png', "Processing speed [element/s]", "Number of elements processed with compression - lossy format")
##########
data = [
    (100*((-d.normal_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/(d.normal_uncompressed_ram[0]),
    (100*((-d.normal_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/(d.normal_uncompressed_ram[1]),
    (100*((-d.small_uncompressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/(d.small_uncompressed_ram[0]),
    (100*((-d.small_uncompressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/(d.small_uncompressed_ram[1]),
]

plot_(d.uncompressed_labels, data, markers, colors, label_names, '1_0_uncompressed_rps.png', "[%/s]", "Size reduction per second without compression", False)

data = [
    (100*((-d.normal_uncompressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_uncompressed_ram[2],
    (100*((-d.normal_uncompressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_uncompressed_ram[3],
    (100*((-d.small_uncompressed_sz[1]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_uncompressed_ram[2],
    (100*((-d.small_uncompressed_sz[1]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_uncompressed_ram[3],
]

plot_(d.uncompressed_labels, data, markers, colors, label_names, '1_1_lossy_uncompressed_rps.png', "[%/s]", "Size reduction per second without compression - lossy format", False)

data = [
    (100*((-d.normal_compressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[0],
    (100*((-d.normal_compressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[1],
    (100*((-d.small_compressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_compressed_ram[0],
    (100*((-d.small_compressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_compressed_ram[1],
]

plot_(d.compressed_labels, data, markers, colors, label_names, '1_2_compressed_rps.png', "[%/s]", "Size reduction per second with compression", False)

data = [
    (100*((-d.normal_compressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[2],
    (100*((-d.normal_compressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[3],
    (100*((-d.small_compressed_sz[1]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_compressed_ram[2],
    (100*((-d.small_compressed_sz[1]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_compressed_ram[3],
]

plot_(d.compressed_labels, data, markers, colors, label_names, '1_3_lossy_compressed_rps.png', "[%/s]", "Size reduction per second with compression - lossy format", False)
##########
data = np.array([
    np.concatenate(((100*((-d.normal_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/(d.normal_uncompressed_ram[0]), (100*((-d.normal_compressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[0]
)),
    np.concatenate(((100*((-d.normal_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/(d.normal_uncompressed_ram[1]),(100*((-d.normal_compressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[1])),
    np.concatenate(((100*((-d.small_uncompressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/(d.small_uncompressed_ram[0]),(100*((-d.small_compressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_compressed_ram[0])),
    np.concatenate(((100*((-d.small_uncompressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/(d.small_uncompressed_ram[1]),(100*((-d.small_compressed_sz[0]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_compressed_ram[1])),
])
#data = 1 / data


for i in range(0, len(data)):
    data[i][np.isinf(np.abs(data[i]))] = 0
    data[i][np.isnan(np.abs(data[i]))] = np.nan
    data[i][data[i] < 0] = np.nan

colors = ['green','blue','red','black']#['green','blue']#
markers = ["+", "x"]#["+", "+", "x", "x"]#

plot_(d.all_labels, data, markers, colors, label_names, '9_1_rps.png', "[%/s]", "Size reduction per second with compression - lossless", False, [12,4], "")

data = np.array([
    np.concatenate(((100*((-d.normal_uncompressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_uncompressed_ram[2],(100*((-d.normal_compressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[2])),
    np.concatenate(((100*((-d.normal_uncompressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_uncompressed_ram[3],(100*((-d.normal_compressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[3])),
    np.concatenate(((100*((-d.small_uncompressed_sz[1]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_uncompressed_ram[2],(100*((-d.small_compressed_sz[1]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_compressed_ram[2])),
    np.concatenate(((100*((-d.small_uncompressed_sz[1]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_uncompressed_ram[3],(100*((-d.small_compressed_sz[1]+d.small_uncompressed_sz[0][0])/d.small_uncompressed_sz[0][0]))/d.small_compressed_ram[3]))

])
#data = 1 / data
for i in range(0, len(data)):
    data[i][np.isinf(np.abs(data[i]))] = 0
    data[i][np.isnan(np.abs(data[i]))] = np.nan
    data[i][data[i] < 0] = np.nan

colors = ['green','blue','red','black']#['green','blue']#
markers = ["+", "x"]#["+", "+", "x", "x"]#

plot_(d.all_labels, data, markers, colors, label_names, '9_2_rps.png', "[%/s]", "Size reduction per second with compression - lossy", False, [12,4], "")



"""data = [
    d.normal_uncompressed_ssd[0]/d.normal_uncompressed_ram[0],
    d.normal_uncompressed_ssd[1]/d.normal_uncompressed_ram[1],
    d.small_uncompressed_ssd[0]/d.small_uncompressed_ram[0],
    d.small_uncompressed_ssd[1]/d.small_uncompressed_ram[1],
    d.normal_uncompressed_ssd[2]/d.normal_uncompressed_ram[2],
    d.normal_uncompressed_ssd[3]/d.normal_uncompressed_ram[3],
    d.small_uncompressed_ssd[2]/d.small_uncompressed_ram[2],
    d.small_uncompressed_ssd[3]/d.small_uncompressed_ram[3],
]

plot_(d.uncompressed_labels, data, markers, label_names, '2_uncompressed_ssd_to_ram.png', "[-]", "Disk slowdown without compression", False)

data = [
    d.normal_compressed_ssd[0]/d.normal_compressed_ram[0],
    d.normal_compressed_ssd[1]/d.normal_compressed_ram[1],
    d.small_compressed_ssd[0]/d.small_compressed_ram[0],
    d.small_compressed_ssd[1]/d.small_compressed_ram[1],
    d.normal_compressed_ssd[2]/d.normal_compressed_ram[2],
    d.normal_compressed_ssd[3]/d.normal_compressed_ram[3],
    d.small_compressed_ssd[2]/d.small_compressed_ram[2],
    d.small_compressed_ssd[3]/d.small_compressed_ram[3],
]

plot_(d.compressed_labels, data, markers, label_names, '2_compressed_ssd_to_ram.png', "[-]", "Disk slowdown with compression", False)"""
