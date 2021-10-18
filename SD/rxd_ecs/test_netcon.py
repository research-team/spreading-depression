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
from neuron.units import ms, mV
from matplotlib import pyplot, animation
from IPython.display import HTML
from cells import *
import plotly.graph_objects as go
h.nrnmpi_init()
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
#rxd.nthread()


rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37
numpy.random.seed(6324555+pcid)





outdir = os.path.abspath('tests/509-netcon')






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
r0 = 1000
x, y, z =0, 0, 30
Lx, Ly, Lz = 1000, 1000, 1000
Kceil = 15.0 



sys.stdout.write('\nrun')
sys.stdout.flush()

#, Axax23(1,1,1), LTS23(2,2,2), Spinstel4(4,4,4), TuftIB5(5,5,5), TuftRS5(6,6,6), Bask56(7,7,7), Axax56(8,8,8), LTS56(9,9,9), NontuftRS6(10,10,10)]




#Create cell



cells = [Bask23(0,0,0),  Spinstel4(100,50,50) ]
time = h.Vector().record(h._ref_t)
cells[0].conect(cells[1])

stim = h.IClamp(cells[0].soma(0.5))
stim.delay = 50
stim.dur = 10
stim.amp = 10


ecs = rxd.Extracellular(-Lx/2.0, -Ly/2.0,
                        -Lz/2.0, Lx/2.0, Ly/2.0, Lz/2.0, dx=20,
                        volume_fraction=alpha, tortuosity=tort) 

k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=lambda nd: 13 
                if nd.x3d**2 + nd.y3d**2 + nd.z3d**2 < r0**2 else 3,
                ecs_boundary_conditions=3)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=135,
                 ecs_boundary_conditions=135)

ca = rxd.Species(ecs, name='ca', d=0.08, charge=2, initial=25,
                 ecs_boundary_conditions=25)



pc.set_maxstep(100)

h.finitialize(-70)


sys.stdout.write('\ninit')
sys.stdout.flush()

def progress_bar(tstop, size=40):
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()



def plot_spike(volt_soma, volt_dend,t, k, na, k_in, na_in, name, axonV, v):

    fig = pyplot.figure(figsize=(20,16))
    ax1 = fig.add_subplot(4,1,1)
    soma_plot = ax1.plot(t , volt_soma , color='black', label='soma')
    dend_plot = ax1.plot(t, volt_dend, color='red', label='dend')
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





h.dt=1

def run(tstop):
        
    while pc.t(0) <= tstop:  
        if pcid == 0: progress_bar(tstop)
        pc.psolve(pc.t(0) + h.dt)
    if pcid == 0:
        i=0
        for cell in cells:
            i=i+1
            plot_spike(cell.somaV,
                        cell.dendV,
                        time,
                        cell.k_vec,
                        cell.na_vec,
                        cell.k_concentration,
                        cell.na_concentration, i, cell.axonV, cell.v_vec)
            plot_spike_html(cell, time, i)
            #plot_nmh("nmh_in_dend", cell.nmh_list_dend, time)
            #plot_nmh("nmh_in_axon", cell.nmh_list_axon, time)
        sys.stdout.write('Simulation complete. Plotting membrane potentials')
        sys.stdout.flush()
      
    pc.barrier()
    exit(0)

run(200)