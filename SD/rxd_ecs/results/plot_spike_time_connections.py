import matplotlib.pyplot as plt
import os
import fnmatch
from matplotlib.font_manager import FontProperties

from neuron import h
import sys

sys.path.append('../')
from neuron.units import ms, mV

h.load_file("stdgui.hoc")

h.finitialize(-65 * mV)
h.continuerun(100 * ms)
plt.figure()


def read():
    time_data_with_e = []
    time_data_without_e = []

    for file in fnmatch.filter(os.listdir('.'), 'spiketime_*.txt'):
        with open(file, 'r', encoding='utf-8') as fh:
            id = str(file).rsplit('_')[1]
            spiketime_without_e = []
            spiketime_with_e = []
            if id[-1] == 'e':
                id = int(id.rsplit('e')[0])
                for line in fh:
                    line = line.rstrip('\n\r')
                    spiketime_with_e.append(float(line))
                time_data_with_e.append((id, spiketime_with_e))
            else:
                id = int(id)
                for line in fh:
                    line = line.rstrip('\n\r')
                    spiketime_without_e.append(float(line))
                time_data_without_e.append((id, spiketime_without_e))

    return time_data_without_e, time_data_with_e


def draw_spiketimes(time_data, par):
    for j, cell in enumerate(time_data):
        spike_times = time_data[j][1]
        if cell[0] == 2 or cell[0] == 5:
            '''2-3L'''
            if cell[0] == 1 or cell[0] == 2 or cell[0] == 3 or cell[0] == 12 or cell[0] == 13:

                for i, spike_times_vec in enumerate(spike_times):
                    plt.vlines(spike_times_vec, 0.5, 1, color=par[cell[0]][1])

            '''4L'''
            if cell[0] == 4 or cell[0] == 16:

                for i, spike_times_vec in enumerate(spike_times):
                    plt.vlines(spike_times_vec, 1.5, 2.5, color=par[cell[0]][1])

            '''5L'''
            if cell[0] == 5 or cell[0] == 6:

                for i, spike_times_vec in enumerate(spike_times):
                    plt.vlines(spike_times_vec, 2.5, 3.5, color=par[cell[0]][1])

            '''5-6L'''
            if cell[0] == 7 or cell[0] == 8 or cell[0] == 9:

                for i, spike_times_vec in enumerate(spike_times):
                    plt.vlines(spike_times_vec, 2.5, 4.5, color=par[cell[0]][1])

            '''6L'''
            if cell[0] == 10:

                for i, spike_times_vec in enumerate(spike_times):
                    plt.vlines(spike_times_vec, 3.5, 4.5, color=par[cell[0]][1])

    plt.show()


def draw(time_data, time_data_e, par):
    for cell, cell_e in zip(time_data, time_data_e):
        spike_times = cell[1]
        spike_times_e = cell_e[1]
        if cell[0] == 16:
            plt.vlines(spike_times, 1, 2, color=par[cell[0]][1])
            plt.vlines(spike_times_e, 0, 1, color=par[cell[0]][1])
            break
    plt.show()


if __name__ == '__main__':
    time_data, time_data_e = read()
    par = {1: ["Bask23", "#1a7ef2"],
           2: ["Axax23", "#42d4f4"],
           3: ["LTS23", "#3a0ca3"],
           4: ["Spinstel4", "#ffba00"],
           5: ["TuftIB5", "#3cb44b"],
           6: ["TuftRS5", "#bfef45"],
           7: ["Bask56", "#c8b6ff"],
           8: ["Axax56", "#f032e6"],
           9: ["LTS56", "#911eb4"],
           10: ["NontuftRS6", "#18502b"],
           12: ["SyppyrFRB", "#f58231"],
           13: ["SyppyrRS", "#e6194B"],
           14: ["TCR", "#ffccd5"],
           15: ["nRT", "#9d4edd"],
           16: ["LTS4", "#010bfc"],
           }
    # draw_spiketimes(time_data, par)
    # draw_spiketimes(time_data_e, par)
    draw(time_data, time_data_e, par)
