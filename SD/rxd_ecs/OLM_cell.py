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
import matplotlib.pyplot as plt
from neuron import gui
'''

    Oriens-lacunosum moleculare (OLM) cells are a major subclass of hippocampal interneurons 
    involved in controlling synaptic plasticity in Shaffer collateral synapses 
    and electrogenesis in pyramidal cell (PC) dendrites. 

see more in here: https://www.frontiersin.org/articles/10.3389/fncel.2015.00201/full

for run : mpiexec -n 1 nrniv -mpi -python OLM_cell.py 
'''

pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
rxd.nthread()


rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37
numpy.random.seed(6324555+pcid)

outdir = os.path.abspath('tests/305')


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

h_gbar=0.0025
ihscale=1.0
erevh = -30.0


somaR = 5
somaL = 20  
dendR = 1.5  
dendL = 250 
axonL = 150
axonR =  1.5/2

alpha = 0.2  
tort = 1.6  
r0 = 1000
x, y, z =0, 0, 30
Lx, Ly, Lz = 1500, 1500, 1000 
Kceil = 15.0 

Rm = 1/5e-05  # Ohm.cm^2 (Migliore value) or 20000*2
gka_soma = 0.0075
gh_soma  = 0.00005
Ra = 150
cm = 1.6

class Neuron:

    def __init__(self):

        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(0,0,0,10)
        self.soma.pt3dadd(15,0,0,10)
        self.soma.L = 20
        self.soma.diam = 10

        self.dend1 = h.Section(name='dend1', cell=self)
        self.dend1.pt3dclear()
        self.dend1.pt3dadd(15,0,0,3)
        self.dend1.pt3dadd(90,0,0,3)
        self.dend1.L = 250
        self.dend1.diam = 3
        self.dend1.nseg = 10
        self.dend1.connect(self.soma, 1, 0)

        self.dend2 = h.Section(name='dend2', cell=self)
        self.dend2.pt3dclear()
        self.dend2.pt3dadd(0,0,0,3)
        self.dend2.pt3dadd(-74,0,0,3)
        self.dend2.L = 250
        self.dend2.diam = 3
        self.dend2.nseg = 10
        self.dend2.connect(self.soma, 0, 0)

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(15,0,0,1.3)
        self.axon.pt3dadd(15,120,0,1.5)
        self.axon.L = 150
        self.axon.diam = 1.5
        self.axon.nseg = 10
        self.axon.connect(self.soma, 1, 0)

        
        h.topology()
        #h.PlotShape(False).plot(plt)
        

        self.all = [self.soma, self.dend1, self.dend2, self.axon]
        print(1)
        #---------------soma----------------
        for mechanism_s in [ 'IA', 'Ih','Nasoma','Ksoma']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).IA.gkAbar = 0.0165
        self.soma(0.5).Ih.gkhbar = 0.00035*0.1
        self.soma(0.5).Nasoma.gnasoma = 0.0107*1.2
        self.soma(0.5).Nasoma.gl = 1/Rm
        self.soma(0.5).Nasoma.el = -67
        self.soma(0.5).Ksoma.gksoma = 0.0319*1.5
        #print(self.soma.psection())
        self.n_Ksoma = h.Vector().record(self.soma(0.5).Ksoma._ref_n)
        self.h_Nasoma = h.Vector().record(self.soma(0.5).Nasoma._ref_h)
        self.m_Nasoma = h.Vector().record(self.soma(0.5).Nasoma._ref_m)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)
        '''
            {'point_processes': {}, 'density_mechs': {
            'IA': {'gkAbar': [0.0165], 'ik': [0.0], 'a': [0.0], 'b': [0.0]}, 
            'Ih': {'gkhbar': [3.5000000000000004e-05], 'ih': [0.0], 'r': [0.0]}, 
            'Ksoma': {'gksoma': [0.04785], 'ik': [0.0], 'n': [0.0]}, 
            'Nasoma': {'gnasoma': [0.012839999999999999], 'gl': [5e-05], 'el': [-67.0], 'ina': [0.0], 'il': [0.0], 'm': [0.0], 'h': [0.0]}}, 'ions': {'na': {'ena': [50.0], 'nai': [10.0], 'nao': [140.0], 'ina': [0.0], 'dina_dv_': [0.0]}, 'k': {'ek': [-77.0], 'ki': [54.4], 'ko': [2.5], 'ik': [0.0], 'dik_dv_': [0.0]}, 'h': {'eh': [0.0], 'hi': [1.0], 'ho': [1.0], 'ih': [0.0], 'dih_dv_': [0.0]}}, 'morphology': {'L': 20.0, 'diam': [10.0], 'pts3d': [(0.0, 0.0, 0.0, 10.0), (20.0, 0.0, 0.0, 10.0)], 'parent': None, 'trueparent': None}, 'nseg': 1, 'Ra': 35.4, 'cm': [1.0], 'regions': set(), 'species': set(), 'name': '<__main__.Neuron object at 0x7faabfacc048>.soma', 'hoc_internal_name': '__nrnsec_0x5628921c9100', 'cell': <__main__.Neuron object at 0x7faabfacc048>}

         '''
        print(2)
        #---------------dends----------------
        for mechanism_d in [ 'IA','Nadend','Kdend']:
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
#-----------------------dend1------------------------
        self.dend1(0.5).IA.gkAbar = 0.004*1.2
        #self.dend1(0.5).Ih.gkhbar = 0.00035*0.1
        self.dend1(0.5).Nadend.gnadend = 2*0.0117
        self.dend1(0.5).Nadend.gl = 1/Rm
        self.dend1(0.5).Nadend.el = -65
        self.dend1(0.5).Kdend.gkdend = 20*0.023

        self.D1n_Kdend = h.Vector().record(self.dend1(0.5).Kdend._ref_n)
        self.D1h_Nadend = h.Vector().record(self.dend1(0.5).Nadend._ref_h)
        self.D1m_Nadend = h.Vector().record(self.dend1(0.5).Nadend._ref_m)
        self.dendV1 = h.Vector()
        self.dendV1.record(self.dend1(0.5)._ref_v)
