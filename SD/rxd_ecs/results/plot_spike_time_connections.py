import matplotlib.pyplot as plt
import os
import fnmatch

from neuron import h
import sys
sys.path.append('../')
from neuron.units import ms, mV

h.load_file("stdgui.hoc")
data = []

for file in fnmatch.filter(os.listdir('.'), 'spiketime_*.txt'):
    with open(file, 'r', encoding='utf-8') as fh:
        id = int(str(file).rsplit('_')[1])
        spiketime = []
        for line in fh:
            line = line.rstrip('\n\r')
            spiketime.append(float(line))
        data.append((id, spiketime))

color = ['red', 'blue', 'yellow', 'black', 'green']

h.finitialize(-65 * mV)
h.continuerun(100 * ms)
plt.figure()
for j, cell in enumerate(data):
    spike_times = data[j][1]

    '''2-3L'''
    if cell[0] == 1 or cell[0] == 2 or cell[0] == 3 or cell[0] == 12 or cell[0] == 13:

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 0.5, 1.5, color=color[0])

    '''4L'''
    if cell[0] == 4 or cell[0] == 16:

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 1.5, 2.5, color=color[1])

    '''5L'''
    if cell[0] == 5 or cell[0] == 6:

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 2.5, 3.5, color=color[2])

    '''5-6L'''
    if cell[0] == 7 or cell[0] == 8 or cell[0] == 9:

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 2.5, 4.5, color=color[3])

    '''6L'''
    if cell[0] == 10:

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 3.5, 4.5, color=color[4])

plt.show()
