import h5py
import os
import numpy as np
import scipy
from scipy.stats import kstwo, ks_2samp, kstest
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import statistics as st

file = 'D:/lfps/lfp3.hdf5'
matfile = r"C:\Users\User\OneDrive\Рабочий стол\2011 may 03 P32 BCX rust\2011_05_03_0003.mat"


def load_cc_lfp(filepath):
    lfp_cc = {}
    with h5py.File(filepath, 'r') as file:
        def traverse(group, prefix=""):
            for key in group.keys():
                item = group[key]
                path = f"{prefix}/{key}" if prefix else key
                if isinstance(item, h5py.Group):
                    traverse(item, path)
                elif isinstance(item, h5py.Dataset):
                    lfp_cc[path] = item[()]
        traverse(file)
    return lfp_cc

def load_matfile(file):
    mat = scipy.io.loadmat(file)
    lfp = mat['lfp']
    return lfp

def plotting_lfp(lfps):
    y_ticks_list = []
    yx=1
    fig, ax = plt.subplots()
    keys = list(lfps.keys())
    for i in keys:
        yx += 1
        ax.plot(np.array(lfps[i]) + yx*(1e3-5))
        y_ticks_list.append(i[7:20])
    ax.set_yticklabels(y_ticks_list)
    plt.show()


def main():
    lfp_cc = load_cc_lfp(file)
    lfp_mat = load_matfile(matfile)
    plotting_lfp(lfp_cc)
    result = 0
    mat_data = []
    mean_cc = 0
    mean_bio = 0
    for i in lfp_mat:
        mat_data = np.concatenate(i)
    for key, value in lfp_cc.items():
        result = ks_2samp(value, mat_data)
        mean_cc = st.mean(value)
    mean_bio = st.mean(mat_data)
    print(result)
    print("Среднее значение в lfp_cc " + str(mean_cc))
    print("Среднее значение в lfp_mat " + str(mean_bio))


if __name__ == "__main__":
    main()