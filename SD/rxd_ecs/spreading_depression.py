"""Simulation of spreading depression"""
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

pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()


try:
    parser = argparse.ArgumentParser(description = '''Run the spreading
                                     depression simulation''')
    
    parser.add_argument('--edema', dest='edema', action='store_const',
                        const=True, default=True,
                        help='''Use inhomogeneous tortuosity and volume
                        fraction to simulate edema''')
    parser.add_argument('--buffer', dest='buffer', action='store_const',
                        const=True, default=False,
                        help='Use a reaction to model astrocytic buffering')
    parser.add_argument('--tstop', nargs='?', type=float, default=200,
                        help='''duration of the simulation in ms (defaults
                        to 200ms)''')
    parser.add_argument('dir', metavar='dir', type=str,
                        help='a directory to save the figures and data')
    args = parser.parse_args()
except:
    os._exit(1)

outdir = os.path.abspath(args.dir)
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

numpy.random.seed(6324555+pcid)    

# simulation parameters
Lx, Ly, Lz = 1000, 1000, 1000     
Kceil = 15.0                       
Ncell = int(9e4*(Lx*Ly*Lz*1e-9))   
Nrec = 1000

somaR = 11.0     # soma radius
dendR = 1.4      # dendrite radius
dendL = 100.0    # dendrite length
doff = dendL + somaR

alpha0, alpha1 = 0.07, 0.2  # anoxic and normoxic volume fractions 
tort0, tort1 = 1.8, 1.2     # anoxic and normoxic tortuosities 
r0 = 100                   # radius for initial elevated K+

class Neuron:
    def __init__(self, x, y, z, rec=False):
        self.x = x
        self.y = y
        self.z = z

        self.soma = h.Section(name='soma', cell=self)
 
        self.soma.pt3dadd(x, y, z + somaR, 2.0*somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0*somaR)
    
        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dadd(x, y, z - somaR, 2.0*dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0*dendR)
        self.dend.nseg = 10 
        self.dend.connect(self.soma, 1,0)
        

        for mechanism in ['tnak', 'tnap', 'taccumulation3', 'kleak']:
            self.soma.insert(mechanism)
            self.dend.insert(mechanism)

        self.soma(0.5).tnak.imax = 0
        self.dend(0.5).tnak.imax = 0

        if rec:
            self.somaV = h.Vector()
            self.somaV.record(self.soma(0.5)._ref_v, rec)
            self.dendV = h.Vector()
            self.dendV.record(self.dend(0.5)._ref_v, rec)
        #self.cyt = rxd.Region([self.soma, self.dend], name='cyt', nrn_region='o')
        #h.pt3dadd(x, y, z, 100, sec=self.soma)
        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.cyt = rxd.Region([self.soma], name='cyt', nrn_region='i')
        #self.na = rxd.Species(self.cyt, name='na', charge=1)
        #self.k = rxd.Species(self.cyt, name='k', charge=1)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        #self.soma(0.5)._ref_h_
        self.time = h.Vector().record(h._ref_t)
        self.nvec = h.Vector().record(self.soma(0.5).tnak._ref_n)
        self.hvec = h.Vector().record(self.soma(0.5).tnap._ref_h)


rec_neurons = [Neuron(
    (numpy.random.random()*2.0 - 1.0) * (Lx/2.0 - somaR), 
    (numpy.random.random()*2.0 - 1.0) * (Ly/2.0 - somaR), 
    (numpy.random.random()*2.0 - 1.0) * (Lz/2.0 - somaR), 1)
    for i in range(0, Nrec)]



if args.edema:
    def alpha(x, y, z) :
        return (alpha0 if x**2 + y**2 + z**2 < r0**2
                else min(alpha1, alpha0 +(alpha1-alpha0)
                *((x**2+y**2+z**2)**0.5-r0)/(Lx/2)))

    def tort(x, y, z) :
        return (tort0 if x**2 + y**2 + z**2 < r0**2
                else max(tort1, tort0 - (tort0-tort1)
                *((x**2+y**2+z**2)**0.5-r0)/(Lx/2)))
else:
    alpha = alpha1
    tort = tort1



ecs = rxd.Extracellular(-Lx/2.0, -Ly/2.0,
                        -Lz/2.0, Lx/2.0, Ly/2.0, Lz/2.0, dx=10,
                        volume_fraction=alpha, tortuosity=tort) 


k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=lambda nd: 60 
                if nd.x3d**2 + nd.y3d**2 + nd.z3d**2 < r0**2 else 3.5,
                ecs_boundary_conditions=3.5)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=133.574,
                 ecs_boundary_conditions=133.574)
kecs = h.Vector()
kecs.record(k[ecs].node_by_location(0, 0, 0)._ref_value)

