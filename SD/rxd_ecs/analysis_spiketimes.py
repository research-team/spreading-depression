import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import numpy.ma as ma
from pylab import  *

color = ['red', 'blue', 'yellow', 'black', 'green', 'cyan', 'magenta']
fig, ax = plt.subplots()
data_ = []
layers=[]
with os.scandir(r'C:\Users\User\OneDrive\Рабочий стол\последние результаты') as it:
    for entry in it:
        if entry.name.endswith(".txt") and entry.is_file():
            with open(entry.path, 'r') as f:
                layer = str(str(entry.name).rsplit('_')[1])
                layers.append(layer)
                spiketime = []
                for line in f:
                    line = line.rstrip('\n\r')
                    spiketime.append(float(line))
                data_.append((layer,spiketime))

bins = np.arange(0.1, 60, 0.1)
def analysis(spks):
    ISIs=np.diff(spks)
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.2)
    # mu=ISIs.mean()
    # lbda= 1 / (1 / ISIs - 1 / mu).mean()
    # model=(
    # sqrt(lbda / 2 / pi / bins ** 3) *
    # exp(-lbda * (bins - mu) ** 2 / 2 / mu ** 2 / bins) * 0.1
    # )
    # model[0] = 0
    lbda = 1 / ISIs.mean()
    model = lbda * exp(-lbda * bins)
    plt.plot(bins, model, 'b', color=color[0])
    plt.xlabel('ISIs')
    plt.ylabel('Probability')
    plt.show()

d=[]
for l, s in data_:
    d.append(s)

d=np.concatenate(d)
analysis(d)

layer_23=[]
layer_4=[]
layer_5=[]
layer_56=[]
layer_6=[]
bins = np.arange(0.1, 100, 0.1)
for layer, spks in data_:
    '''L-23'''
    if layer=="1" or layer=="2" or layer=="3" or layer=="12" or layer=="13":
        layer_23.append(spks)
    '''L-4'''
    if layer=="4" or layer=="16":
        layer_4.append(spks)
    '''L-5'''
    if layer=="5" or layer=="6":
        layer_5.append(spks)
    '''L-56'''
    if layer=="7" or layer=="8" or layer=="9":
        layer_56.append(spks)
    '''L-6'''
    if layer=="10":
        layer_6.append(spks)
