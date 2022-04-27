import json
import matplotlib.pyplot as plt
import os
import csv


data = []
with open('./results/plot_spike_time.json', 'r', encoding='utf-8') as fh:
    data = json.loads(fh.read())

color = ['red', 'blue', 'yellow', 'black', 'green']

h.finitialize(-65 * mV)
h.continuerun(100 * ms)

for cell in data['cells']:
    spike_times = [h.Vector() for nc in cell.netcons]
    for nc, spike_times_vec in zip(netcons, spike_times):
        nc.record(spike_times_vec)

    '''2-3L'''
    if cell['id']==1 or cell['id']==2 or cell['id']==3 or cell['id']==12 or cell['id']==13:
        plt.figure()

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 0.5, 1.5, color=color[0])

    '''4L'''
    if cell['id'] == 4 or cell['id'] == 16:
        plt.figure()

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 1.5, 2.5, color=color[1])

    '''5L'''
    if cell['id'] == 5 or cell['id'] == 6:
        plt.figure()

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 2.5, 3.5, color=color[2])

    '''5-6L'''
    if cell['id'] == 7 or cell['id'] == 8 or cell['id'] == 9:
        plt.figure()

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 2.5, 4.5, color=color[3])

    '''6L'''
    if cell['id'] == 10:
        plt.figure()

        for i, spike_times_vec in enumerate(spike_times):
            plt.vlines(spike_times_vec, 3.5, 4.5, color=color[4])

    plt.show()

