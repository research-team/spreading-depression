import h5py
import os
import numpy as np
import scipy
from scipy import io
from scipy.stats import kstwo, ks_2samp, kstest
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import statistics as st

file = ''
matfile = r""


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
    keys.sort()
    for i in keys:
        yx += 1
        plt.plot(np.array(lfps[i]) + yx*(1e3-5))
        # y_ticks_list.append(i[7:20])
    plt.legend([key[7:20] for key in keys])
    # ax.set_yticklabels(y_ticks_list)
    plt.show()


def main():
    lfp_cc = load_cc_lfp(file)
    lfp_mat = load_matfile(matfile)
    plotting_lfp(lfp_cc)
    result = 0
    mat_data = []
    mean_cc = 0
    mean_bio = 0
    values = []

    for channel, items in enumerate(lfp_mat):
        for era, varb in enumerate(items):
            mat_data.append(varb)
            # mean_bio=st.mean(varb)

    for key, value in lfp_cc.items():
        values.append(value)
        # mean_cc=st.mean(value)


    result = ks_2samp(values[0], mat_data[0])

    mat_data = np.concatenate(mat_data)
    values = np.concatenate(values)

    mean_cc = st.mean(values)
    mean_bio = st.mean(mat_data)

    print(result)
    print("Среднее значение в lfp_cc " + str(mean_cc))
    print("Среднее значение в lfp_mat " + str(mean_bio))


if __name__ == "__main__":
    main()