import fnmatch
import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import numpy.ma as ma
from scipy.stats import gamma
from pylab import *


filepath = r"path/"


def load_data(filepath):
    mat = scipy.io.loadmat(filepath)
    spks = mat['spks']
    return spks
data = load_data(filepath)
# print(data)

color = ['red', 'blue', 'yellow', 'black', 'gray', 'cyan', 'magenta']



fig, ax = plt.subplots()
data = np.moveaxis(data, [0, 1], [1, 0])

# Отстройка спайктаймов 
for j, spks in enumerate(data):
    i = 0
    plt.clf()

    for p, items in enumerate(spks):
        items_3 = np.array(items[0])
        mask=(items_3 >= 350) & (items_3 <= 400)
        if p==12 or p==14 or p==13:
            plt.vlines(items_3[mask], 1.5, 2.5 , color=color[0])
        if p==9 or p==11:
            plt.vlines(items_3[mask], 1.5, 2.5 , color=color[1])
        if p==8 or p==10:
            plt.vlines(items_3[mask], 1.5, 2.5 , color=color[2])
        if p==6 or p==7:
            plt.vlines(items_3[mask], 1.5, 2.5 , color=color[3])
        if p==3 or p==4 or p==5:
            plt.vlines(items_3[mask], 1.5, 2.5 , color=color[4])
        if p == 0 or p == 1 or p == 2:
            plt.vlines(items_3[mask], 1.5, 2.5 , color=color[5])
        #plt.vlines(items[0], i, i+1)
    i += 1
    fig.savefig('path/' + str(j))

# Анализ

#ISIs - interspike intervals
# for a, spks in enumerate(data):
data_3= data[29]
# print(data_3)
layer_13=[]
layer_12_14=[]
layer_9_11=[]
layer_8_10=[]
layer_6_7=[]
layer_3_4_5=[]
layer_0_1_2=[]
bins = np.arange(0.1, 5, 0.1)
for b, items in enumerate(data_3):
    if b==13:
        layer_13.append(items[0])
    if b==12 or b==14:
        layer_12_14.append(items[0])
    if b==9 or b==11:
        layer_9_11.append(items[0])
    if b==8 or b==10:
        layer_8_10.append(items[0])
    if b==6 or b==7:
        layer_6_7.append(items[0])
    if b==3 or b==4 or b==5:
        layer_3_4_5.append(items[0])
    if b==0 or b==1 or b==2:
        layer_0_1_2.append(items[0])

for i in layer_13:
    ISIs = np.diff(i, axis=0)
    N = len(ISIs)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(lbda / 2 / pi / bins ** 3) *
            exp(-lbda * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    # lbda = 1 / ISIs.mean()
    # model = lbda * exp(-lbda * bins) * 0.1
    plot(bins, model, 'b')
    # plt.hist(ISIs, bins, color=color[6])
    fig.savefig('path/' + '13')
plt.clf()
for i in layer_12_14:
    ISIs = np.diff(i, axis=0)
    N = len(ISIs)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(lbda / 2 / pi / bins ** 3) *
            exp(-lbda * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    # lbda = 1 / ISIs.mean()
    # model = lbda * exp(-lbda * bins) * 0.1
    plot(bins, model, 'b')
    # plt.hist(ISIs, bins, color=color[5])
    fig.savefig('path/' + '12_14')
plt.clf()
for i in layer_9_11:
    ISIs = np.diff(i, axis=0)
    N = len(ISIs)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(lbda / 2 / pi / bins ** 3) *
            exp(-lbda * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    # lbda = 1 / ISIs.mean()
    # model = lbda * exp(-lbda * bins) * 0.1
    plot(bins, model, 'b')
    # plt.hist(ISIs, bins, color=color[4])
    fig.savefig('path/' + '9_11')
plt.clf()
for i in layer_8_10:
    ISIs = np.diff(i, axis=0)
    N = len(ISIs)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(lbda / 2 / pi / bins ** 3) *
            exp(-lbda * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    # lbda = 1 / ISIs.mean()
    # model = lbda * exp(-lbda * bins) * 0.1
    plot(bins, model, 'b')
    # plt.hist(ISIs, bins, color=color[3])
    fig.savefig('path/' + '8_10')
plt.clf()
for i in layer_6_7:
    ISIs = np.diff(i, axis=0)
    N = len(ISIs)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(lbda / 2 / pi / bins ** 3) *
            exp(-lbda * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    # lbda = 1 / ISIs.mean()
    # model = lbda * exp(-lbda * bins) * 0.1
    plot(bins, model, 'b')
    # plt.hist(ISIs, bins, color=color[2])
    fig.savefig('path/' + '6_7')
plt.clf()
for i in layer_3_4_5:
    ISIs = np.diff(i, axis=0)
    N = len(ISIs)
    mu = ISIs.mean()
    lbda = 1 / (1 / ISIs - 1 / mu).mean()
    model = (
            sqrt(lbda / 2 / pi / bins ** 3) *
            exp(-lbda * (bins - mu) ** 2 /
                2 / mu ** 2 / bins) * 0.1
    )
    model[0] = 0
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    # lbda = 1 / ISIs.mean()
    # model = lbda * exp(-lbda * bins) * 0.1
    plot(bins, model, 'b')
    fig.savefig('path/' + '3_4_5')
plt.clf()
for i in layer_0_1_2:
    ISIs=np.diff(i, axis=0)
    N=len(ISIs)
    mu=ISIs.mean()
    lbda= 1 /(1/ISIs - 1/ mu).mean()
    model= (
        sqrt(lbda/2/pi/bins**3)*
        exp(-lbda*(bins-mu)**2 /
            2/mu ** 2 / bins)*0.1
    )
    model[0]=0
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.1)
    # lbda = 1 / ISIs.mean()
    # model = lbda * exp(-lbda * bins) * 0.1
    plot(bins, model, 'b')
#     plt.hist(ISIs, bins, color=color[0])
    fig.savefig('path/' + '0_1_2')
plt.clf()
plt.show()
