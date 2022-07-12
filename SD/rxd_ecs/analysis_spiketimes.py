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
with os.scandir(r'path/') as it:
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

# ISIs - interspike intervals

for i in layer_23:
    ISIs=np.diff(i, axis=0)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(abs(lbda) / 2 / pi / bins ** 3) *
            exp(-abs(lbda) * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    print(model)
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    plot(model) # plot the model of probability
    plt.hist(ISIs, bins, color=color[0])
    fig.savefig('path/' + '23')
plt.clf()
for i in layer_4:
    ISIs = np.diff(i, axis=0)
    print(ISIs)
    ISIs = np.diff(i, axis=0)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(abs(lbda) / 2 / pi / bins ** 3) *
            exp(-abs(lbda) * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    print(model)
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    plot(model)  # plot the model of probability
    plt.hist(ISIs, bins, color=color[1])
    fig.savefig('path/' + '4')
plt.clf()
for i in layer_5:
    ISIs = np.diff(i, axis=0)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(abs(lbda) / 2 / pi / bins ** 3) *
            exp(-abs(lbda) * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    print(model)
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    plot(model)
    plt.hist(ISIs, bins, color=color[2])
    fig.savefig('path/' + '5')
plt.clf()
for i in layer_56:
    ISIs = np.diff(i, axis=0)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(abs(lbda) / 2 / pi / bins ** 3) *
            exp(-abs(lbda) * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    print(model)
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    plot(model)
    plt.hist(ISIs, bins, color=color[3])
    fig.savefig('path/' + '56')
plt.clf()
for i in layer_6:
    ISIs = np.diff(i, axis=0)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(abs(lbda) / 2 / pi / bins ** 3) *
            exp(-abs(lbda) * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    print(model)
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    plot(model)
    plt.hist(ISIs, bins, color=color[4])
    fig.savefig('path/' + '6')
plt.show()
