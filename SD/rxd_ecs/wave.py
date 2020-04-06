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
# when using multiple processes get the relevant id and number of hosts
#h.nrnmpi_init()
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
root = 0

# set the save directory and if buffering or inhomogeneous tissue
# characteristics are used.

rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37

numpy.random.seed(6324555 + pcid)
outdir = os.path.abspath('tests/392(100 - 300ms)W')






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

# simulation parameters
Lx, Ly, Lz = 1000, 1000, 1000
Kceil = 15.0  # threshold used to determine wave speed
Ncell = int(9e4 * (Lx * Ly * Lz * 1e-9))
Nrec = 1000

somaR = 11.0  # soma radius
dendR = 1.4  # dendrite radius
dendL = 100.0  # dendrite length
doff = dendL + somaR

alpha0, alpha1 = 0.07, 0.2  # anoxic and normoxic volume fractions
tort0, tort1 = 1.8, 1.6  # anoxic and normoxic tortuosities
r0 = 100  # radius for initial elevated K+



Rm = 28000 # Ohm.cm^2 (Migliore value)
cm = 1.2
Ra = 150
class Neuron:

    def __init__(self, x, y, z, rec=False):
        self.x = x
        self.y = y
        self.z = z
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
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
        
        #---------------dend----------------
        
        for mechanism_d in [ 'extracellular', 'IA','Nadend','Kdend', 'Nafcr', 'IKscr', ]:
            self.dend.insert(mechanism_d)

        self.dend(0.5).IA.gkAbar = 0.004*1.2
        #self.dend1(0.5).Ih.gkhbar = 0.00035*0.1
        self.dend(0.5).Nadend.gnadend = 2*0.0117
        self.dend(0.5).Nadend.gl = 1/Rm
        self.dend(0.5).Nadend.el = -65
        self.dend(0.5).Kdend.gkdend = 20*0.023

        self.Dn_Kdend = h.Vector().record(self.dend(0.5).Kdend._ref_n)
        self.Dh_Nadend = h.Vector().record(self.dend(0.5).Nadend._ref_h)
        self.Dm_Nadend = h.Vector().record(self.dend(0.5).Nadend._ref_m)
        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        #print(numpy.array(self.k_i))
        #print(nu mpy.array(self.k.nodes.concentration)) 11 count
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        
        
        for sec in self.all:        
            Ra = 150
            cm = 1

        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        

        #self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0, geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        #self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        #self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        #self.k_i= self.k[self.cyt]
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1


  
rec_neurons = [Neuron(
    (numpy.random.random() * 2.0 - 1.0) * (Lx / 2.0 - somaR),
    (numpy.random.random() * 2.0 - 1.0) * (Ly / 2.0 - somaR),
    (numpy.random.random() * 2.0 - 1.0) * (Lz / 2.0 - somaR), 100)
    for i in range(0, int(Nrec))]

alpha = alpha1
tort = tort1


time = h.Vector().record(h._ref_t)
ecs = rxd.Extracellular(-Lx / 2.0, -Ly / 2.0,
                        -Lz / 2.0, Lx / 2.0, Ly / 2.0, Lz / 2.0, dx=(20, 20, 50),  # dx - скорость распространнения в разные стороны - различны по осям
                        volume_fraction=alpha, tortuosity=tort)


k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=lambda nd: 100
if nd.x3d ** 2 + nd.y3d ** 2 + nd.z3d ** 2 < r0 ** 2 else 3.5,
                ecs_boundary_conditions=3.5)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=142,
                 ecs_boundary_conditions=142)



kecs = h.Vector()
kecs.record(k[ecs].node_by_location(0, 0, 0)._ref_value)
pc.set_maxstep(100)

# initialize and set the intracellular concentrations
h.finitialize(-70)





def progress_bar(tstop, size=40):
    """ report progress of the simulation """
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()


