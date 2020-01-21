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
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()

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
if pcid == 0 and not os.path.exists(outdir):
    try:
        os.makedirs(outdir)
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
    """ A neuron with soma and dendrite with; fast and persistent sodium
    currents, potassium currents, passive leak and potassium leak and an
    accumulation mechanism. """

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


        for mechanism in ['tnak', 'tnap', 'taccumulation3', 'kleak']:
            self.soma.insert(mechanism)
            self.dend.insert(mechanism)

        #
        self.soma(0.5).tnak.imax = 0
        self.dend(0.5).tnak.imax = 0

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)
        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.time = h.Vector().record(h._ref_t)



rec_neurons = [Neuron(
    (numpy.random.random() * 2.0 - 1.0) * (Lx / 2.0 - somaR),
    (numpy.random.random() * 2.0 - 1.0) * (Ly / 2.0 - somaR),
    (numpy.random.random() * 2.0 - 1.0) * (Lz / 2.0 - somaR), 100)
    for i in range(0, int(Nrec / nhost))]

alpha = alpha1
tort = tort1


ecs = rxd.Extracellular(-Lx / 2.0, -Ly / 2.0,
                        -Lz / 2.0, Lx / 2.0, Ly / 2.0, Lz / 2.0, dx=10,
                        volume_fraction=alpha, tortuosity=tort)


k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial=lambda nd: 40
if nd.x3d ** 2 + nd.y3d ** 2 + nd.z3d ** 2 < r0 ** 2 else 3.5,
                ecs_boundary_conditions=3.5)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=133.574,
                 ecs_boundary_conditions=133.574)


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
                    scolor = cmap((somaV[i].get(idx) + 70.0) / 70.0)
                    # plot the soma
                    ax.plot(cell_x, cell_y, soma_z, linewidth=2, color=scolor,
                            alpha=0.5)

                    dcolor = cmap((dendV[i].get(idx) + 70.0) / 70.0)
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

def plot_spike_for_1_neu(volt, t, i, tstop):
    #fig, ax = pyplot.subplots()
    #ax.plot(t, volt)
    pyplot.plot(t,volt)
    pyplot.xticks(np.arange(0, tstop+1, 100.0))
    #pyplot.yticks(np.arange(1,15,3))
    #plt.show()
    pyplot.grid()
    #fig.savefig(os.path.join(outdir, 'spike_%i.png' % i))
    pyplot.savefig(os.path.join(outdir, 'spike_%i.png' % i))
    pyplot.close('all')


h.dt = 1

def run(tstop):

    if pcid == 0:
        fout = open(os.path.join(outdir, 'wave_progress%s.txt' ), 'a')

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
        for i in range(1000) :
            plot_spike_for_1_neu(rec_neurons[i].somaV, rec_neurons[i].time, i ,tstop)
        print("\nSimulation complete. Plotting membrane potentials")

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