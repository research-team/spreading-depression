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

bins = np.arange(0.1, 10, 0.1)

data_0=np.concatenate(layer_56)
ISIs = np.diff(data_0)
counts, _ = histogram(ISIs, bins)
prob = counts / len(ISIs)
bar(bins[:-1], prob, width=0.1)
lbda = 1 / ISIs.mean()
model = lbda * exp(-lbda * bins) * 0.01
plt.plot(bins, model, 'b')
plt.xlabel('ISIs')
plt.ylabel('Probability')
plt.show()

