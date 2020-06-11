import random
import pandas as pd
import plotly.express as px
from mpi4py import MPI
from neuron import h, crxd as rxd
from neuron.crxd import rxdmath
from matplotlib import pyplot, colors, colorbar
from matplotlib_scalebar import scalebar
from mpl_toolkits.mplot3d import Axes3D
import numpy
import argparse
import os
import sys
import pickle
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from cells import *
import json



h.nrnmpi_init()
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
root = 0


#time =300
rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37

numpy.random.seed(6324555 + pcid)





outdir = os.path.abspath('tests/748_c4')






k_na_dir = os.path.abspath(os.path.join(outdir, 'K_NA'))
nmh_dir = os.path.abspath(os.path.join(outdir, 'n_m_h'))

if not os.path.exists(k_na_dir):
    try:
        os.makedirs(outdir)
        os.makedirs(k_na_dir)
        os.makedirs(nmh_dir)
    except:
        print("Unable to create the directory %r for the data and figures"
              % outdir)
        os._exit(1)


somaR = 6.0  
dendR = 1.4  
dendL = 50.0  
doff = dendL + somaR
alpha = 0.2  
tort = 1.6  
r0 = 100
x, y, z =0, 0, 30
Lx, Ly, Lz = 1000, 1000, 1000 
Kceil = 15.0 



sys.stdout.write('\nrun')
sys.stdout.flush()

#, Axax23(1,1,1), LTS23(2,2,2), Spinstel4(4,4,4), TuftIB5(5,5,5), TuftRS5(6,6,6), Bask56(7,7,7), Axax56(8,8,8), LTS56(9,9,9), NontuftRS6(10,10,10)]




#Create cell

print(1)

cells = [Spinstel4(0,0,0,1), Spinstel4(10,24,24,2)]
time = h.Vector().record(h._ref_t)
print(2)
cells[0].connect(cells[1],1)
stim = h.NetStim()
stim.number = 1
stim.start = 50
ncstim = h.NetCon(stim, cells[0].synlistex[0])
ncstim.delay = 10
ncstim.weight[0] = 1
'''
stim1 = h.NetStim()
stim1.number = 1
stim1.start = 50
ncstim1 = h.NetCon(stim, cells[0].synlistex[1])
ncstim1.delay = 10
ncstim1.weight[0] = 1

stim2 = h.NetStim()
stim2.number = 1
stim2.start = 50
ncstim = h.NetCon(stim, cells[0].synlistex[2])
ncstim.delay = 10
ncstim.weight[0] = 1
'''
print(3)

ecs = rxd.Extracellular(-Lx/2.0, -Ly/2.0,
                        -Lz/2.0, Lx/2.0, Ly/2.0, Lz/2.0, dx=20,
                        volume_fraction=alpha, tortuosity=tort) 

k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=1,
                ecs_boundary_conditions=1)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=145,
                 ecs_boundary_conditions=145)

ca = rxd.Species(ecs, name='ca', d=0.08, charge=2, initial=25,
                 ecs_boundary_conditions=25)

pc.set_maxstep(100)
h.finitialize()


sys.stdout.write('\ninit')
sys.stdout.flush()
print(4)
def progress_bar(tstop, size=40):
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()



def plot_spike(volt_soma, volt_dend,t, k, na, k_in, na_in, name, axonV, v, d1):

    fig = pyplot.figure(figsize=(20,16))
    ax1 = fig.add_subplot(4,1,1)
    soma_plot = ax1.plot(t , volt_soma , color='black', label='soma')
    dend_plot = ax1.plot(t, volt_dend, color='red', label='dend')
    dend_plot1 = ax1.plot(t, d1, color='yellow', label='dend1')
    axon_plot = ax1.plot(t, axonV, color='blue', label='axon')
    v_plot = ax1.plot(t, v, color='green', label='v')
    ax1.legend()
    ax1.set_ylabel('mV')
   

    ax2 = fig.add_subplot(4,1,2)
    k_plot = ax2.plot(t, k, color='blue', label='K')
    na_plot = ax2.plot(t, na, color='yellow', label='Na')
    ax2.legend()
    ax2.set_ylabel('current (mA/cm$^2$)')
  

    ax3 = fig.add_subplot(4,1,3)
    k_in_plot = ax3.plot(t, k_in, color='red', label='K')
    ax3.legend()

    ax4 = fig.add_subplot(4,1,4)
    na_in_plot = ax4.plot(t, na_in, color='blue', label='Na')
    ax4.legend()
    ax4.set_xlabel('time (ms)')
    fig.savefig(os.path.join(k_na_dir, '%i.png' %name))
    pyplot.close('all')

