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

h.nrnmpi_init()
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
root = 0

rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37

numpy.random.seed(6324555 + pcid)
outdir = os.path.abspath('tests/606W')


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
Lx, Ly, Lz = 100, 100, 1700 
Kceil = 15.0  # threshold used to determine wave speed
Ncell = int(9e4 * (Lx * Ly * Lz * 1e-9))

#L2/3 (0-400)
Nbask23 = 90 #59
Naxax23 = 90 #59
NLTS23 = 90 #59

#L4 (400-700)
Nspinstel4 = 240
NtuftIB5 = 800
Bask_4 = 235 #235 bask4
#L5 (700-1200)
NtuftRS5 = 200
Nbask56 = 100

#L5/6 (700-1700)
Naxax56 = 100
NLTS56 = 500

#L6(1200-1700)
NnontuftRS6 = 500

somaR = 11  # soma radius
dendR = 1.4  # dendrite radius
dendL = 100.0  # dendrite length
doff = dendL + somaR

alpha0, alpha1 = 0.07, 0.2  # anoxic and normoxic volume fractions
tort0, tort1 = 1.8, 1.6  # anoxic and normoxic tortuosities
r0 = 100  # radius for initial elevated K+

num=0

count_cells = 0
count_syn = 0

#0-400
rec_neurons1 = [LTS23(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(somaR,400),
    i)
    for i in range(0, int(NLTS23))]

num+=NLTS23
rec_neurons2=[Bask23(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(somaR,400), 
    i)
    for i in range(num, int(num+Nbask23))]

num+=Nbask23
rec_neurons3=[Axax23(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(somaR,400), 
    i)
    for i in range(num, int(num+Naxax23))]

num+=Naxax23
#400-700
rec_neurons4=[Spinstel4(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(400,700), i)
    for i in range(num, int(num+Nspinstel4))]

num+=Nspinstel4
rec_neurons5=[TuftIB5(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(400,700), i)
    for i in range(num, int(num+NtuftIB5))]
num+=NtuftIB5
rec_neurons11 = [Bask4(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(400,700), i)
    for i in range(num, num+Bask_4)]

num+=Bask_4
#700-1200
rec_neurons6=[TuftRS5(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,1200), i)
    for i in range(num, int(num+NtuftRS5))]
num+=NtuftRS5
rec_neurons7=[Bask56(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,1200), i)
    for i in range(num, int(num+Nbask56))]

num+=Nbask56

#700-1700
rec_neurons8=[Axax56(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,1700), i)
    for i in range(num, int(num+Naxax56))]
num+=Naxax56
rec_neurons9=[LTS56(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,1700), i)
    for i in range(num, int(num+NLTS56))]

num+=NLTS56
rec_neurons10=[NontuftRS6(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(1200,1700-somaR), i)
    for i in range(num, int(num+NnontuftRS6))]
#2710
cell=[rec_neurons1, rec_neurons2, rec_neurons3, rec_neurons4, rec_neurons5, rec_neurons6, rec_neurons7, rec_neurons8, rec_neurons9, rec_neurons10, rec_neurons11]

for i in rec_neurons1:
    i.connect(rec_neurons3[random.randint(0,Naxax23-1)])
    i.connect(rec_neurons2[random.randint(0,Nbask23-1)])
    i.connect(rec_neurons7[random.randint(0,Nbask56-1)])
    i.connect(rec_neurons5[random.randint(0,NtuftIB5-1)])
    count_syn+=4
    count_cells+=1

for i in rec_neurons3:
    i.connect(rec_neurons1[random.randint(0,NLTS23-1)])
    i.connect(rec_neurons2[random.randint(0,Nbask23-1)])
    i.connect(rec_neurons7[random.randint(0,Nbask56-1)])
    i.connect(rec_neurons5[random.randint(0,NtuftIB5-1)])
    count_syn+=4
    count_cells+=1

for i in rec_neurons2:
    i.connect(rec_neurons1[random.randint(0,NLTS23-1)])
    i.connect(rec_neurons3[random.randint(0,Naxax23-1)])
    i.connect(rec_neurons7[random.randint(0,Nbask56-1)])
    i.connect(rec_neurons5[random.randint(0,NtuftIB5-1)])
    count_syn+=4
    count_cells+=1


for i in rec_neurons4:
    i.connect(rec_neurons3[random.randint(0,Naxax23-1)])
    i.connect(rec_neurons2[random.randint(0,Nbask23-1)])
    i.connect(rec_neurons1[random.randint(0,NLTS23-1)])
    i.connect(rec_neurons11[random.randint(0,Bask_4-1)])
    i.connect(rec_neurons8[random.randint(0,Naxax56-1)])
    i.connect(rec_neurons9[random.randint(0,NLTS56-1)])
    count_syn+=6
    count_cells+=1