#-----------------------dend2------------------------
        self.dend2(0.5).IA.gkAbar = 0.004*1.2
        #self.dend1(0.5).Ih.gkhbar = 0.00035*0.1
        self.dend2(0.5).Nadend.gnadend = 2*0.0117
        self.dend2(0.5).Nadend.gl = 1/Rm
        self.dend2(0.5).Nadend.el = -65
        self.dend2(0.5).Kdend.gkdend = 20*0.023

        self.D2n_Kdend = h.Vector().record(self.dend2(0.5).Kdend._ref_n)
        self.D2h_Nadend = h.Vector().record(self.dend2(0.5).Nadend._ref_h)
        self.D2m_Nadend = h.Vector().record(self.dend2(0.5).Nadend._ref_m)

        self.dendV2 = h.Vector()
        self.dendV2.record(self.dend2(0.5)._ref_v)
        print(3)
        #--------------axon-----------------
        for mechanism in [ 'Kaxon', 'Naaxon']:
            self.axon.insert(mechanism)

        self.axon(0.5).Naaxon.gnaaxon = 0.01712
        self.axon(0.5).Naaxon.gl = 1/Rm
        self.axon(0.5).Naaxon.el = -67
        self.axon(0.5).Kaxon.gkaxon = 0.05104
        #print(self.soma.psection())
        self.n_Kaxon = h.Vector().record(self.axon(0.5).Kaxon._ref_n)
        self.h_Naaxon = h.Vector().record(self.axon(0.5).Naaxon._ref_h)
        self.m_Naaxon = h.Vector().record(self.axon(0.5).Naaxon._ref_m)

        self.axonV = h.Vector()
        self.axonV.record(self.axon(0.5)._ref_v)

        

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        
        
        for sec in self.all:        
            Ra = 150
            cm = 1
        print(4)
sys.stdout.write('\nrun')
sys.stdout.flush()



for sec in h.allsec():
    sec.nai = 4.297

#Create cell
cell = Neuron()
'''
stim = h.IClamp(cell.soma(0.5))
stim.delay = 50
stim.dur = 50
stim.amp = 1
'''
time = h.Vector().record(h._ref_t)
print(5)
ecs = rxd.Extracellular(-Lx/2.0, -Ly/2.0,
                        -Lz/2.0, Lx/2.0, Ly/2.0, Lz/2.0, dx=1,
                        volume_fraction=alpha, tortuosity=tort) 
print(6)
k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=lambda nd: 50 
                if nd.x3d**2 + nd.y3d**2 + nd.z3d**2 < r0**2 else 3,
                ecs_boundary_conditions=3)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=148,
                 ecs_boundary_conditions=148)

pc.set_maxstep(100)
h.finitialize()

sys.stdout.write('\ninit')
sys.stdout.flush()

def progress_bar(tstop, size=40):
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()



def plot_spike(volt_soma, volt_dend, t, k, na, k_in, na_in):

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
    fig.savefig(os.path.join(k_na_dir, 'spike.png'))
    pyplot.close('all')







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
        if pcid == 0 and int(pc.t(0)) % 10 == 0:
            dist = 0
            dist1 = 1e9
            for nd in k.nodes:
                r = (nd.x3d**2+nd.y3d**2+nd.z3d**2)**0.5
                if nd.concentration>Kceil and r > dist:
                    dist = r
                if nd.concentration<=Kceil and r < dist1:
                    dist1 = r
            
            fout.write("%g\t%g\t%g\n" %(pc.t(0), dist, dist1))
            fout.flush()
    #plot_image_region(cell.k.nodes.concentration, 2.5, 140, 'Potassium intracellular; t = %6.0fms' % h.t, cell.k, cell.cyt)
    print(7)
    sys.stdout.write('\ndone, wait\n')
    sys.stdout.flush()
    
    #progress_bar(tstop)
    print(8)
    if pcid == 0:
    #plot_image_region(cell.k.nodes.concentration, 2.5, 140, 'Potassium intracellular; t = %6.0fms' % h.t, cell.k, cell.cyt)
        fout.close()
        plot_spike(cell.somaV,
                    cell.dend1V,
                    time,
                    cell.k_vec,
                    cell.na_vec,
                    cell.k_concentration,
                    cell.na_concentration)
    
    
    pos = [x, y, z]
    pout = open(os.path.join(outdir,"membrane_potential.pkl"),'wb')
    pickle.dump([cell.somaV, cell.dendV, pos],pout)
    pout.close()
    pc.barrier()
    #plot_cell('cell')    
    exit(0)

run(200)
