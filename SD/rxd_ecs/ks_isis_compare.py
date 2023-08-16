import numpy as np
import scipy.io
import os
from matplotlib import pyplot as plt
from scipy.stats import kstwo, ks_2samp, kstest
from pylab import *

filepath=r"C:\Users\User\OneDrive\Рабочий стол\2011 may 03 P32 BCX rust\2011_05_03_0003.mat"

def load_data(file):
    mat = scipy.io.loadmat(file)
    spks = mat['spks']
    return spks

data_gen=[]
with os.scandir(r'C:\Users\User\OneDrive\Рабочий стол\последние результаты') as it:
    for entry in it:
        if entry.name.endswith(".txt") and entry.is_file():
            with open(entry.path, 'r') as f:
                for line in f:
                    line = line.rstrip('\n\r')
                    data_gen.append(float(line))

data=load_data(filepath)
data_bio=[]
ISI_bio=[]
for channel, items in enumerate(data):
        for era, varb in enumerate(items):
            if any(varb[0]):
                a=np.concatenate(varb[0], axis=None)
                data_bio.append(a)
                ISIs = np.diff(a)
                ISI_bio.append(ISIs)

data_bio=np.concatenate(data_bio)
data_bio_f=[]
for i in data_bio:
    data_bio_f.append(float(i))
#all data
res_all=kstest(data_bio_f, data_gen)

#ISIs
ISIs_gen=np.diff(data_gen)

ISI_bio=np.concatenate(ISI_bio)
res_isis=ks_2samp(ISIs_gen, ISI_bio)

print(res_all)