for i in rec_neurons5:
    i.connect(rec_neurons7[random.randint(0,Nbask56-1)])
    count_syn+=1
    count_cells+=1

for i in rec_neurons6:
    i.connect(rec_neurons7[random.randint(0,Nbask56-1)])
    count_syn+=1
    count_cells+=1

for i in rec_neurons7:
    i.connect(rec_neurons6[random.randint(0,NtuftRS5-1)])
    i.connect(rec_neurons9[random.randint(0,NLTS56-1)])
    i.connect(rec_neurons8[random.randint(0,Naxax56-1)])
    count_syn+=3
    count_cells+=1

for i in rec_neurons8:
    i.connect(rec_neurons7[random.randint(0,Nbask56-1)])
    i.connect(rec_neurons10[random.randint(0,NnontuftRS6-1)])
    count_syn+=2
    count_cells+=1

for i in rec_neurons9:
    i.connect(rec_neurons7[random.randint(0,Nbask56-1)])
    i.connect(rec_neurons10[random.randint(0,NnontuftRS6-1)])
    count_syn+=2
    count_cells+=1

for i in rec_neurons10:
    i.connect(rec_neurons9[random.randint(0,NLTS56-1)])
    i.connect(rec_neurons8[random.randint(0,Naxax56-1)])
    count_syn+=2
    count_cells+=1

for i in rec_neurons11:
    i.connect(rec_neurons1[random.randint(0,NLTS23-1)])
    i.connect(rec_neurons3[random.randint(0,Naxax23-1)])
    i.connect(rec_neurons2[random.randint(0,Nbask23-1)])
    i.connect(rec_neurons9[random.randint(0,NLTS56-1)])
    i.connect(rec_neurons8[random.randint(0,Naxax56-1)])
    i.connect(rec_neurons7[random.randint(0,Nbask56-1)])
    i.connect(rec_neurons4[random.randint(0,Nspinstel4-1)])
    count_syn+=7
    count_cells+=1






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
print('initialize')




df = pd.DataFrame({
    'id' : [j.id for i in cell for j in i],
    'name' : [j.name for i in cell for j in i],
    'number' : [j.number for i in cell for j in i],
    'count' : [j.count for i in cell for j in i],
    'cells' : [j.cells for i in cell for j in i]
    })
df.to_csv(os.path.join(outdir,'data_cells.csv'))

dg = pd.DataFrame({
    'count_cells' : [count_cells],
    'count_syn' : [count_syn]
    })
dg.to_csv(os.path.join(outdir,'info.csv'))


def progress_bar(tstop, size=40):
    """ report progress of the simulation """
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()

def plot_3D_data(data):
    data.head(10)
    fig = px.scatter_3d(data, x='x', y='y', z='z', color='name')
    fig.update_layout(
    scene = dict(
        aspectratio = dict(
            x = 1,
            y = 1,
            z = 16
        )
    ),
    margin = dict(
        t = 20,
        b = 20,
        l = 20,
        r = 20
    )
)
    fig.write_html(os.path.join(outdir, 'data3D.html'))


def plot_rec_neurons():
    somaV, dendV, pos, data = [], [], [], []
    for i in range(nhost):
        fin = open(os.path.join(outdir, 'membrane_potential_%i.pkl' % i), 'rb')
        [sV, dV, p, id] = pickle.load(fin)
        fin.close()
        somaV.extend(sV)
        dendV.extend(dV)
        pos.extend(p)
        data.extend(id)

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
       # for i in [0, 108] :
            #plot_spike(rec_neurons[i], time , i)
        print("\nSimulation complete. Plotting membrane potentials")
        plot_K_ecs_in_point_000(kecs ,time)

    # save membrane potentials
    soma, dend, pos, data = [], [], [], []
    x_pos,y_pos,z_pos,id_color, listname = [],[],[],[], []

    for j in cell:
        for n in j:
            soma.append(n.somaV)
            dend.append(n.dendV)
            pos.append([n.x, n.y, n.z])
            data.append([n.id])
            x_pos.append(n.x)
            y_pos.append(n.y)
            z_pos.append(n.z)
            id_color.append(n.id)
            listname.append(n.name)
            plot_spike_html(n, time, n.number)

    #pout = open(os.path.join(outdir, "membrane_potential_%i.pkl" % pcid), 'wb')
    #pickle.dump([soma, dend, pos, data], pout)
    #pout.close()
    d3_data = pd.DataFrame(dict(x=x_pos, y=y_pos, z=z_pos, id=id_color, name=listname))
    pc.barrier()
    if pcid == 0:

        plot_3D_data(d3_data)
        #plot_rec_neurons()
    exit(0)


run(100)