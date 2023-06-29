import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from pylab import *


filepath = r"C:\Users\User\OneDrive\Рабочий стол\2011 may 03 P32 BCX rust\2011_05_03_0003.mat"


def load_data(filepath):
    mat = scipy.io.loadmat(filepath)
    spks = mat['spks']
    return spks
data = load_data(filepath)
# print(data)

color = ['red', 'blue', 'yellow', 'black', 'gray', 'cyan', 'magenta']
fig, ax = plt.subplots()

bins = np.arange(0, 60, 0.1)

def analysis(spks):
    ISIs=np.array(spks)
    counts, _ = histogram(ISIs, bins)
    prob = counts / len(ISIs)
    bar(bins[:-1], prob, width=0.2)
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
ISI=[]
for channel, items in enumerate(data):
        for era, varb in enumerate(items):
            if any(varb[0]):
                a=np.concatenate(varb[0], axis=None)
                ISIs=np.diff(a)
                ISI.append(ISIs)

for i in ISI:
    for y in i:
        if y>1:
            data_0.append(y)

# data_0=np.concatenate(data_0, axis=None)
analysis(data_0)

