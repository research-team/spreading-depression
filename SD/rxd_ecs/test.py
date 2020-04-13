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
# mpiexec -n 1 nrniv -mpi -python cell_sd.py
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
rxd.nthread()


rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37
numpy.random.seed(6324555+pcid)





outdir = os.path.abspath('tests/500')






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
r0 = 60
x, y, z =0, 0, 30
Lx, Ly, Lz = 100, 100, 100 
Kceil = 15.0 



sys.stdout.write('\nrun')
sys.stdout.flush()

cells = [Bask23(0,0,0), Axax23(1,1,1), LTS23(2,2,2), Spinstel4(4,4,4), TuftIB5(5,5,5), TuftRS5(6,6,6), Bask56(7,7,7), Axax56(8,8,8), LTS56(9,9,9), NontuftRS6(10,10,10)]



for sec in h.allsec():
    sec.nai = 4.297

#Create cell


stim = h.IClamp(cell.soma(0.5))
stim.delay = 150
stim.dur = 1
stim.amp = 1

time = h.Vector().record(h._ref_t)

ecs = rxd.Extracellular(-Lx/2.0, -Ly/2.0,
                        -Lz/2.0, Lx/2.0, Ly/2.0, Lz/2.0, dx=1,
                        volume_fraction=alpha, tortuosity=tort) 

k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=lambda nd: 50 
                if nd.x3d**2 + nd.y3d**2 + nd.z3d**2 < r0**2 else 3,
                ecs_boundary_conditions=3)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=142,
                 ecs_boundary_conditions=142)


h.finitialize(-70 * mV)

sys.stdout.write('\ninit')
sys.stdout.flush()

def progress_bar(tstop, size=40):
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()



def plot_spike(volt_soma, volt_dend, k, na, k_in, na_in, name):

    fig = pyplot.figure(figsize=(20,16))
    ax1 = fig.add_subplot(4,1,1)
    soma_plot = ax1.plot(t , volt_soma , color='black', label='soma')
    dend_plot = ax1.plot(t, volt_dend, color='red', label='dend')
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








h.dt=1

def run(tstop):
        
    while pc.t(0) <= tstop:  
        if pcid == 0: progress_bar(tstop)
        pc.psolve(pc.t(0) + h.dt)
    if pcid == 0:
        for cell in cells:
            plot_spike(cell.somaV,
                        cell.dendV,
                        time,
                        cell.k_vec,
                        cell.na_vec,
                        cell.k_concentration,
                        cell.na_concentration, cell.id)
        
        sys.stdout.write('Simulation complete. Plotting membrane potentials')
        sys.stdout.flush()
      
    pc.barrier()
    exit(0)

run(200)