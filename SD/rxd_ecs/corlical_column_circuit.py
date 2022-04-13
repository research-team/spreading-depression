import logging

from SD.rxd_ecs.Thalamus import thalamus_cell

logging.basicConfig(filename='logs.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
logging.info("let's get it started")
import random
import os
import sys
import csv
import h5py as hdf5

from cells import *
import json
from neuron.units import ms, mV
import numpy as np
h.load_file("stdgui.hoc")
pc = h.ParallelContext()
rank = int(pc.id())
nhost = int(pc.nhost())

AMPA_nclist = []
GABA_nclist = []
NMDA_nclist = []

#time =300
# rxd.options.enable.extracellular = True

# simulation parameters
time_sim = 200
Lx, Ly, Lz = 200, 200, 1700
Kceil = 15.0  # threshold used to determine wave speed
Ncell = int(9e4 * (Lx * Ly * Lz * 1e-9))

#L2/3 (0-400)
Nbask23 = 10 #59
Naxax23 = 10 #59
NLTS23 = 10 #59
NsyppyrFRB = 5
NsyppyrRS = 50
#L4 (400-700)
Nspinstel4 = 30
Nbask4=20
NtuftIB5 = 40
Bask_4 = 20 #235 bask4
#L5 (700-1200)
NtuftRS5 = 10
Nbask56 = 10

#L5/6 (700-1700)
Naxax56 = 10
NLTS56 = 25

#L6(1200-1700)
NnontuftRS6 = 25

#tlms
NTCR = 15
NnRT = 10

somaR = 11  # soma radius
dendR = 1.4  # dendrite radius
dendL = 100.0  # dendrite length
doff = dendL + somaR

alpha0, alpha1 = 0.07, 0.2  # anoxic and normoxic volume fractions
tort0, tort1 = 1.8, 1.6  # anoxic and normoxic tortuosities
r0 = 100  # radius for initial elevated K+

count_cells = 0
count_syn = 0

#0-400

data={}
data['cells']=[]

value=0#100 #% epilepsy

class CC_circuit:
    def __init__(self):

        self.data={}
        self.data['cells']=[]
        self.groups = []
        self.neurons = []

        logging.info('start creating neurons')

        rec_neurons12 = []

        num=0

        epi=int(value*NsyppyrFRB/100)
        for i in range(rank, NsyppyrFRB-epi, nhost):
            rec_neurons12.append(SyppyrFRB(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform( -850+somaR,-450),
            i+num))

        num+=NsyppyrFRB

        if value!=0:
            for i in range(rank, epi, nhost):
                rec_neurons12.append(EpilepsySyppyrFRB(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-850 + somaR, -450),
                    i + num))

        self.syppyrFRB = self.addpool(rec_neurons12)
        num+=epi

        rec_neurons13 = []
        epi=int(value*NsyppyrRS/100)
        for i in range(rank, NsyppyrRS-epi, nhost):
            rec_neurons13.append(SyppyrRS(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-850+somaR,-450),
            i+num))

        num+=NsyppyrRS-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                rec_neurons13.append(EpilepsySyppyrRS(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-850 + somaR, -450),
                    i + num))

        self.syppyrRS = self.addpool(rec_neurons13)
        num+=epi

        rec_neurons1 = []
        for i in range(rank, NLTS23, nhost):
            rec_neurons1.append(LTS23(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-850+somaR,-450),
            i+num))

        self.LTS23 = self.addpool(rec_neurons1)
        num+=NLTS23

        rec_neurons2=[]
        for i in range(rank, Nbask23, nhost):
            rec_neurons2.append(Bask23(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-850+somaR,-450),
            i+num))

        self.bask23 = self.addpool(rec_neurons2)
        num+=Nbask23

        rec_neurons3=[]
        for i in range(rank, Naxax23, nhost):
            rec_neurons3.append(Axax23(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-850+somaR,-450),
            i+num))

        self.axax23 = self.addpool(rec_neurons3)
        num+=Naxax23
        #400-700
        rec_neurons4=[]
        epi=int(value*Nspinstel4/100)
        for i in range(rank, Nspinstel4-epi, nhost):
            rec_neurons4.append(Spinstel4(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-450,-150), i+num))

        num+=Nspinstel4-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                rec_neurons4.append(EpilepsySpinstel4(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-450, -150), i + num))

        self.spinstel4 = self.addpool(rec_neurons4)
        num+=epi

        rec_neurons16=[]
        for i in range(rank, Nbask4, nhost):
            rec_neurons16.append(Bask4(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-450,-150), i+num))

        self.bask4 = self.addpool(rec_neurons16)
        num+=Nbask4

        rec_neurons5=[]
        epi=int(value*NtuftIB5/100)
        for i in range(rank, NtuftIB5-epi, nhost):
            rec_neurons5.append(TuftIB5(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,50), i+num))
        num+=NtuftIB5-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                rec_neurons5.append(EpilepsyTuftIB5(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-150, 50), i + num))

        self.tuftIB5 = self.addpool(rec_neurons5)
        num+=epi

        #700-1200
        rec_neurons6=[]
        epi=int(value*NtuftRS5/100)
        for i in range(rank, NtuftRS5-epi, nhost):
            rec_neurons6.append(TuftRS5(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,350), i+num))
        num+=NtuftRS5-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                rec_neurons6.append(EpilepsyTuftRS5(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-150, 350), i + num))

        self.tuftRS5 = self.addpool(rec_neurons6)
        num+=epi

        rec_neurons7=[]
        for i in range(rank, Nbask56, nhost):
            rec_neurons7.append(Bask56(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,350), i+num))

        self.bask56 = self.addpool(rec_neurons7)
        num+=Nbask56

        #700-1700
        rec_neurons8=[]
        for i in range(rank, Naxax56, nhost):
            rec_neurons8.append(Axax56(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,850), i+num))

        self.axax56 = self.addpool(rec_neurons8)
        num+=Naxax56

        rec_neurons9=[]
        for i in range(rank, NLTS56, nhost):
            rec_neurons9.append(LTS56(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,850), i+num))


        self.lts56 = self.addpool(rec_neurons9)
        num+=NLTS56

        rec_neurons10=[]
        epi=int(value*NnontuftRS6/100)
        for i in range(rank, NnontuftRS6-epi, nhost):
            rec_neurons10.append(NontuftRS6(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(350,850-somaR), i+num))
        num+=NnontuftRS6-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                rec_neurons10.append(EpilepsyNontuftRS6(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(350, 850 - somaR), i + num))
        num += epi
        self.nontuftRS6 = self.addpool(rec_neurons10)


        rec_neurons14=[]
        for i in range(rank, NTCR, nhost):
            rec_neurons14.append(TCR(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(1000,1300-somaR), i+num))

        self.tcr = self.addpool(rec_neurons14)
        num +=NTCR

        rec_neurons15=[]
        for i in range(rank, NnRT, nhost):
            rec_neurons15.append(nRT(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(1100,1300-somaR), i+num))

        self.nrt = self.addpool(rec_neurons15)
        num +=NnRT

        self.thalamus_generator = self.addgener(2, 100, 10)

        rec_neurons16=[]
        for i in range(rank, NnRT, nhost):
            rec_neurons16.append(thalamus_cell(
                random.uniform(somaR,Lx-somaR),
                random.uniform(somaR,Ly-somaR),
                random.uniform(-500,-200-somaR),i+num))
        self.nt=self.addpool(rec_neurons16)
        num+=NnRT



        logging.info('created neurons, start adding conections')

        ''' CONNECTIONS '''

        '''
        Connections AMPA
        '''
        connectcells(self.thalamus_generator, self.tcr, 0.85, 1, 1)
        connectcells(self.tcr, self.spinstel4, 0.5, 1, 1)

        connectcells(self.syppyrFRB, self.bask23, 0.23, 1, 1)
        'Возможно стоит поделить на 2 количество syn у syppyrRS и syppyrFRB
        connectcells(self.syppyrFRB, self.syppyrFRB, 9.37, 1, 1)
        connectcells(self.syppyrFRB, self.syppyrRS, 9.37, 1, 1)

        connectcells(self.syppyrFRB, self.axax23, 0.08, 1, 1)
        connectcells(self.syppyrFRB, self.tuftRS5, 7.27, 1, 1)
        connectcells(self.syppyrFRB, self.nontuftRS6, 1.46, 1, 1)
        connectcells(self.syppyrFRB, self.bask56, 0.096, 1, 1)
        connectcells(self.syppyrFRB, self.tuftIB5, 4.44, 1, 1)
        connectcells(self.syppyrFRB, self.lts56, 0.27, 1, 1)
        connectcells(self.syppyrFRB, self.axax56, 0.03, 1, 1)
        connectcells(self.syppyrFRB, self.syppyrRS, 9.37, 1, 1)
        connectcells(self.syppyrFRB, self.LTS23, 0.55, 1, 1)

        connectcells(self.syppyrRS, self.LTS23, 0.55, 1, 1)
        connectcells(self.syppyrRS, self.bask23, 0.22, 1, 1)
        connectcells(self.syppyrRS, self.axax23, 0.08, 1, 1)
        connectcells(self.syppyrRS, self.syppyrFRB, 9.37, 1, 1)
        connectcells(self.syppyrRS, self.tuftIB5, 4.95, 1, 1)
        connectcells(self.syppyrRS, self.lts56, 0.53, 1, 1)
        connectcells(self.syppyrRS, self.axax56, 0.03, 1, 1)
        connectcells(self.syppyrRS, self.syppyrRS, 9.37, 1, 1)
        connectcells(self.syppyrRS, self.tuftRS5, 4.44, 1, 1)
        connectcells(self.syppyrRS, self.bask56, 0.11, 1, 1)
        connectcells(self.syppyrRS, self.nontuftRS6, 1.46, 1, 1)
        connectcells(self.syppyrRS, self.spinstel4, 0.98, 1, 1)

        connectcells(self.spinstel4, self.bask4, 0.031, 1, 1)
        connectcells(self.spinstel4, self.LTS23, 0.3, 1, 1)
        connectcells(self.spinstel4, self.spinstel4, 0.099, 1, 1)
        connectcells(self.spinstel4, self.bask23, 0.02, 1, 1)
        connectcells(self.spinstel4, self.syppyrFRB, 0.68, 1, 1)
        connectcells(self.spinstel4, self.syppyrRS, 0.58, 1, 1)
        connectcells(self.spinstel4, self.bask56, 0.01, 1, 1)
        connectcells(self.spinstel4, self.nontuftRS6, 0.14, 1, 1)
        connectcells(self.spinstel4, self.axax56, 0.004, 1, 1)
        connectcells(self.spinstel4, self.LTS56, 0.03, 1, 1)
        connectcells(self.spinstel4, self.axax23, 0.005, 1, 1)

        connectcells(self.tuftRS5, self.tuftRS5, 2.25, 1, 1)
        connectcells(self.tuftRS5, self.axax56, 0.027, 1, 1)
        connectcells(self.tuftRS5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftRS5, self.nontuftRS6, 1.164, 1, 1)
        connectcells(self.tuftRS5, self.spinstel4, 0.161, 1, 1)
        'Возможно поделить на 2 количество syn в следующих двух соединениях'
        connectcells(self.tuftRS5, self.syppyrRS, 0.36, 1, 1)
        connectcells(self.tuftRS5, self.syppyrFRB, 0.36, 1, 1)
        connectcells(self.tuftRS5, self.bask23, 0.017, 1, 1)
        connectcells(self.tuftRS5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftRS5, self.axax23, 0.004, 1, 1)
        connectcells(self.tuftRS5, self.LTS23, 0.019, 1, 1)
        connectcells(self.tuftRS5, self.LTS56, 0.284, 1, 1)
        connectcells(self.tuftRS5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftRS5, self.tuftIB5, 1.916, 1, 1)


        connectcells(self.tuftIB5, self.LTS23, 0.013, 1, 1)
        connectcells(self.tuftIB5, self.lts56, 0.279, 1, 1)
        connectcells(self.tuftIB5, self.axax56, 0.027, 1, 1)
        connectcells(self.tuftIB5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftIB5, self.tuftRS5, 1.916, 1, 1)
        connectcells(self.tuftIB5, self.axax23, 0.004, 1, 1)
        connectcells(self.tuftIB5, self.syppyrRS, 0.36, 1, 1)
        connectcells(self.tuftIB5, self.syppyrFRB, 0.36, 1, 1)
        connectcells(self.tuftIB5, self.nontuftRS6, 1.164, 1, 1)
        connectcells(self.tuftIB5, self.spinstel4, 0.156, 1, 1)
        connectcells(self.tuftIB5, self.bask23, 0.017, 1, 1)
        connectcells(self.tuftIB5, self.tuftIB5, 1.916, 1, 1)


        connectcells(self.nontuftRS6, self.nontuftRS6, 0.68, 1, 1)
        connectcells(self.nontuftRS6, self.bask23, 0.004, 1, 1)
        connectcells(self.nontuftRS6, self.nontuftRS6, 0.68, 1, 1)
        connectcells(self.nontuftRS6, self.spinstel4, 0.044, 1, 1)
        connectcells(self.nontuftRS6, self.syppyrFRB, 0.093, 1, 1)
        connectcells(self.nontuftRS6, self.syppyrRS, 0.093, 1, 1)
        connectcells(self.nontuftRS6, self.bask56, 0.057, 1, 1)
        connectcells(self.nontuftRS6, self.axax56, 0.014, 1, 1)
        connectcells(self.nontuftRS6, self.LTS56, 0.16, 1, 1)
        connectcells(self.nontuftRS6, self.tuftRS5, 0.85, 1, 1)
        connectcells(self.nontuftRS6, self.tuftIB5, 0.85, 1, 1)
        connectcells(self.nontuftRS6, self.axax23, 0.00096, 1, 1)



        '''
            Connections GABA
        '''

        connectcells(self.bask23, self.syppyrFRB, 9.37, 1, -1)

        connectcells(self.axax23, self.bask23, 0.023, 1, -1)
        connectcells(self.axax23, self.axax23, 0.00027, 1, -1)
        connectcells(self.axax23, self.LTS23, 0.029, 1, -1)
        connectcells(self.axax23, self.tuftIB5, 0.082, 1, -1)

        connectcells(self.LTS23, self.bask23, 0.446, 1, -1)
        connectcells(self.LTS23, self.syppyrFRB, 0.74, 1, -1)
        connectcells(self.LTS23, self.LTS23, 0.301, 1, -1)

        connectcells(self.bask23, self.tuftIB5, 1.53, 1, -1)

        connectcells(self.axax56, self.tuftIB5, 0.108, 1, -1)
        connectcells(self.axax56, self.nontuftRS6, 0.014, 1, -1)

        connectcells(self.lts56, self.axax56, 0.062, 1, -1)
        connectcells(self.lts56, self.lts56, 0.105, 1, -1)
        connectcells(self.lts56, self.tuftIB5, 3.761, 1, -1)

        connectcells(self.bask56, self.nontuftRS6, 3.22, 1, -1)
        connectcells(self.bask56, self.tuftIB5, 1.324, 1, -1)
        connectcells(self.bask56, self.bask56, 0.755, 1, -1)

        '''
        Connections GABA NEW
        '''
        connectcells(self.bask23, self.LTS23, 0.00045, 1, -1)
        connectcells(self.axax23, self.syppyrFRB, 0.0008, 1, -1)

        connectcells(self.LTS23, self.axax23, 0.004, 1, -1)

        connectcells(self.bask23, self.spinstel4, 0.0004, 1, -1)
        connectcells(self.axax23, self.spinstel4, 0.0006, 1, -1)
        connectcells(self.LTS23, self.spinstel4, 0.000105, 1,-1)

        connectcells(self.axax23, self.nontuftRS6, 0.027, 1, -1)

        connectcells(self.LTS23, self.nontuftRS6, 0.0003, 1, -1)

        connectcells(self.LTS23, self.tuftIB5, 7.84, 1,-1)
        connectcells(self.LTS23, self.tuftRS5, 0.0002, 1,-1)

        connectcells(self.LTS23, self.axax56, 0.0045, 1, -1)
        connectcells(self.LTS23, self.lts56, 0.0002, 1, -1)

        connectcells(self.bask56, self.axax56, 0.071, 1, -1)
        connectcells(self.axax56, self.nontuftRS6, 0.26, 1, -1)
        connectcells(self.bask56, self.nontuftRS6, 0.007, 1, -1)

        connectcells(self.lts56, self.nontuftRS6, 1.86, 1, -1)
        connectcells(self.lts56, self.bask56, 0.16, 1, -1)
        connectcells(self.bask56, self.lts56, 0.22, 1, -1)
        connectcells(self.bask56, self.spinstel4, 0.25, 1, -1)
        connectcells(self.lts56, self.spinstel4, 0.34, 1, -1)
        connectcells(self.bask56, self.tuftRS5, 13.68, 1, -1)
        connectcells(self.lts56, self.tuftRS5, 7.275, 1, -1)
        connectcells(self.axax56, self.tuftRS5, 0.68, 1, -1)

        connectcells(self.lts56, self.syppyrRS, 4.1, 1, -1)
        connectcells(self.lts56, self.LTS23, 0.0002, 1, -1)

        connectcells(self.lts56, self.axax23, 0.0002, 1, -1)
        connectcells(self.lts56, self.bask23, 0.298, 1, -1)
        connectcells(self.axax56, self.syppyrRS, 0.017, 1, -1)



        logging.info('added conections')


    def addpool(self, cell_list, name="test"):
        '''
        Creates interneuronal pool and returns gids of pool
        Parameters
        ----------
        cell_list: list
            list of particular type of cell
        name: string
            name of neuronal pool
        Returns
        -------
        gids: list
            the list of neurons gids
        '''
        gids = []

        for i in range(rank, len(cell_list)-1, nhost):
            cell = cell_list[i]
            self.neurons.append(cell)
            self.data['cells'].append({
                'name': cell.name,
                'id': cell.id,
                'num': cell.number,
                'x': cell.x,
                'y' : cell.y,
                'z' : cell.z
            })

            gid = cell.number
            gids.append(gid)
            pc.set_gid2node(gid, rank)
            pc.cell(gid, cell._spike_detector)

        self.groups.append((gids, cell_list[0].name))

        return gids

    def addgener(self, start, freq, nums, r=True):
        '''
        Creates generator and returns generator gid
        Parameters
        ----------
        start: int
            generator start up
        freq: int
            generator frequency
        nums: int
            signals number
        Returns
        -------
        gid: int
            generator gid
        '''
        gid = 0
        gids = []

        for i in range(rank, 20, nhost):
            stim = h.NetStim()
            stim.number = nums
            if r:
                stim.start = random.uniform(start - 3, start + 3)
                stim.noise = 0.05
            else:
                stim.start = start
            stim.interval = int(1000 / freq)
            #skinstim.noise = 0.1
            self.neurons.append(stim)
            while pc.gid_exists(gid) != 0:
                gid += 1
            pc.set_gid2node(gid, rank)
            ncstim = h.NetCon(stim, None)
            pc.cell(gid, ncstim)

            gids.append(gid)

        return gids

