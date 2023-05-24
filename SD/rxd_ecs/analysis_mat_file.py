import fnmatch
import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import numpy.ma as ma
from scipy.stats import gamma
from pylab import *


filepath = r'C:\Users\User\OneDrive\Рабочий стол\2011 may 03 P32 BCX rust\2011_05_03_0003.mat'
file=""


def load_data(filepath):
    mat = scipy.io.loadmat(filepath)
    spks = mat['spks']
    return spks
data = load_data(filepath)
# print(data)

color = ['red', 'blue', 'yellow', 'black', 'gray', 'cyan', 'magenta']

fig, ax = plt.subplots()
bins = np.arange(0.9, 10, 0.1)

def analysis(spks):
    ISIS=np.concatenate(spks)
    counts, _ = histogram(ISIS, bins)
    prob = counts / len(ISIS)
    bar(bins[:-1], prob, width=0.1)
    lbda = 1 / ISIS.mean()
    model = lbda * exp(-lbda * bins) * 0.1
    plt.plot(bins, model, 'b')
    plt.xlabel('ISIs')
    plt.ylabel('Probability')
    count=0
    # fig.savefig(r'C:\Users\User\OneDrive\Рабочий стол\bio_res\0'+str(count+1))
    # count+=1
    plt.show()

data_0=[]
x=0
ISIs=[]
a=[]
for channel, items in enumerate(data):
    if channel==0:
        for era, varb in enumerate(items):
            data_0.append(varb[0])
            a=np.concatenate(data_0)
        ISIs=np.diff(a)
            # x += 1000
analysis(ISIs)