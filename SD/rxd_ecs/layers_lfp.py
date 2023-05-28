import matplotlib.pyplot as plt
import numpy as np
import scipy.io
from pylab import *
import seaborn as sns
from scipy.stats import norm, kstest

filepath = r'C:\Users\User\OneDrive\Рабочий стол\2011 may 03 P32 BCX rust\2011_05_03_0003.mat'
file=""

color = ['red', 'blue', 'yellow', 'black', 'gray', 'cyan', 'magenta']

def load_data(filepath):
    mat = scipy.io.loadmat(filepath)
    spks = mat['lfp']
    return spks

data = load_data(filepath)
data = np.moveaxis(data, [0, 1, 2], [2, 1,0])
data_0=[]
yx=0
for era, items in enumerate(data):
    if era<=4:
        for channel, varb in enumerate(items):
            plt.plot(np.array(items[0])+yx*850)
            yx+=1


plt.show()
