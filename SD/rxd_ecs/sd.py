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

# when using multiple processes get the relevant id and number of hosts
#h.nrnmpi_init()
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
root = 0

# set the save directory and if buffering or inhomogeneous tissue
# characteristics are used.
try:
    parser = argparse.ArgumentParser(description='''Run the spreading
                                     depression simulation''')
    parser.add_argument('--tstop', nargs='?', type=float, default=200,
                        help='''duration of the simulation in ms (defaults
                        to 200ms)''')
    parser.add_argument('dir', metavar='dir', type=str,
                        help='a directory to save the figures and data')
    args = parser.parse_args()

except:
    os._exit(1)

outdir = os.path.abspath(args.dir)

#os.mkdir(os.path.join(outdir, 'K_NA')) 
k_na_dir = os.path.abspath(os.path.join(outdir, 'K_NA'))
nmh_dir = os.path.abspath(os.path.join(outdir, 'n_m_h'))
if pcid == 0 and not os.path.exists(k_na_dir):
    try:
        #os.makedirs(outdir)
        os.makedirs(k_na_dir)
        os.makedirs(nmh_dir)
    except:
        print("Unable to create the directory %r for the data and figures"
              % outdir)
        os._exit(1)

rxd.nthread(4)
rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37

numpy.random.seed(6324555 + pcid)

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