def plot_rec_neurons():
    somaV, dendV, pos = [], [], []
    for i in range(nhost):
        fin = open(os.path.join(outdir, 'membrane_potential_%i.pkl' % i), 'rb')
        [sV, dV, p] = pickle.load(fin)
        fin.close()
        somaV.extend(sV)
        dendV.extend(dV)
        pos.extend(p)

        for idx in range(somaV[0].size()):
            # create a plot for each record (100ms)
            if idx % 100 ==0:
                fig = pyplot.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.set_position([0.0, 0.05, 0.9, 0.9])
                ax.set_xlim([-Lx / 2.0, Lx / 2.0])
                ax.set_ylim([-Ly / 2.0, Ly / 2.0])
                ax.set_zlim([-Lz / 2.0, Lz / 2.0])
                ax.set_xticks([int(Lx * i / 4.0) for i in range(-2, 3)])
                ax.set_yticks([int(Ly * i / 4.0) for i in range(-2, 3)])
                ax.set_zticks([int(Lz * i / 4.0) for i in range(-2, 3)])

                cmap = pyplot.get_cmap('jet')
                for i in range(Nrec):
                    x = pos[i]
                    soma_z = [x[2] - somaR, x[2] + somaR]
                    cell_x = [x[0], x[0]]
                    cell_y = [x[1], x[1]]
                    scolor = cmap((somaV[i].get(idx) + 40.0) / 80.0 )
                    # plot the soma
                    ax.plot(cell_x, cell_y, soma_z, linewidth=2, color=scolor,
                            alpha=0.5)

                    dcolor = cmap((dendV[i].get(idx) + 40.0) / 80.0)
                    dend_z = [x[2] - somaR, x[2] - somaR - dendL]
                    # plot the dendrite
                    ax.plot(cell_x, cell_y, dend_z, linewidth=0.5, color=dcolor,
                            alpha=0.5)

                norm = colors.Normalize(vmin=-70, vmax=80)
                pyplot.title('Neuron membrane potentials; t = %gms' % (idx))


                ax1 = fig.add_axes([0.88, 0.05, 0.04, 0.9])
                cb1 = colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm,
                                            orientation='vertical')
                cb1.set_label('mV')


                filename = 'neurons_{:05d}.png'.format(idx)
                pyplot.savefig(os.path.join(outdir, filename))
                pyplot.close()



def plot_image_data(data, min_val, max_val, filename, title):
    sb = scalebar.ScaleBar(1e-6)
    sb.location = 'lower left'
    pyplot.imshow(data, extent=k[ecs].extent('xy'), vmin=min_val,
                  vmax=max_val, interpolation='nearest', origin='lower')
    pyplot.colorbar()
    sb = scalebar.ScaleBar(1e-6)
    sb.location = 'lower left'
    ax = pyplot.gca()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.add_artist(sb)
    pyplot.title(title)
    pyplot.xlim(k[ecs].extent('x'))
    pyplot.ylim(k[ecs].extent('y'))
    pyplot.savefig(os.path.join(outdir, filename))
    pyplot.close()


def plot_spike(cell, time, i):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=cell.somaV, x=time, mode='lines', name='soma'))
    fig.add_trace(go.Scatter(y=cell.dendV, x=time, mode='lines', name='dendrite'))
    fig.add_trace(go.Scatter(y=cell.v_vec, x=time, mode='lines', name='v'))
    fig.update_layout(title='Voltage of Neuron %i' % i,
                   xaxis_title='ms',
                   yaxis_title='mV')
    fig.write_html(os.path.join(k_na_dir, 'spike%i.html' % i))


def plot_spike_for_1_neu(volt_soma, volt_dend, t, i, tstop, k, na, k_in, na_in, v):
    #fig, ax = pyplot.subplots()
    #ax.plot(t, volt)
    #pyplot.plot(t,volt_soma, lebel='soma')
    #pyplot.plot(t, volt_dend, lebel='dend')
    #pyplot.xticks(np.arange(0, tstop+1, 100.0))

    #pyplot.yticks(np.arange(1,15,3))
    #plt.show()
    #pyplot.grid()
    #pyplot.legend()
    #fig.savefig(os.path.join(outdir, 'spike_%i.png' % i))
    #pyplot.savefig(os.path.join(outdir, 'spike_%i.png' % i))
    #pyplot.close('all')

    fig = pyplot.figure(figsize=(40,40))
    ax1 = fig.add_subplot(5,1,1)
    soma_plot = ax1.plot(t , volt_soma , color='black', label='soma')
    dend_plot = ax1.plot(t, volt_dend, color='red', label='dend')
    ax1.legend()
    ax1.set_ylabel('mV')
   

    ax2 = fig.add_subplot(5,1,2)
    k_plot = ax2.plot(t, k, color='blue', label='K')
    na_plot = ax2.plot(t, na, color='yellow', label='Na')
    ax2.legend()
    ax2.set_ylabel('current (mA/cm$^2$)')
  

    ax3 = fig.add_subplot(5,1,3)
    k_in_plot = ax3.plot(t, k_in, color='red', label='K')
    ax3.legend()

    ax4 = fig.add_subplot(5,1,4)
    na_in_plot = ax4.plot(t, na_in, color='blue', label='Na')
    ax4.legend()
    ax4.set_xlabel('time (ms)')

    ax5 = fig.add_subplot(5,1,5)
    v=ax5.plot(t, v, color='green', label='v')
    ax5.legend()
    ax5.set_xlabel('time (ms)')
    #pyplot.savefig(os.path.join(outdir, 'spike_%i.png' % i))
    fig.savefig(os.path.join(k_na_dir, 'spike_%i.png' % i))
    pyplot.close('all')





