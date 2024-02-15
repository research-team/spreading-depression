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

# mpiexec -n 1 nrniv -mpi -python cell_sd.py
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
rxd.nthread()


rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37
numpy.random.seed(6324555+pcid)





outdir = os.path.abspath('tests/334')






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

Rm = 28000 # Ohm.cm^2 (Migliore value)
cm = 1.2
Ra = 150
class Neuron:

    def __init__(self):

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
#        for mechanism_s in ['h','hNa','hha2', 'IA','kadcr','borgka','Ih','Ihvip', 'kap', 'km' ,'pas', 'Nafcr', 'kdrcr', 'IKscr', 'iCcr', 'kadcr']:
 #           self.soma.insert(mechanism_s)
        for mechanism_s in ['extracellular','h','hNa','hha2', 'IA', 'Ih','Nasoma','km','Ksoma','pas', 'k_ion', 'na_ion', 'kap','nap', 'kdrcr', 'Nafcr','IKscr' ]:
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


        self.soma(0.5).h.ghdbar = 0.00005
        self.soma(0.5).h.vhalfl = -73
        self.soma(0.5).Ih.gkhbar = 0.00035*0.1
        self.soma(0.5).km.gbar = 0.06
        #self.soma(0.5).borgka.gkabar = 0.00015*4*0.5
        #self.soma(0.5).kadcr.gkabar = 0.003
        self.soma(0.5).hha2.gnabar = 0.007
        self.soma(0.5).hha2.gkbar = 0.007/10
        self.soma(0.5).hha2.gl = 0
        self.soma(0.5).hha2.el = -70
        #self.soma(0.5).pas.g = 1/Rm
        #self.soma(0.5).pas.e = -70
        self.soma(0.5).Nafcr.gnafbar = 0.015
        self.soma(0.5).kdrcr.gkdrbar = 0.018
        self.soma(0.5).IKscr.gKsbar = 0.000725
        #self.soma(0.5).iCcr.gkcbar = 0.00003
        #self.soma(0.5).kadcr.gkabar = 0.003 

        #print(self.soma.psection())
        #self.n_Ksoma = h.Vector().record(self.soma(0.5).Ksoma._ref_n)
        #self.h_Nasoma = h.Vector().record(self.soma(0.5).Nasoma._ref_h)
        #self.m_Nasoma = h.Vector().record(self.soma(0.5).Nasoma._ref_m)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)
        
        #---------------dend----------------
        
        for mechanism_d in ['Nadend','Kdend','hha_old', 'h', 'hNa','IA','kap', 'pas', 'Nafcr', 'kdrcr', 'nap', 'k_ion', 'na_ion', 'Ihvip', 'kad']:
            self.dend.insert(mechanism_d)
        self.dend(0.5).IA.gkAbar = 0.004*1.2
        #self.dend1(0.5).Ih.gkhbar = 0.00035*0.1
        self.dend(0.5).Nadend.gnadend = 2*0.0117
        self.dend(0.5).Nadend.gl = 1/Rm
        self.dend(0.5).Nadend.el = -65
        self.dend(0.5).Kdend.gkdend = 20*0.023
        self.dend(0.5).h.ghdbar = 0.00005 * 4
        self.dend(0.5).h.vhalfl = -81
        self.dend(0.5).IA.gkAbar = 0.004*1.2
        self.dend(0.5).kad.gkabar = 0
        #self.dend(0.5).km.gbar = 0.06
        #self.dend(0.5).borgka.gkabar = 0.00015*4*0.5
        self.dend(0.5).hha_old.gnabar = 0.007
        self.dend(0.5).hha_old.gkbar = 0.007/8.065
        self.dend(0.5).hha_old.el = -70
        self.dend(0.5).hha_old.gl = 0
        #self.dend(0.5).pas.g = 1/20000
        #self.dend(0.5).pas.e = -70

        self.dend(0.5).Nafcr.gnafbar = 0.018*5
        self.dend(0.5).kdrcr.gkdrbar = 0.018*0.5
        #self.Dn_Kdend = h.Vector().record(self.dend(0.5).Kdend._ref_n)
        #self.Dh_Nadend = h.Vector().record(self.dend(0.5).Nadend._ref_h)
        #self.Dm_Nadend = h.Vector().record(self.dend(0.5).Nadend._ref_m)
        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        
        for sec in self.all:        
            Ra = 150
            cm = 1.2

        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0, geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=14)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=120)
        self.k_i= self.k[self.cyt]