class Neuron:

    def __init__(self, x, y, z, rec=False):
        self.x = x
        self.y = y
        self.z = z

        self.soma = h.Section(name='soma', cell=self)
        # add 3D points to locate the neuron in the ECS
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        # self.dend.nseg = 10 # multiple dendrite segments
        self.dend.connect(self.soma, 1, 0)


        for mechanism_s in [ 'tnak','tnap', 'taccumulation3', 'kleak']:
            self.soma.insert(mechanism_s)

        for mechanism_d in ['tnak','tnap', 'taccumulation3', 'kleak']:
            self.dend.insert(mechanism_d)

        h.pt3dadd(x, y, z, 1000, sec=self.soma)
        h.pt3dadd(0, 0, 0, 100, sec=self.soma)

        self.soma(0.5).tnak.imax = 0
        self.dend(0.5).tnak.imax = 0
        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)
        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.time = h.Vector().record(h._ref_t)
        
        #self.spine_neu = rxd.Region([self.soma],nrn_region='i')

        #self.intracellular = rxd.Region(self.soma, name='cyt', nrn_region='i')
        #self.mem = rxd.Region(h.allsec(), name='cell_mem', geometry=rxd.membrane())
        #self.k = rxd.Species(self.intracellular, name='k', d=1, charge=1 )
        #self.na = rxd.Species(self.intracellular , name='na', d=1, charge=1)
        # intracellular
        
        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.cyt = rxd.Region([self.soma], name='cyt', nrn_region='i')
        #self.na = rxd.Species(self.cyt, name='na', charge=1)
        #self.k = rxd.Species(self.cyt, name='k', charge=1)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        #self.soma(0.5)._ref_h_
        self.nvec = h.Vector().record(self.soma(0.5).tnak._ref_n)
        self.hvec = h.Vector().record(self.soma(0.5).tnap._ref_h)
        '''
        #m
        self.mvec_cal = h.Vector().record(self.dend(0.5).cal._ref_m)
        self.mvec_can = h.Vector().record(self.dend(0.5).can._ref_m)
        self.mvec_cat = h.Vector().record(self.dend(0.5).cat._ref_m)
        self.mvec_ikc = h.Vector().record(self.dend(0.5).ikc._ref_m)
        self.mvec_iar = h.Vector().record(self.dend(0.5).iar._ref_m)
        self.mvec_nax = h.Vector().record(self.dend(0.5).nax._ref_m)
        
        #n
        self.nvec_kap = h.Vector().record(self.dend(0.5).kap._ref_n)
        self.nvec_kdr = h.Vector().record(self.dend(0.5).kdr._ref_n)
        self.nvec_km = h.Vector().record(self.dend(0.5).km._ref_n)

        #h
        self.hvec_can = h.Vector().record(self.dend(0.5).can._ref_h)
        self.hvec_cat = h.Vector().record(self.dend(0.5).cat._ref_h)
        self.hvec_nax = h.Vector().record(self.dend(0.5).nax._ref_h)

        #for soma
        self.nvec = h.Vector().record(self.soma(0.5).kdr._ref_n)
        self.hvec = h.Vector().record(self.soma(0.5).nax._ref_h)
        self.mvec = h.Vector().record(self.soma(0.5).ikc._ref_m)
        '''
    '''   
              
        self.Glu = rxd.Species(self.cyt, name='Glu', initial=0)
        self.mGluR = rxd.Species(self.cyt,name="mGluR", initial=initmGluR)
        self.Glu_mGluR = rxd.Species(self.cyt, name="Glu_mGluR", initial=0)
        self.react1 = rxd.Reaction(self.Glu + self.mGluR, self.Glu_mGluR, K1, K2)
        
        #print(it)
        self.degGlu = rxd.Species(self.cyt, name="degGlu", initial=0)
        self.react2 = rxd.Reaction(self.Glu, self.degGlu, degGluRate)
        #print(it)
        self.G = rxd.Species(self.cyt, name="G", initial=K_G)
        self.GG_mGluR = rxd.Species(self.cyt, name="GG_mGluR", initial=0)
        self.react3 = rxd.Reaction(self.Glu_mGluR + self.G, self.GG_mGluR,D5f,D5b)
        #print(it)
        self.aG = rxd.Species(self.cyt, name="aG",initial=0)
        self.react4 = rxd.Reaction(self.GG_mGluR, self.aG + self.mGluR,D6f)
        self.react5 = rxd.Reaction(self.aG, self.G, D7f)
        #print(it)
        self.PLC = rxd.Species(self.cyt, name="PLC", initial=K_PLC)
        self.aPLC_aG = rxd.Species(self.cyt, name="aPLC_aG", initial=0)
        self.react6 = rxd.Reaction(self.aG + self.PLC, self.aPLC_aG, G2f, G2b)
        #print(it)
        self.PIP2 = rxd.Species(self.cyt, name="PIP2",initial=K_PIP2)
        self.aPLC_PIP2 = rxd.Species(self.cyt, name="aPLC_PIP2",initial=0)
        self.react7 = rxd.Reaction(self.aPLC_aG+self.PIP2, self.aPLC_PIP2, kfplc, kbplc)
        #print(it)
        self.ip3 = rxd.Species(self.cyt, name="ip3",d=1.415, initial=0)
        self.react8 = rxd.Reaction(self.aPLC_PIP2,self.ip3 ,Vmax1)
        #h.setpointer(self.Glu.nodes[0]._ref_concentration,'G',self.dend)
        
        self.Glu_vec = h.Vector().record(self.soma(0.5)._ref_Glui)
        self.ip3_vec = h.Vector().record(self.soma(0.5)._ref_ip3i)

        {'point_processes': {}, 'density_mechs': {'pas': {'g': [0.001], 'e': [-70.0], 
        'i': [0.0]}, 'cagk': {'gbar': [0.01], 'ik': [0.0], 'gkca': [0.0], 'o': [0.0]}, 

        'cal': {'gcalbar': [0.003], 'ggk': [0.0], 'ica': [0.0], 'gcal': [0.0], 'minf':[0.0], 'tau': [0.0], 'm': [0.0]},
        'can': {'gcanbar': [0.0003], 'ica': [0.0], 'gcan': [0.0], 'minf': [0.0], 'hinf': [0.0], 'taum': [0.0], 'tauh': [0.0], 'm': [0.0], 'h': [0.0]},
        'cat': {'gcatbar': [0.003], 'ica': [0.0], 'gcat': [0.0], 'hinf': [0.0], 'htau':[0.0], 'minf': [0.0], 'mtau': [0.0], 'm': [0.0], 'h': [0.0]}, 
        'ikc': {'gkbar': [0.003],'taumin': [0.1], 'm_inf': [0.0], 'tau_m': [0.0], 'm': [0.0]},
        'iar': {'ghbar': [2e-05],'k2': [0.0001], 'alpha': [0.0], 'beta': [0.0], 'm': [0.0], 'c1': [0.0], 'o1': [0.0],'o2': [0.0], 'p0': [0.0], 'p1': [0.0]}, 
        'kap': {'sh': [0.0], 'gbar': [0.008], 'g': [0.0], 'n': [0.0], 'l': [0.0]}, 
        'kdr': {'gbar': [0.003], 'sh': [0.0], 'ninf': [0.0], 'g': [0.0], 'taun': [0.0], 'n': [0.0]}, 
        'km': {'gmax': [10.0], 'i': [0.0], 'gk': [0.0],'ninf': [0.0], 'ntau': [0.0], 'tadj': [0.0], 'n': [0.0]}, 
        'nax': {'sh': [0.0], 'gbar':[0.01], 'm': [0.0], 'h': [0.0]}}, 
        'ions': {'na': {'ena': [50.0], 'nai': [10.0], 'nao':[140.0], 'ina': [0.0], 'dina_dv_': [0.0]}, 
        'k': {'ek': [-77.0], 'ki': [54.4], 'ko':[2.5], 'ik': [0.0], 'dik_dv_': [0.0]}, 
        'ca': {'eca': [132.4579341637009], 'cai': [5e-05], 'cao': [2.0], 'ica': [0.0], 'dica_dv_': [0.0]}, 
        'h': {'eh': [0.0], 'hi': [1.0], 'ho': [1.0],'ih': [0.0], 'dih_dv_': [0.0]}}, 
        'morphology': {'L': 100.0, 'diam': [2.799999952316284],'pts3d': [(196.6820831298828, 30.027196884155273, 52.79754638671875, 2.799999952316284),
                    (196.6820831298828, 30.027196884155273, -47.20245361328125, 2.799999952316284)], 
                    'parent': <__main__.Neuron object at 0x7f010ee0b208>.soma(1), 'trueparent': <__main__
                    .Neuron object at 0x7f010ee0b208>.soma(1)}, 'nseg': 1, 'Ra': 35.4, 'cm': [1.0], 'regions': 
                    set(), 'species': set(), 'name': '<__main__.Neuron object at 0x7f010ee0b208>.dend',
                     'hoc_internal_name': '__nrnsec_0x256a750', 'cell': <__main__.Neuron object at 0x7f010ee0b208>}


        {'point_processes': {}, 'density_mechs': {
        'leak': {'gk': [1e-05], 'gna': [1e-05], 'gcl': [0.0001], 'ga': [0.0], 'ik': [0.0], 'ina': [0.0], 'icl': [0.0], 'ia': [0.0], 'qk': [0.0], 'qna': [0.0], 'qcl': [0.0], 'qa': [0.0]}, 
        'taccumulation3': {'c1': [0.0]}, 
        'tnak': {'gk': [5.0], 'imax': [0.0], 'ileak': [0.0], 'minf': [0.0], 'ninf': [0.0], 'taun': [0.0], 'ipump': [0.0], 'n': [0.0]}, 
        'tnap': {'gnap': [0.4], 'ina': [0.0], 'minf': [0.0], 'hinf': [0.0], 'tauh': [0.0], 'h': [0.0]}}, 
        'ions': {'na': {'ena': [50.0], 'nai': [10.0], 'nao': [140.0], 'ina': [0.0], 'dina_dv_': [0.0]}, 
        'k': {'ek': [-77.0], 'ki': [54.4], 'ko': [2.5], 'ik': [0.0], 'dik_dv_': [0.0]},
         'ca': {'eca': [132.4579341637009], 'cai': [5e-05], 'cao': [2.0], 'ica': [0.0], 'dica_dv_': [0.0]}, 
         'cl': {'ecl': [0.0], 'cli': [1.0], 'clo': [1.0], 'icl': [0.0], 'dicl_dv_': [0.0]}, 
         'a': {'ea': [0.0], 'ai': [1.0], 'ao': [1.0], 'ia': [0.0], 'dia_dv_': [0.0]}}, 
         'morphology': {'L': 596.9584103595818, 'diam': [20.875968596211216], 'pts3d': [(343.8056335449219, -50.5482063293457, -268.5406799316406, 22.0), (343.8056335449219, -50.5482063293457, -290.5406799316406, 22.0), (0.0, 0.0, 0.0, 22.0), (0.0, 0.0, 122.0, 11.0)], 'parent': None, 'trueparent': None}, 'nseg': 1, 'Ra': 35.4, 'cm': [1.0], 'regions': set(), 'species': set(), 'name': '<__main__.Neuron object at 0x7fafa6b2ed68>.soma', 'hoc_internal_name': '__nrnsec_0x3ce0cb0', 'cell': <__main__.Neuron object at 0x7fafa6b2ed68>}

    '''    
   
