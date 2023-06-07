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
# 0. ?? 1. channel 2. experiment
data_=data[:, :, 2]

def plot_lfp(X):
    mS = X.shape
    mInter = max(X.flatten())
    mShift = -abs(mInter) * range(mS[1])
    X2 = X + mShift

    plt.plot(X2)

    # bar
    mCoorX = [int(0.9 * mS[0]), int(0.9 * mS[0])]
    mCoorY = [int(mShift[-1]), int(mShift[-2])]
    plt.plot(mCoorX, mCoorY)
    plt.text(mCoorX[0] + 5, int(mCoorY[1] - mInter / 2), str(int(mInter)), dict(size=10))
    plt.show()
    # print(mS)

plot_lfp(data_)