def connectcells(pre, post, weight, delay, type, N = 50):
    ''' Connects with excitatory synapses
      Parameters
      ----------
      pre: list
          list of presynase neurons gids
      post: list
          list of postsynapse neurons gids
      weight: float
          weight of synapse
          used with Gaussself.Ian distribution
      delay: int
          synaptic delay
          used with Gaussself.Ian distribution
      type: synapse type 1 - AMPA; -1 - GABA; 0 - NMDA
      N: int
        number of synapses
    '''
    nsyn = random.randint(N-15, N)
    for i in post:
        if pc.gid_exists(i):
            for j in range(nsyn):
                srcgid = random.randint(pre[0], pre[-1])
                target = pc.gid2cell(i)
                if(type==1):
                    syn = target.AMPA_syns[j]
                    nc = pc.gid_connect(srcgid, syn)
                    AMPA_nclist.append(nc)
                elif(type==-1):
                    syn = target.GABA_syns[j]
                    nc = pc.gid_connect(srcgid, syn)
                    GABA_nclist.append(nc)
                elif (type == 0):
                    syn = target.NMDA_syns[j]
                    nc = pc.gid_connect(srcgid, syn)
                    NMDA_nclist.append(nc)
                    # nc.weight[0] = random.gauss(weight, weight / 6) # str
                nc.weight[0] = random.gauss(weight, weight / 5) * 5
                nc.delay = random.gauss(delay, 1 / 4)