sys.stdout.write('\nrun')
sys.stdout.flush()


# show ion in extracellular space  
def video(species, min_conc=3, max_conc=40, frames=200):
    
    fig = pyplot.figure()
    im = pyplot.imshow(species[ecs].states3d.mean(2), vmin=min_conc, vmax=max_conc)
    pyplot.axis('off')

    def init():
        im.set_data(species[ecs].states3d.mean(2))
        return [im]
    def animate(i):
        h.fadvance()
        im.set_data(species[ecs].states3d.mean(2))
        return [im]

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=300)
    ret =  HTML(anim.to_html5_video())
    anim.save(os.path.join(outdir,'basic_animation.mp4'))
    pyplot.close()



for sec in h.allsec():
    sec.nai = 4.297

#Create cell
cell = Neuron()

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
print(2)
# points for record concetration
#k_0_0_0=h.Vector().record(k[ecs].node_by_location(0, 0, 0)._ref_value)
#k_10_10_20=h.Vector().record(k[ecs].node_by_location(10, 10, -20)._ref_value)
#k_20_20_50=h.Vector().record(k[ecs].node_by_location(17, 17, -48)._ref_value)
print(3)

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

def plot_rec_neurons():
    somaV, dendV, pos = [], [], []
    
    fin = open(os.path.join(outdir,'membrane_potential.pkl'),'rb')
    [sV, dV, p] = pickle.load(fin)
    fin.close()
    somaV.extend(sV) #list
    dendV.extend(dV) #list
    pos.extend(p) #list.len()=3

    for idx in range(len(somaV)):
        if idx%100==0:  
            fig = pyplot.figure()
            ax = fig.add_subplot(111,projection='3d')
            ax.set_position([0.0,0.05,0.9,0.9])
            ax.set_xlim([-Lx/2.0, Lx/2.0])
            ax.set_ylim([-Ly/2.0, Ly/2.0])
            ax.set_zlim([-Lz/2.0, Lz/2.0])
            

            cmap = pyplot.get_cmap('jet')
            
            x = pos
            soma_z = [x[2]-somaR,x[2]+somaR]
            cell_x = [x[0],x[0]]
            cell_y = [x[1],x[1]]
            scolor = cmap((somaV[idx]+70.0)/70.0)
            # plot the soma
            ax.plot(cell_x, cell_y, soma_z, linewidth=2, color=scolor, 
                    alpha=0.5)

            dcolor = cmap((dendV[idx]+70.0)/70.0)
            dend_z = [x[2]-somaR, x[2]-somaR - dendL]
            # plot the dendrite
            ax.plot(cell_x, cell_y, dend_z, linewidth=0.5, color=dcolor, 
                    alpha=0.5)

            norm = colors.Normalize(vmin=-70,vmax=0)
            pyplot.title('Neuron membrane potentials; t = %gms' % (idx))

            # add a colorbar 
            ax1 = fig.add_axes([0.88,0.05,0.04,0.9])
            cb1 = colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm,
                                                orientation='vertical')
            cb1.set_label('mV')
            
            # save the plot
            filename = 'neurons_{:05d}.png'.format(idx)
            pyplot.savefig(os.path.join(outdir,filename))
            pyplot.close()

def plot_spike(volt_soma, volt_dend, t, k, na, k_in, na_in,v):

    fig = pyplot.figure(figsize=(20,16))
    ax1 = fig.add_subplot(4,1,1)
    soma_plot = ax1.plot(t , volt_soma , color='black', label='soma')
    dend_plot = ax1.plot(t, volt_dend, color='red', label='dend')
    v=ax1.plot(t, v, color='blue', label='v')
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



def plot_K_ecs_in_points(x, t):
    for i in x:
        pyplot.plot(t, i)
    pyplot.legend(['0 0 0','10 10 -20','20 20 -50'])
    pyplot.grid()
    pyplot.savefig(os.path.join(outdir, 'k_ecs.png'))
    pyplot.close('all')