def plot_K_ecs_in_point_000(k, t):
    pyplot.plot(t, k)
    pyplot.grid()
    pyplot.savefig(os.path.join(outdir, 'k_ecs.png'))
    pyplot.close('all')



def plot_n_m_h(t, soma , i):
    fig = pyplot.figure(figsize=(20,16))
    ax1 = fig.add_subplot(1,1,1)
    n_plot = ax1.plot(t , soma.nvec , color='red', label='n (in soma)')
    h_plot = ax1.plot(t , soma.hvec, color='blue', label='h (in soma)')
    ax1.legend()
    ax1.set_ylabel('state')


    ax1.set_xlabel('time (ms)')
    fig.savefig(os.path.join(nmh_dir, 'nmh_%i.png' % i))
    pyplot.close('all')
   
'''
    ax2 = fig.add_subplot(2,1,2)
    nhh_plot = ax2.plot(t , nhh , color='black', label='n')
    mhh_plot = ax2.plot(t, mhh, color='red', label='m')
    hhh_plot = ax2.plot(t , hhh , color='green', label='h')
    ax2.legend()
    ax2.set_ylabel('state')
    ax2.set_xlabel('time (ms)')
    #pyplot.savefig(os.path.join(outdir, 'spike_%i.png' % i))
    fig.savefig(os.path.join(outdir, 'nmh_%i.png' % i))
    pyplot.close('all')

    n1_plot = ax1.plot(t , soma.nvec_kap , color='black', label='n cap')
    n2_plot = ax1.plot(t , soma.nvec_kdr, color='orange', label='n kdr')
    n3_plot = ax1.plot(t , soma.nvec_km , color='green', label='n km')
    ax1.legend()
    ax1.set_ylabel('state')

    ax2 = fig.add_subplot(4,1,2)
    m1_plot = ax2.plot(t , soma.mvec_nax , color='blue', label='m nax')
    m2_plot = ax2.plot(t , soma.mvec_iar, color='pink', label='m iar')
    m3_plot = ax2.plot(t , soma.mvec_ikc , color='grey', label='m ikc')
    m4_plot = ax2.plot(t , soma.mvec_cat , color='yellow', label='m cat')
    m5_plot = ax2.plot(t , soma.mvec_can , color='red', label='m can')
    m6_plot = ax2.plot(t , soma.mvec_cal , color='aqua', label='m cal')
    ax2.legend()
    ax2.set_ylabel('state')

    ax3 = fig.add_subplot(4,1,3)
    h1_plot = ax3.plot(t , soma.hvec_nax , color='blue', label='h nax')
    h2_plot = ax3.plot(t , soma.hvec_cat, color='yellow', label='h cat')
    h3_plot = ax3.plot(t , soma.hvec_can , color='red', label='h can')
    ax3.legend()
    ax3.set_ylabel('state')
'''
h.dt = 1

def run(tstop):

    
    while pc.t(0) <= tstop:
        if int(pc.t(0)) % 100 == 0:
            if pcid == 0:
                plot_image_data(k[ecs].states3d.mean(2), 3.5, 40,
                                'k_mean_%05d' % int(pc.t(0) / 100),
                                'Potassium concentration; t = %6.0fms'
                                % pc.t(0))

            
        if pcid == 0: progress_bar(tstop)
        pc.psolve(pc.t(0) + h.dt)
        
    if pcid == 0:
        progress_bar(tstop)
        for i in [0, 108] :
            plot_spike(rec_neurons[i], time , i)
            #plot_spike_for_1_neu(rec_neurons[i].somaV,
             #                   rec_neurons[i].dendV,
              #                  time,
               #                 i,
                #                tstop, rec_neurons[i].k_vec,
                 #               rec_neurons[i].na_vec,
                   #             rec_neurons[i].k_concentration,
                    #            rec_neurons[i].na_concentration, rec_neurons[i].v_vec)
            #plot_n_m_h(time,
              #          rec_neurons[i], 
               #         i)
        print("\nSimulation complete. Plotting membrane potentials")
        plot_K_ecs_in_point_000(kecs ,time)

    # save membrane potentials
    soma, dend, pos = [], [], []
    for n in rec_neurons:
        soma.append(n.somaV)
        dend.append(n.dendV)
        pos.append([n.x, n.y, n.z])
    pout = open(os.path.join(outdir, "membrane_potential_%i.pkl" % pcid), 'wb')
    pickle.dump([soma, dend, pos], pout)
    pout.close()
    pc.barrier()
    if pcid == 0:
        plot_rec_neurons()
    exit(0)


run(300)