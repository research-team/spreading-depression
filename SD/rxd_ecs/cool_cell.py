from mpi4py import MPI
from neuron import h, rxd
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

# mpiexec -n 1 nrniv -mpi -python cell_sd.py
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
rxd.nthread()


rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.load_file('import3d.hoc')
h.celsius = 37
numpy.random.seed(6324555+pcid)





outdir = os.path.abspath('tests/393')






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

 
Kceil = 15.0 

Rm = 28000 # Ohm.cm^2 (Migliore value)
cm = 1.2
Ra = 150
class Neuron:

    def __init__(self, file):

        self.cell = h.Import3d_SWC_read()
        self.cell.input(file)
        h.Import3d_GUI(self.cell, 0)
        self.i3d = h.Import3d_GUI(self.cell, 0)
        self.i3d.instantiate(self)
        for sec in self.all:
            sec.nseg = 1 + 10 * int(sec.L / 5)
            for mechanism in ['extracellular','Nasoma','Ksoma' ]:
                sec.insert(mechanism)
        #h.topology()   

        self.soma = self.dend[1](0.5)
        '''
        self.soma.IA.gkAbar = 0.0165
        self.soma.Ih.gkhbar = 0.00035*0.1
        self.soma.Nasoma.gnasoma = 0.0107*1.2
        self.soma.Nasoma.gl = 1/Rm
        self.soma.Nasoma.el = -67
        self.soma.Ksoma.gksoma = 0.0319*1.5
        self.soma.h.ghdbar = 0.00005
        self.soma.h.vhalfl = -73
        self.soma.Ih.gkhbar = 0.00035*0.1
        self.soma.km.gbar = 0.06
        self.soma.hha2.gnabar = 0.007
        self.soma.hha2.gkbar = 0.007/10
        self.soma.hha2.gl = 0
        self.soma.hha2.el = -70
        self.soma.Nafcr.gnafbar = 0.015
        self.soma.kdrcr.gkdrbar = 0.018
        self.soma.IKscr.gKsbar = 0.000725
        '''
        self.somaV = h.Vector()
        self.somaV.record(self.dend[1](0.5)._ref_v)
        self.k_vec = h.Vector().record(self.dend[1](0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend[1](0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend[1](0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend[1](0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.dend[1](0.5)._ref_vext[0])
        
        for sec in self.all:        
            Ra = 150
            cm = 1.2

        self.cyt = rxd.Region(h.allsec(), name='cyt', nrn_region='i', dx=0.17)
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=14)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=120)
        self.k_i= self.k[self.cyt]

    def extrema(self):
        xlo = ylo = zlo = xhi = yhi = zhi = None
        for sec in self.all:
            n3d = sec.n3d()
            xs = [sec.x3d(i) for i in range(n3d)]
            ys = [sec.y3d(i) for i in range(n3d)]
            zs = [sec.z3d(i) for i in range(n3d)]
            my_xlo, my_ylo, my_zlo = min(xs), min(ys), min(zs)
            my_xhi, my_yhi, my_zhi = max(xs), max(ys), max(zs)
            if xlo is None:
                xlo, ylo, zlo = my_xlo, my_ylo, my_zlo
                xhi, yhi, zhi = my_xhi, my_yhi, my_zhi
            else:
                xlo, ylo, zlo = min(xlo, my_xlo), min(ylo, my_ylo), min(zlo, my_zlo)
                xhi, yhi, zhi = max(xhi, my_xhi), max(yhi, my_yhi), max(zhi, my_zhi)
        return (xlo, ylo, zlo, xhi, yhi, zhi)

sys.stdout.write('\nrun')
sys.stdout.flush()

cell = Neuron('2014-06-24-N2_All.CNG.swc')
rxd.set_solve_type(h.allsec(), dimension=3)
stim = h.IClamp(cell.soma)
stim.delay = 150
stim.dur = 1
stim.amp = 1

time = h.Vector().record(h._ref_t)

xlo, ylo, zlo, xhi, yhi, zhi = cell.extrema()
padding = 50
ecs = rxd.Extracellular(xlo - padding, ylo - padding, zlo - padding,
                        xhi + padding, yhi + padding, zhi + padding,
                        dx=10, volume_fraction=alpha, tortuosity=tort) 

k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=lambda nd: 50 
                if nd.x3d**2 + nd.y3d**2 + nd.z3d**2 < r0**2 else 3,
                ecs_boundary_conditions=3)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=142,
                 ecs_boundary_conditions=142)