rec_neurons = [Neuron(
    (numpy.random.random() * 2.0 - 1.0) * (Lx / 2.0 - somaR),
    (numpy.random.random() * 2.0 - 1.0) * (Ly / 2.0 - somaR),
    (numpy.random.random() * 2.0 - 1.0) * (Lz / 2.0 - somaR), 1000)
    for i in range(0, int(Nrec))]

alpha = alpha1
tort = tort1



ecs = rxd.Extracellular(-Lx / 2.0, -Ly / 2.0,
                        -Lz / 2.0, Lx / 2.0, Ly / 2.0, Lz / 2.0, dx=10,  # dx - скорость распространнения в разные стороны - различны по осям
                        volume_fraction=alpha, tortuosity=tort)


k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=lambda nd: 40
if nd.x3d ** 2 + nd.y3d ** 2 + nd.z3d ** 2 < r0 ** 2 else 3.5,
                ecs_boundary_conditions=3.5)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=133.574,
                 ecs_boundary_conditions=133.574)



kecs = h.Vector()
kecs.record(k[ecs].node_by_location(0, 0, 0)._ref_value)
pc.set_maxstep(100)

# initialize and set the intracellular concentrations
h.finitialize()
for sec in h.allsec():
    sec.nai = 4.297




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

def plot_spike_for_1_neu(volt_soma, volt_dend, t, i, tstop, k, na, k_in, na_in):
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
    #pyplot.savefig(os.path.join(outdir, 'spike_%i.png' % i))
    fig.savefig(os.path.join(k_na_dir, 'spike_%i.png' % i))
    pyplot.close('all')