if args.buffer:
 
    kb = 0.0008
    kth = 15.0
    kf = kb / (1.0 + rxdmath.exp(-(k - kth)/1.15))
    Bmax = 10

    A = rxd.Species(ecs,name='buffer', charge=1, d=0,
                    initial = lambda nd: 0 if nd.x3d**2 + nd.y3d**2 + nd.z3d**2
                    < r0**2 else Bmax)
    AK = rxd.Species(ecs,name='bound', charge=1, d=0,
                    initial = lambda nd: Bmax if nd.x3d**2 + nd.y3d**2 + 
                    nd.z3d**2 < r0**2 else 0)

    buffering = rxd.Reaction(k + A, AK, kf, kb)

pc.set_maxstep(10) 

h.finitialize()
for sec in h.allsec():
    sec.nai = 4.297

def progress_bar(tstop, size=40):
    prog = h.t/float(tstop)
    fill = int(size*prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100*prog, pc.t(0), tstop))
    sys.stdout.flush()

def plot_rec_neurons():
    somaV, dendV, pos = [], [], []
    for i in range(nhost):
        fin = open(os.path.join(outdir,'membrane_potential_%i.pkl' % i),'rb')
        [sV, dV, p] = pickle.load(fin)
        fin.close()
        somaV.extend(sV)
        dendV.extend(dV)
        pos.extend(p)

        for idx in range(somaV[0].size()):  
            if idx % 100 == 0:
                fig = pyplot.figure()
                ax = fig.add_subplot(111,projection='3d')
                ax.set_position([0.0,0.05,0.9,0.9])
                ax.set_xlim([-Lx/2.0, Lx/2.0])
                ax.set_ylim([-Ly/2.0, Ly/2.0])
                ax.set_zlim([-Lz/2.0, Lz/2.0])
                ax.set_xticks([int(Lx*i/4.0) for i in range(-2,3)])
                ax.set_yticks([int(Ly*i/4.0) for i in range(-2,3)])
                ax.set_zticks([int(Lz*i/4.0) for i in range(-2,3)])
                cmap = pyplot.get_cmap('jet')
                for i in range(Nrec):
                    x = pos[i]
                    soma_z = [x[2]-somaR,x[2]+somaR]
                    cell_x = [x[0],x[0]]
                    cell_y = [x[1],x[1]]
                    scolor = cmap((somaV[i].get(idx)+40.0)/80.0)
                    ax.plot(cell_x, cell_y, soma_z, linewidth=2, color=scolor, 
                            alpha=0.5)
                    dcolor = cmap((dendV[i].get(idx)+40.0)/80.0)
                    dend_z = [x[2]-somaR, x[2]-somaR - dendL]
                    ax.plot(cell_x, cell_y, dend_z, linewidth=0.5, color=dcolor, 
                            alpha=0.5)
                norm = colors.Normalize(vmin=-70,vmax=80)
                pyplot.title('Neuron membrane potentials; t = %gms' % (idx))
     
                ax1 = fig.add_axes([0.88,0.05,0.04,0.9])
                cb1 = colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm,
                                                    orientation='vertical')
                cb1.set_label('mV')
                

                filename = 'neurons_{:05d}.png'.format(idx)
                pyplot.savefig(os.path.join(outdir,filename))
                pyplot.close()

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




h.dt = 1  

def run(tstop):
    if pcid == 0:
        name = '' if not args.edema else '_edema'
        name += '' if not args.buffer else '_buffer'
        fout = open(os.path.join(outdir,'wave_progress%s.txt' % name),'a')

    while pc.t(0) <= tstop:
        if int(pc.t(0)) % 100 == 0:
            if pcid == 0:
                plot_image_data(k[ecs].states3d.mean(2), 3.5, 60,
                                'k_mean_%05d' % int(pc.t(0)/100),
                                'Potassium concentration; t = %6.0fms'
                                % pc.t(0))

            if pcid == nhost - 1 and args.buffer:
                plot_image_data(AK[ecs].states3d.mean(2), 0, 10,
                                'buffered_mean_%05d' % int(pc.t(0)/100),
                                'Buffered concentration; t = %6.0fms' % pc.t(0))
        if pcid == 0: progress_bar(tstop)
        pc.psolve(pc.t(0)+h.dt)  # run the simulation for 1 time step
        
        # determine the furthest distance from the origin where
        # extracellular potassium exceeds Kceil (dist)
        # And the shortest distance from the origin where the extracellular
        # extracellular potassium is below Kceil (dist1)
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
    if pcid == 0 :
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
        

    soma, dend, pos = [], [], []
    for n in rec_neurons:
        soma.append(n.somaV)
        dend.append(n.dendV)
        pos.append([n.x,n.y,n.z])
    pout = open(os.path.join(outdir,"membrane_potential_%i.pkl" % pcid),'wb')
    pickle.dump([soma,dend,pos],pout)
    pout.close()
    pc.barrier()    

    if pcid == 0:
        plot_rec_neurons()
run(args.tstop)