h.finitialize(-70 * mV)
'''
mpiexec -n 1 nrniv -mpi -python cool_cell.py
numprocs=1
NEURON -- VERSION 7.8.0-5-g80a4bfbb master (80a4bfbb) 2019-11-01
Duke, Yale, and the BlueBrain Project -- Copyright 1984-2019
See http://neuron.yale.edu/neuron/credits

Additional mechanisms from files
 bgka.mod cad.mod cadyn.mod cadyn_new.mod cagk.mod calH.mod cal.mod cancr.mod car.mod cat.mod ccanl.mod gskch.mod hha2.mod hha_old.mod h.mod hNa.mod IA.mod iccr.mod Ih.mod Ihvip.mod ikscr.mod kadistcr.mod kad.mod ka.mod kap.mod Kaxon.mod kca.mod Kdend.mod kdrcr.mod kdr.mod kleck.mod km.mod kslow.mod Ksoma.mod LcaMig.mod na3.mod Naaxon.mod Nadend.mod nafcr.mod NapIn.mod nap.mod Nasoma.mod nca.mod nmda.mod

runOne point section Import3d_Section[2] ending at line 48 has been removed
    and child Import3d_Section[3] reattached
    and child Import3d_Section[4] reattached
11
12
13
14
15
--------------------------------------------------------------------------
mpiexec noticed that process rank 0 with PID 0 on node kseniia-pc exited on signal 9 (Killed).
--------------------------------------------------------------------------

'''
#sys.stdout.write('\ninit')
#sys.stdout.flush()

def progress_bar(tstop, size=40):
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()



def plot_image_data(data, min_val, max_val, filename, title):
    """Plot a 2d image of the data"""
    sb = scalebar.ScaleBar(1e-6)
    sb.location='lower left'
    pyplot.imshow(data, extent=k[ecs].extent('xy'), vmin=min_val,
                  vmax=max_val, interpolation='nearest', origin='lower')
    pyplot.colorbar()
    sb = scalebar.ScaleBar(1e-6)
    sb.location='lower left'
    ax = pyplot.gca()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.add_artist(sb)
    pyplot.title(title)
    pyplot.xlim(k[ecs].extent('x'))
    pyplot.ylim(k[ecs].extent('y'))
    pyplot.savefig(os.path.join(outdir,filename))
    pyplot.close()


def plot_cell( filename):
    somaV, dendV, pos = [], [], []
    
    fin = open(os.path.join(outdir,'membrane_potential.pkl'),'rb')
    [sV, dV, p] = pickle.load(fin)
    fin.close()
    somaV.extend(sV) #list
    dendV.extend(dV) #list
    pos.extend(p) #list.len()=3

     
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
   
    

    cmap = pyplot.get_cmap('jet')
    
    x = pos
    soma_z = [x[2]-somaR,x[2]+somaR]
    cell_x = [x[0],x[0]]
    cell_y = [x[1],x[1]]
    scolor = cmap((somaV[0]+70.0)/70.0)
    # plot the soma
    ax.plot(cell_x, soma_z, linewidth=2, color=scolor, 
            alpha=0.5)

    dcolor = cmap((dendV[0]+70.0)/70.0)
    dend_z = [x[2]-somaR, x[2]-somaR - dendL]
    # plot the dendrite
    ax.plot(cell_x, dend_z, linewidth=0.5, color=dcolor, 
            alpha=0.5)
    ax.plot(0,0, color='g', marker='*' )
    ax.plot(10,20, color='y', marker='*')
    ax.plot(20,50, color='r', marker='*')
    ax.set_xlim([-Lx/2,Lx/2])
    ax.set_ylim([-Lz/2,Lz/2])

    norm = colors.Normalize(vmin=-70,vmax=0)

    filename = filename+'.png'
    pyplot.grid()
    pyplot.savefig(os.path.join(outdir,filename))
    pyplot.close()

h.dt=1

def run(tstop):
    print(1)
    if pcid == 0:
        fout = open(os.path.join(outdir,'wave_progress.txt' ),'a')
    while pc.t(0) <= tstop:
        if int(pc.t(0)) % 100 == 0 and pcid == 0:
            
            plot_image_data(k[ecs].states3d.mean(2), 3.5, 40,
                        'k_mean_%05d' % int(pc.t(0)/100),
                        'Potassium concentration; t = %6.0fms'
                        % pc.t(0))
        if pcid == 0: progress_bar(tstop)

        pc.psolve(pc.t(0) + h.dt)
    sys.stdout.write('\ndone, wait\n')
    sys.stdout.flush()
    exit(0)

run(300)