def plot_K_ecs_in_point_000(k, t):
    pyplot.plot(t, k)
    pyplot.grid()
    pyplot.savefig(os.path.join(outdir, 'k_ecs.png'))
    pyplot.close('all')



def plot_n_m_h(t, soma , i):
    fig = pyplot.figure(figsize=(20,5))
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

    if pcid == 0:
        fout = open(os.path.join(outdir, 'wave_progress.txt' ), 'a')

    while pc.t(0) <= tstop:
        if int(pc.t(0)) % 100 == 0:
            if pcid == 0:
                plot_image_data(k[ecs].states3d.mean(2), 3.5, 40,
                                'k_mean_%05d' % int(pc.t(0) / 100),
                                'Potassium concentration; t = %6.0fms'
                                % pc.t(0))

            
        if pcid == 0: progress_bar(tstop)
        pc.psolve(pc.t(0) + h.dt)
        if pcid == 0 and int(pc.t(0)) % 10 == 0:
            dist = 0
            dist1 = 1e9
            for nd in k.nodes:
                r = (nd.x3d ** 2 + nd.y3d ** 2 + nd.z3d ** 2) ** 0.5
                if nd.concentration > Kceil and r > dist:
                    dist = r
                if nd.concentration <= Kceil and r < dist1:
                    dist1 = r

            fout.write("%g\t%g\t%g\n" % (pc.t(0), dist, dist1))
            fout.flush()
    if pcid == 0:
        progress_bar(tstop)
        fout.close()
        for i in range(200) :
            plot_spike_for_1_neu(rec_neurons[i].somaV,
                                rec_neurons[i].dendV,
                                rec_neurons[i].time,
                                i,
                                tstop, rec_neurons[i].k_vec,
                                rec_neurons[i].na_vec,
                                rec_neurons[i].k_concentration,
                                rec_neurons[i].na_concentration)
            plot_n_m_h(rec_neurons[i].time,
                        rec_neurons[i], 
                        i)
        print("\nSimulation complete. Plotting membrane potentials")
        plot_K_ecs_in_point_000(kecs ,rec_neurons[0].time)

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



run(args.tstop)
