import numpy as np
import matplotlib.pyplot as plt
import data as d
import matplotlib.ticker as ticker
np.set_printoptions(precision=3, suppress=True)
#plt.rc('font', size=16)
#plt.rc('legend', fontsize=10)

colors=['green','green','blue','blue']
def plot_(labels, data, markers, label_names, filename, ylabel, title, limit_y = True):
    fig = plt.figure(tight_layout = True, dpi = 250, figsize=[6.25,2.8])


    print(filename)
    
    for i in range(0, len(data)):
        print(label_names[i], data[i])
        #data[i] = data[i][np.logical_not(np.isnan(data[i]))]
        plt.plot(labels, data[i], marker = markers[i%2], color=colors[i], label = label_names[i], linestyle=":", markersize=9,lw=0.5,mew=0.6)
    print("-----------------------------")
    plt.legend(fontsize=10.5)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(title,fontsize=11.5)
    ax = plt.gca()
    if limit_y:
        ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0, xmax=len(labels)-1)
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
markers = ["+", "x"]

label_names = ["read normal", "write normal", "read small", "write small", "lossy read normal", "lossy write normal", "lossy read small", "lossy write small"]

data = [
    83484/d.normal_uncompressed_ram[0],
    83484/d.normal_uncompressed_ram[1],
    180000/d.small_uncompressed_ram[0],
    180000/d.small_uncompressed_ram[1],
]

plot_(d.uncompressed_labels, data, markers, label_names, '0_0_uncompressed_fps.png', "Processing speed [element/s]", "Number of elements processed without compression")


data = [
    83484/d.normal_uncompressed_ram[2],
    83484/d.normal_uncompressed_ram[3],
    180000/d.small_uncompressed_ram[2],
    180000/d.small_uncompressed_ram[3],
]

plot_(d.uncompressed_labels, data, markers, label_names, '0_1_lossy_uncompressed_fps.png', "Processing speed [element/s]", "Number of elements processed without compression - lossy format")

data = [
    83484/d.normal_compressed_ram[0],
    83484/d.normal_compressed_ram[1],
    180000/d.small_compressed_ram[0],
    180000/d.small_compressed_ram[1],
]

plot_(d.compressed_labels, data, markers, label_names, '0_2_compressed_fps.png', "Processing speed [element/s]", "Number of elements processed with compression")

data = [
    83484/d.normal_compressed_ram[2],
    83484/d.normal_compressed_ram[3],
    180000/d.small_compressed_ram[2],
    180000/d.small_compressed_ram[3],
]

plot_(d.compressed_labels, data, markers, label_names, '0_3_lossy_compressed_fps.png', "Processing speed [element/s]", "Number of elements processed with compression - lossy format")
##########
data = [
    (100*((-d.normal_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/(d.normal_uncompressed_ram[0]),
    (100*((-d.normal_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/(d.normal_uncompressed_ram[1]),
    (100*((-d.small_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/(d.small_uncompressed_ram[0]),
    (100*((-d.small_uncompressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/(d.small_uncompressed_ram[1]),
]

plot_(d.uncompressed_labels, data, markers, label_names, '1_0_uncompressed_rps.png', "[%/s]", "Size reduction per second without compression", False)

data = [
    (100*((-d.normal_uncompressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_uncompressed_ram[2],
    (100*((-d.normal_uncompressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_uncompressed_ram[3],
    (100*((-d.small_uncompressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.small_uncompressed_ram[2],
    (100*((-d.small_uncompressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.small_uncompressed_ram[3],
]

plot_(d.uncompressed_labels, data, markers, label_names, '1_1_lossy_uncompressed_rps.png', "[%/s]", "Size reduction per second without compression - lossy format", False)

data = [
    (100*((-d.normal_compressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[0],
    (100*((-d.normal_compressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[1],
    (100*((-d.small_compressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.small_compressed_ram[0],
    (100*((-d.small_compressed_sz[0]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.small_compressed_ram[1],
]

plot_(d.compressed_labels, data, markers, label_names, '1_2_compressed_rps.png', "[%/s]", "Size reduction per second with compression", False)

data = [
    (100*((-d.normal_compressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[2],
    (100*((-d.normal_compressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.normal_compressed_ram[3],
    (100*((-d.small_compressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.small_compressed_ram[2],
    (100*((-d.small_compressed_sz[1]+d.normal_uncompressed_sz[0][0])/d.normal_uncompressed_sz[0][0]))/d.small_compressed_ram[3],
]

plot_(d.compressed_labels, data, markers, label_names, '1_3_lossy_compressed_rps.png', "[%/s]", "Size reduction per second with compression - lossy format", False)
##########
data = [
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

plot_(d.compressed_labels, data, markers, label_names, '2_compressed_ssd_to_ram.png', "[-]", "Disk slowdown with compression", False)