def prun():
    ''' simulation control
    Parameters
    ----------
    speed: int
      duration of each layer
    '''
    pc.timeout(0)
    tstop = time_sim#25 + (6 * speed + 125) * step_number
    pc.set_maxstep(10 * ms)
    h.finitialize(-70 * mV)
    pc.psolve(tstop * ms)


def spike_recording(pool, extra = False):   #new
    '''Record spikes from gids
    Parameters
    ----------
    pool: list
      list of neurons gids
    Returns
    -------
    v_vec: list of h.Vector()
        recorded voltage
    '''
    v_vec = []
    for i in pool:
        cell = pc.gid2cell(i)
        v_vec.append(cell.v_vec)
    return v_vec


def spikeout(pool, name, v_vec):
    ''' Reports simulation results
      Parameters
      ----------
      pool: list
        list of neurons gids
      name: string
        pool name
      version: int
          test number
      v_vec: list of h.Vector()
          recorded voltage
    '''
    global rank
    pc.barrier()
    vec = h.Vector()
    for i in range(nhost):
        if i == rank:
            outavg = []
            for j in range(len(pool)):
                outavg.append(list(v_vec[j]))
            outavg = np.mean(np.array(outavg), axis=0, dtype=np.float32)
            vec = vec.from_python(outavg)
        pc.barrier()
    pc.barrier()
    result = pc.py_gather(vec, 0)
    if rank == 0:
        logging.info("start recording")
        result = np.mean(np.array(result), axis=0, dtype=np.float32)
        with hdf5.File('./results/voltage_{}.hdf5'.format(name),'w') as file:
            file.create_dataset('#0_step', data=np.array(result), compression="gzip")
    else:
        logging.info(rank)

