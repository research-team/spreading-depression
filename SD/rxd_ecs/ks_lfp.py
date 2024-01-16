import h5py
import os
import numpy as np
import scipy
from scipy import io
from scipy.stats import kstwo, ks_2samp, kstest
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import statistics as st
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.models import ColumnDataSource
from bokeh.models import Legend
import pandas as pd

file = ''
matfile = r""


def load_cc_lfp(filepath):
    '''
    Load lfp from hdf5 file
    Args:
		filepath (str): path to the file
	Returns:
		lfp_cc: dictionary with keys and values
    '''
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
    '''
    Load mat file
    Args:
		filepath (str): path to the file
	Returns:
		lfp
	'''
    mat = scipy.io.loadmat(file)
    lfp = mat['lfp']
    return lfp

def plotting_lfp(lfps):
    '''
    Plot lfp in matplotlib
    Args:
		lfps: dictionary
	Returns:
		plot
    '''
    y_ticks_list = []
    yx=1
    fig, ax = plt.subplots()
    keys = list(lfps.keys())
    keys.sort()
    for i in keys:
        yx += 1
        plt.plot(np.array(lfps[i]) + yx*(1e1-1))
        # y_ticks_list.append(i[7:20])
    plt.legend([key[7:20] for key in keys])
    # ax.set_yticklabels(y_ticks_list)
    plt.show()

def plot_bokeh(lfps):
    '''
    Plot lfp in bokeh
    Args:
        lfps: dictionary
    Returns:
		plot
	'''
    colors = ['black', 'red', 'green', 'blue', 'indigo', 'crimson', 'orange', 'gold', 'gray', 'maroon', 'navy',
              'purple', 'olive', 'cyan', 'brown', 'lime']
    keys = list(lfps.keys())
    keys.sort()
    yx = 1
    legend = []

    p = figure(title='График данных', x_axis_label='X', y_axis_label='Y')

    for i, key in enumerate(keys):
        y = np.array(lfps[key]) + yx * 1e-10
        x = np.arange(len(lfps[key]))
        p.line(x, y, line_width=2, legend_label=str(i), color=colors[i])
        yx += 1

    p.legend.location = 'top_left'

    show(p)


def main():
    lfp_cc = load_cc_lfp(file)
    lfp_mat = load_matfile(matfile)
    # plotting_lfp(lfp_cc)
    plot_bokeh(lfp_cc)

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

    #Kolmogorov-Smirnov test
    result = ks_2samp(values[0], mat_data[0])

    #Comparison of averages
    mat_data = np.concatenate(mat_data)
    values = np.concatenate(values)

    mean_cc = st.mean(values)
    mean_bio = st.mean(mat_data)

    print(result)
    print("Среднее значение в lfp_cc " + str(mean_cc))
    print("Среднее значение в lfp_mat " + str(mean_bio))


if __name__ == "__main__":
    main()