def plot_n_m_h(t, soma):
    fig = pyplot.figure(figsize=(20,16))
    ax1 = fig.add_subplot(3,1,1)
    ax1.plot(t, soma.n_km, label='km')
    ax1.plot(t, soma.n_kap, label='kap')
    ax1.plot(t, soma.n_hha2, label='hha2')
    ax1.legend()
    ax1.set_ylabel('state')

    ax2 = fig.add_subplot(3,1,2)
    ax2.plot(t, soma.m_hha2, label='hha2')
    ax2.plot(t, soma.m_kca, label='kca')
    ax2.legend()
    ax2.set_ylabel('state')

    ax3 = fig.add_subplot(3,1,3)
    ax3.plot(t , soma.h_hha2 , label='hha2')
    ax3.legend()
    ax3.set_ylabel('state')

    


    ax3.set_xlabel('time (ms)')
    fig.savefig(os.path.join(nmh_dir, 'nmhSOMA.png'))
    pyplot.close('all')

def plot_n_m_h_Dend(t, soma):
    fig = pyplot.figure(figsize=(20,16))
    ax1 = fig.add_subplot(3,1,1)
    ax1.plot(t, soma.Dn_km, label='km')
    ax1.plot(t, soma.Dn_kap, label='kap')
    ax1.plot(t, soma.Dn_hha_old, label='hha_old')
    ax1.plot(t, soma.Dn_Kdend, label='Kdend')
    ax1.legend()
    ax1.set_ylabel('state')

    ax2 = fig.add_subplot(3,1,2)
    ax2.plot(t, soma.Dm_kca, label='kca')
    ax2.plot(t, soma.Dm_cat, label='cat')
    ax2.plot(t, soma.Dm_car, label='car')
    ax2.plot(t, soma.Dm_hha_old, label='hha_old')
    ax2.plot(t, soma.Dm_calH, label='calH')
    ax2.plot(t, soma.Dm_Nadend, label='Nadend')
    ax2.plot(t, soma.Dm_nap, label='nap')
    ax2.legend()
    ax2.set_ylabel('state')

    ax3 = fig.add_subplot(3,1,3)
    ax3.plot(t , soma.Dh_hha_old , label='hha_old')
    ax3.plot(t , soma.Dh_cat , label='cat')
    ax3.plot(t , soma.Dh_car , label='car')
    ax3.plot(t , soma.Dh_calH , label='calH')
    ax3.plot(t , soma.Dh_Nadend , label='Nadend')
    ax3.legend()
    ax3.set_ylabel('state')

    ax3.set_xlabel('time (ms)')
    fig.savefig(os.path.join(nmh_dir, 'nmhDEND.png'))
    pyplot.close('all')


def plot_image_data(data, min_val, max_val, filename, title):
    """Plot a 2d image of the data"""
    sb = scalebar.ScaleBar(1e-6)
    sb.location='lower left'
    pyplot.imshow(data, extent=k[ecs].extent('xz'), vmin=min_val,
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
    pyplot.ylim(k[ecs].extent('z'))
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
        '''
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
        '''
    #plot_image_region(cell.k.nodes.concentration, 2.5, 140, 'Potassium intracellular; t = %6.0fms' % h.t, cell.k, cell.cyt)
    
    sys.stdout.write('\ndone, wait\n')
    sys.stdout.flush()
    
    #progress_bar(tstop)
    
    if pcid == 0:
    #plot_image_region(cell.k.nodes.concentration, 2.5, 140, 'Potassium intracellular; t = %6.0fms' % h.t, cell.k, cell.cyt)
        #fout.close()
    
        plot_spike(cell.somaV,
                    cell.dendV,
                    time,
                    cell.k_vec,
                    cell.na_vec,
                    cell.k_concentration,
                    cell.na_concentration, cell.v_vec)
        #plot_n_m_h(time, cell)
        #plot_n_m_h_Dend(time, cell)
        sys.stdout.write('Simulation complete. Plotting membrane potentials')
        sys.stdout.flush()
       # plot_K_ecs_in_points([k_0_0_0,k_10_10_20, k_20_20_50 ] ,time)
    pos = [x, y, z]
    pout = open(os.path.join(outdir,"membrane_potential.pkl"),'wb')
    pickle.dump([cell.somaV, cell.dendV, pos],pout)
    pout.close()
    pc.barrier()
    plot_cell('cell')    
    if pcid == 0: plot_rec_neurons()
    exit(0)

run(200)