def spiketimeout(pool, name, v_vec):
    ''' Reports simulation results
      Parameters
      ----------
      pool: list
        list of neurons gids
      name: string
        pool name
      version: int
          test number
      v_vec: list of h.Vector()
          recorded voltage
    '''
    global rank
    pc.barrier()
    vec = h.Vector()
    for i in range(nhost):
        if i == rank:
            outavg = []
            for j in range(len(pool)):
                if len(list(v_vec[j])) > 0:
                    outavg.append(list(v_vec[j]))
            flat_outavg = [item for sublist in outavg for item in sublist]
            vec = vec.from_python(flat_outavg)
        pc.barrier()
    pc.barrier()
    result = pc.py_gather(outavg, 0)
    if rank == 0:
        logging.info("start recording")
        flat_result = [item for sublist in result for item in sublist]
        with open('./results/spiketime_{}.txt'.format(name),'w') as spk_file:
            for time in flat_result:
                for t in time:
                    spk_file.write(str(t)+"\n")
    else:
        logging.info(rank)

def spike_time_rec(pool, th=0):
    v_vec = []
    for i in pool:
        cell = pc.gid2cell(i)
        vec = h.Vector()
        cell._spike_detector.threshold = th
        cell._spike_detector.record(vec)
        v_vec.append(vec)
    return v_vec

def finish():
    ''' proper exit '''
    pc.runworker()
    pc.done()
    # print("hi after finish")
    h.quit()

if __name__ == '__main__':
    '''
    CC_c: cpg
        topology of cortical column
    '''
    k_nrns = 0
    k_name = 1

    CC_c = CC_circuit()
    logging.info("created")
    recorders = []
    spike_rec = []

    for group in CC_c.groups:
        recorders.append(spike_recording(group[k_nrns]))
        spike_rec.append(spike_time_rec(group[k_nrns]))

    logging.info("added recorders")

    print("- " * 10, "\nstart")
    prun()
    print("- " * 10, "\nend")

    for group, recorder in zip(CC_c.groups, recorders):
        spikeout(group[k_nrns], group[k_name], recorder)

    for group, recorder in zip(CC_c.groups, spike_rec):
        spiketimeout(group[k_nrns], group[k_name], recorder)

    logging.info("done")


    finish()