def plot_spike_html(cell, time, i):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=cell.somaV, x=time, mode='lines', name='soma'))
    fig.add_trace(go.Scatter(y=cell.dendV, x=time, mode='lines', name='dendrite'))
    fig.add_trace(go.Scatter(y=cell.dendV1, x=time, mode='lines', name='dendrite1'))
    fig.add_trace(go.Scatter(y=cell.dendV2, x=time, mode='lines', name='dendrite2'))
    fig.add_trace(go.Scatter(y=cell.dendV3, x=time, mode='lines', name='dendrite3'))
    fig.add_trace(go.Scatter(y=cell.dendV4, x=time, mode='lines', name='dendrite4'))
    fig.add_trace(go.Scatter(y=cell.v_vec, x=time, mode='lines', name='v'))
    fig.add_trace(go.Scatter(y=cell.axonV, x=time, mode='lines', name='axon'))
    fig.update_layout(title='Voltage of Neuron %i' % i,
                   xaxis_title='ms',
                   yaxis_title='mV')
    fig.write_html(os.path.join(k_na_dir, 'spike%i.html' % i))

def plot_nmh(name, list, time):
    fig = go.Figure()
    for i in  range(len(list)):
        fig.add_trace(go.Scatter(y=list[i], x=time, mode='lines', name='%i' %i))
    fig.update_layout(title='nmh',
                   xaxis_title='ms',
                   yaxis_title='')
    fig.write_html(os.path.join(k_na_dir, '%s.html' % name))

def plot_is(data, name, id):
    fig = go.Figure()
    for i in range(len(name)):
        fig.add_trace(go.Scatter(y=data[i], x=time, mode='lines', name=name[i]))
    fig.update_layout(title='i',
                      xaxis_title='ms',
                      yaxis_title='')
    fig.write_html(os.path.join(k_na_dir, '%s_soma.html' % id))

def plot_id(data, name, id):
    fig = go.Figure()
    for i in range(len(name)):
        fig.add_trace(go.Scatter(y=data[i], x=time, mode='lines', name=name[i]))
    fig.update_layout(title='i',
                      xaxis_title='ms',
                      yaxis_title='')
    fig.write_html(os.path.join(k_na_dir, '%s_dend.html' % id))


h.dt=0.1

def run(tstop):
        
    while pc.t(0) <= tstop:  
        if pcid == 0: progress_bar(tstop)
        pc.psolve(pc.t(0) + h.dt)
    if pcid == 0:
        for cell in cells:

            d=[]
            d.append(cell.v1)
            d.append(cell.v2)
            d.append(cell.v3)
            d.append(cell.v4)
            d.append(cell.v5)
            #d.append(cell.v6)
            d.append(cell.v7)
            d.append(cell.v8)
            d.append(cell.v9)
            #d.append(cell.v10)
            d2 =[]
            d2.append(cell.vd1)
            d2.append(cell.vd2)
            d2.append(cell.vd3)
            d2.append(cell.vd4)
            d2.append(cell.vd5)
            #2 d.append(celld.v6)
            d2.append(cell.vd7)
            d2.append(cell.vd8)
            d2.append(cell.vd9)
            plot_is(d,["ina_naf2", 'ina_napf_spinstell', 'ik_kdr_fs', 'ik_ka', 'ik_kc_fast',  'ik_k2', 'ik_kahp_slower', 'ica_cal'], cell.number)
            plot_id(d2, ["ina_naf2", 'ina_napf_spinstell', 'ik_kdr_fs', 'ik_ka', 'ik_kc_fast', 'ik_k2', 'ik_kahp_slower',
                       'ica_cal'], cell.number)
            plot_spike(cell.somaV,
                        cell.dendV,
                        time,
                        cell.k_vec,
                        cell.na_vec,
                        cell.k_concentration,
                        cell.na_concentration, cell.number, cell.axonV, cell.v_vec, cell.dendV1)
            plot_spike_html(cell, time, cell.number)
            #plot_nmh("nmh_in_dend", cell.nmh_list_dend, time)
            #plot_nmh("nmh_in_axon", cell.nmh_list_axon, time)
        sys.stdout.write('Simulation complete. Plotting membrane potentials')
        sys.stdout.flush()



    pc.barrier()
    exit(0)

run(200)