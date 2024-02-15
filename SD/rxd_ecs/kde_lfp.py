import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from itertools import chain

flatten = chain.from_iterable
Y_OFFSET = 1000

layers=[]
data = {}
with os.scandir(r'C:\Users\User\OneDrive\Рабочий стол\последние результаты') as it:
    for entry in it:
        if entry.name.endswith(".hdf5") and entry.is_file():
            with h5py.File(entry.path, 'r') as f:
                data[entry.name] = np.array(f[list(f.keys())[0][:]])
                list_keys = list(data.keys())
                list_keys.sort()

list_data = list(data.items())
voltages_data = np.array(list_data)

def peak_finding(layers_data, dstep, border_time, border_ampl, debug = False):

    layers_num, _  = layers_data.shape

    peaks_time= [[] for _ in range(layers_num)]
    peaks_ampl = [[] for _ in range(layers_num)]
    peaks_chan = [[] for _ in range(layers_num)]

    for index, layer in layers_data:
        e_max_inds, e_max_vals = find_extrema(layer, np.greater)
        e_min_inds, e_min_vals =  find_extrema(layer, np.less)

        offset = slice(1, None) if e_min_inds[0] < e_max_inds[0] else slice(None)
        comb = list(zip(e_max_vals, e_min_inds[offset]))

        max_value_peaks = []

        for max_index, min_index in comb:
            max_value = e_max_vals[e_max_inds == max_index]
            min_value = e_min_vals[e_min_inds == min_index]
            dT = abs(max_index - min_index) * dstep
            dA = abs(max_value - min_value)

            if (border_time[0] <= dT <= border_time[1]) and border_ampl[0] <= dA <= border_ampl[1]:
                peaks_time[index].append(max_index)
                peaks_ampl[index].append(dA)
                peaks_chan[index].append(index)
                max_value_peaks.append(max_value)
        if debug:
            xticks = np.arange(len(layer)) * dstep
            y_offset = index * Y_OFFSET
            # plot the curve
            plt.plot(xticks, layer, color='k')
            # plot the extrema
            plt.plot(e_max_inds * dstep, e_max_vals, '.', color='r')
            plt.plot(e_min_inds * dstep, e_min_vals , '.', color='b')
            # plot the peaks
            x = np.asarray(peaks_time[int(index.rsplit('_')[1])]) * dstep
            y = np.asarray(max_value_peaks) + np.asarray(peaks_chan[int(index.rsplit('_')[1])]) * Y_OFFSET
            plt.plot(x, y, '.', color='g', ms=20)

        if debug:
            plt.show()

        return np.asarray(peaks_time), np.asarray(peaks_ampl), np.asarray(peaks_chan)

def find_extrema(array, condition):
    indexes = np.ndarray
    for i in array:
        indexes = argrelextrema(array, condition)[0]
        if len(indexes) == 0:
            return None, None

    values = array[indexes]
    diff_nearby_extrema = np.abs(np.diff(values, n=1))
    indexes = np.array([index for index, diff in zip(indexes, diff_nearby_extrema) if diff > 0] + [indexes[-1]])
    values = array[indexes]
    return indexes, values

# def plot_3d_density(X, Y, xmin, xmax, ymin, ymax, factor=8, filepath=None):



layers = [0,15]
dstep=0.025
border_time = [0.1, 3] #???
border_ampl = [100, np.inf]

peaks_time, peaks_ampl, peaks_lay = peak_finding(voltages_data, dstep, border_time, border_ampl, debug=True)

x_data = np.array(list(flatten(peaks_time))) * dstep
y_data = np.array(list(flatten(peaks_lay)))
z_data = np.array(list(flatten(peaks_ampl)))





