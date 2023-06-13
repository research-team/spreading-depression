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
color = ['red', 'blue', 'yellow', 'black', 'gray', 'cyan', 'magenta']

fig, ax = plt.subplots()
bins = np.arange(0, 10, 0.1)

def analysis(spks):
    ISIs=np.diff(spks)
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    mu=ISIs.mean()
    lbda= 1 / (1 / ISIs - 1 / mu).mean()
    model=(
    sqrt(lbda / 2 / pi / bins ** 3) *
    exp(-lbda * (bins - mu) ** 2 / 2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    # lbda = 1 / ISIs.mean()
    # model = lbda * exp(-lbda * bins)
    plt.plot(bins, model, 'b', color=color[0])
    plt.xlabel('ISIs')
    plt.ylabel('Probability')
    plt.show()

data_0=[]
x=0
for channel, items in enumerate(data):
        for era, varb in enumerate(items):
            data_0.append(varb[0]+x)
            x+=1000
data_0=np.concatenate(data_0, axis=None)
analysis(data_0)