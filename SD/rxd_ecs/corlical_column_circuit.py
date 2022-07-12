import logging
import json

#from SD.rxd_ecs.Thalamus import thalamus_cell

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
from neuron.units import ms, mV
import numpy as np
h.load_file("stdgui.hoc")
pc = h.ParallelContext()
rank = int(pc.id())
nhost = int(pc.nhost())

AMPA_nclist = []
GABA_nclist = []
NMDA_nclist = []

# rxd.options.enable.extracellular = True

# simulation parameters
time_sim = 300
Lx, Ly, Lz = 200, 200, 1700
Kceil = 15.0  # threshold used to determine wave speed
Ncell = int(9e4 * (Lx * Ly * Lz * 1e-9))

#L2/3 (0-400)
Nbask23 = 90 #59
Naxax23 = 90 #59
NLTS23 = 90 #59
NsyppyrFRB = 40
NsyppyrRS = 500
#L4 (400-700)
Nspinstel4 = 240
Nbask4=40
NtuftIB5 = 400
Bask_4 = 235 #235 bask4
#L5 (700-1200)
NtuftRS5 = 200
Nbask56 = 100

#L5/6 (700-1700)
Naxax56 = 100
NLTS56 = 250

#L6(1200-1700)
NnontuftRS6 = 250

#tlms
NTCR = 250
NnRT = 100

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
        self.layers = []

        logging.info('start creating neurons')

        self.syppyrFRB = []

        num=0

        epi=int(value*NsyppyrFRB/100)
        logging.info(f'epi{epi}')

        for i in range(rank, NsyppyrFRB-epi, nhost):
            self.syppyrFRB.append(self.addpool(SyppyrFRB(
                    random.uniform(somaR,Lx-somaR),
                    random.uniform(somaR,Ly-somaR),
                    random.uniform( -850+somaR,-450),
                    i+num)))

        num+=NsyppyrFRB

        if value!=0:
            for i in range(rank, epi, nhost):
                self.syppyrFRB.append(self.addpool(EpilepsySyppyrFRB(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-850 + somaR, -450),
                    i + num)))

        num+=epi

        self.groups.append((self.syppyrFRB, pc.gid2cell(self.syppyrFRB[0]).name))
        self.layers.append((self.syppyrFRB, pc.gid2cell(self.syppyrFRB[0]).id))
        logging.info(f'fbr{self.syppyrFRB}')

        self.syppyrRS = []
        epi=int(value*NsyppyrRS/100)
        for i in range(rank, NsyppyrRS-epi, nhost):
            self.syppyrRS.append(self.addpool(SyppyrRS(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-850+somaR,-450),
            i+num)))

        num+=NsyppyrRS-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                self.syppyrRS.append(self.addpool(EpilepsySyppyrRS(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-850 + somaR, -450),
                    i + num)))

        num+=epi
        self.groups.append((self.syppyrRS, pc.gid2cell(self.syppyrRS[0]).name))
        self.layers.append((self.syppyrRS, pc.gid2cell(self.syppyrRS[0]).id))
        logging.info(f'rs{self.syppyrRS}')

        self.LTS23 = []
        for i in range(rank, NLTS23, nhost):
            self.LTS23.append(self.addpool(LTS23(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-850+somaR,-450),
            i+num)))

        self.groups.append((self.LTS23, pc.gid2cell(self.LTS23[0]).name))
        self.layers.append((self.LTS23, pc.gid2cell(self.LTS23[0]).id))
        num+=NLTS23

        self.bask23=[]
        for i in range(rank, Nbask23, nhost):
            self.bask23.append(self.addpool(Bask23(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-850+somaR,-450),
            i+num)))

        self.groups.append((self.bask23, pc.gid2cell(self.bask23[0]).name))
        self.layers.append((self.bask23, pc.gid2cell(self.bask23[0]).id))

        num+=Nbask23

        self.axax23=[]
        for i in range(rank, Naxax23, nhost):
            self.axax23.append(self.addpool(Axax23(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-850+somaR,-450),
            i+num)))

        self.groups.append((self.axax23, pc.gid2cell(self.axax23[0]).name))
        self.layers.append((self.axax23, pc.gid2cell(self.axax23[0]).id))
        num+=Naxax23

        #400-700
        self.spinstel4=[]
        epi=int(value*Nspinstel4/100)
        for i in range(rank, Nspinstel4-epi, nhost):
            self.spinstel4.append(self.addpool(Spinstel4(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-450,-150), i+num)))

        num+=Nspinstel4-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                self.spinstel4.append(self.addpool(EpilepsySpinstel4(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-450, -150), i + num)))

        self.groups.append((self.spinstel4, pc.gid2cell(self.spinstel4[0]).name))
        self.layers.append((self.spinstel4, pc.gid2cell(self.spinstel4[0]).id))
        num+=epi

        self.bask4=[]
        for i in range(rank, Nbask4, nhost):
            self.bask4.append(self.addpool(Bask4(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-450,-150), i+num)))

        self.groups.append((self.bask4, pc.gid2cell(self.bask4[0]).name))
        self.layers.append((self.bask4, pc.gid2cell(self.bask4[0]).id))
        num+=Nbask4

        self.tuftIB5=[]
        epi=int(value*NtuftIB5/100)
        for i in range(rank, NtuftIB5-epi, nhost):
            self.tuftIB5.append(self.addpool(TuftIB5(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,50), i+num)))
        num+=NtuftIB5-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                self.tuftIB5.append(self.addpool(EpilepsyTuftIB5(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-150, 50), i + num)))

        self.groups.append((self.tuftIB5, pc.gid2cell(self.tuftIB5[0]).name))
        self.layers.append((self.tuftIB5, pc.gid2cell(self.tuftIB5[0]).id))
        num+=epi

        #700-1200
        self.tuftRS5=[]
        epi=int(value*NtuftRS5/100)
        for i in range(rank, NtuftRS5-epi, nhost):
            self.tuftRS5.append(self.addpool(TuftRS5(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,350), i+num)))
        num+=NtuftRS5-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                self.tuftRS5.append(self.addpool(EpilepsyTuftRS5(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-150, 350), i + num)))

        self.groups.append((self.tuftRS5, pc.gid2cell(self.tuftRS5[0]).name))
        self.layers.append((self.tuftRS5, pc.gid2cell(self.tuftRS5[0]).id))
        num+=epi

        self.bask56=[]
        for i in range(rank, Nbask56, nhost):
            self.bask56.append(self.addpool(Bask56(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,350), i+num)))

        self.groups.append((self.bask56, pc.gid2cell(self.bask56[0]).name))
        self.layers.append((self.bask56, pc.gid2cell(self.bask56[0]).id))
        num+=Nbask56

        #700-1700
        self.axax56=[]
        for i in range(rank, Naxax56, nhost):
            self.axax56.append(self.addpool(Axax56(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,850), i+num)))

        self.groups.append((self.axax56, pc.gid2cell(self.axax56[0]).name))
        self.layers.append((self.axax56, pc.gid2cell(self.axax56[0]).id))
        num+=Naxax56

        self.lts56=[]
        for i in range(rank, NLTS56, nhost):
            self.lts56.append(self.addpool(LTS56(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(-150,850), i+num)))

        self.groups.append((self.lts56, pc.gid2cell(self.lts56[0]).name))
        self.layers.append((self.lts56, pc.gid2cell(self.lts56[0]).id))
        num+=NLTS56

        self.nontuftRS6=[]
        epi=int(value*NnontuftRS6/100)
        for i in range(rank, NnontuftRS6-epi, nhost):
            self.nontuftRS6.append(self.addpool(NontuftRS6(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(350,850-somaR), i+num)))
        num+=NnontuftRS6-epi

        if value!=0:
            for i in range(rank, epi, nhost):
                self.nontuftRS6.append(self.addpool(EpilepsyNontuftRS6(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(350, 850 - somaR), i + num)))
        num += epi
        self.groups.append((self.nontuftRS6, pc.gid2cell(self.nontuftRS6[0]).name))
        self.layers.append((self.nontuftRS6, pc.gid2cell(self.nontuftRS6[0]).id))


        self.tcr=[]
        for i in range(rank, NTCR, nhost):
            self.tcr.append(self.addpool(TCR(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(1000,1300-somaR), i+num)))

        self.groups.append((self.tcr, pc.gid2cell(self.tcr[0]).name))
        self.layers.append((self.tcr, pc.gid2cell(self.tcr[0]).id))
        num +=NTCR

        self.nrt=[]
        for i in range(rank, NnRT, nhost):
            self.nrt.append(self.addpool(nRT(
            random.uniform(somaR,Lx-somaR),
            random.uniform(somaR,Ly-somaR),
            random.uniform(1100,1300-somaR), i+num)))

        self.groups.append((self.nrt, pc.gid2cell(self.nrt[0]).name))
        self.layers.append((self.nrt, pc.gid2cell(self.nrt[0]).id))
        num +=NnRT

        self.thalamus_generator = self.addgener(2, 10, 10)

        #rec_neurons16=[]
        #for i in range(rank, NnRT, nhost):
        #    rec_neurons16.append(thalamus_cell(
        #        random.uniform(somaR,Lx-somaR),
        #        random.uniform(somaR,Ly-somaR),
        #        random.uniform(-500,-200-somaR),i+num))
        #self.nt=self.addpool(rec_neurons16)
        #num+=NnRT



        logging.info('created neurons, start adding conections')

        ''' CONNECTIONS '''

        '''
        Connections AMPA
        '''
        '''connections thalamus'''
        connectcells(self.thalamus_generator, self.tcr, 0.85, 1, 1)
        connectcells(self.tcr, self.spinstel4, 0.5, 1, 1)
        connectcells(self.tcr, self.nrt, 0.5, 1, 1)
        connectcells(self.tcr, self.tuftRS5, 0.5, 1, 1)
        connectcells(self.tcr, self.tuftIB5, 0.5, 1, 1)
        connectcells(self.tcr, self.syppyrFRB, 0.25, 1, 1)
        connectcells(self.tcr, self.syppyrRS, 0.25, 1, 1)
        connectcells(self.nrt, self.bask23, 0.25, 1, 1)
        connectcells(self.nrt, self.axax23, 0.25, 1, 1)

        connectcells(self.syppyrFRB, self.bask23, 0.23, 1, 1)
        '''Возможно стоит поделить на 2 количество syn у syppyrRS и syppyrFRB add NMDA'''
        connectcells(self.syppyrFRB, self.syppyrFRB, 6.37, 1, 1)
        connectcells(self.syppyrFRB, self.syppyrFRB, 2.37, 1, 0)
        connectcells(self.syppyrFRB, self.syppyrRS, 6.37, 1, 1)
        connectcells(self.syppyrFRB, self.syppyrRS, 2.37, 1, 0)

        connectcells(self.syppyrFRB, self.axax23, 0.08, 1, 1)
        connectcells(self.syppyrFRB, self.tuftRS5, 7.27, 1, 1)
        connectcells(self.syppyrFRB, self.nontuftRS6, 1.46, 1, 1)
        connectcells(self.syppyrFRB, self.nontuftRS6, 0.46, 1, 0)
        connectcells(self.syppyrFRB, self.bask56, 0.096, 1, 1)
        connectcells(self.syppyrFRB, self.tuftIB5, 3.44, 1, 1)
        connectcells(self.syppyrFRB, self.tuftIB5, 1.44, 1, 0)

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
        connectcells(self.syppyrRS, self.tuftRS5, 3.44, 1, 1)
        connectcells(self.syppyrRS, self.tuftRS5, 1.44, 1, 0)
        connectcells(self.syppyrRS, self.bask56, 0.11, 1, 1)
        connectcells(self.syppyrRS, self.nontuftRS6, 1.46, 1, 1)
        connectcells(self.syppyrRS, self.spinstel4, 0.98, 1, 1)
        connectcells(self.syppyrRS, self.spinstel4, 0.5, 1, 0)

        connectcells(self.spinstel4, self.bask4, 0.031, 1, 1)
        connectcells(self.spinstel4, self.LTS23, 0.3, 1, 1)
        connectcells(self.spinstel4, self.spinstel4, 0.099, 1, 1)
        connectcells(self.spinstel4, self.spinstel4, 0.099, 1, 0)
        connectcells(self.spinstel4, self.bask23, 0.02, 1, 1)
        connectcells(self.spinstel4, self.syppyrFRB, 0.68, 1, 1)
        connectcells(self.spinstel4, self.syppyrFRB, 0.68, 1, 0)
        connectcells(self.spinstel4, self.syppyrRS, 0.58, 1, 1)
        connectcells(self.spinstel4, self.syppyrRS, 0.58, 1, 0)
        connectcells(self.spinstel4, self.bask56, 0.01, 1, 1)
        connectcells(self.spinstel4, self.nontuftRS6, 0.14, 1, 1)
        connectcells(self.spinstel4, self.nontuftRS6, 0.14, 1, 0)
        connectcells(self.spinstel4, self.axax56, 0.004, 1, 1)
        connectcells(self.spinstel4, self.lts56, 0.03, 1, 1)
        connectcells(self.spinstel4, self.axax23, 0.005, 1, 1)

        connectcells(self.tuftRS5, self.tuftRS5, 2.25, 1, 1)
        connectcells(self.tuftRS5, self.tuftRS5, 1.25, 1, 0)
        connectcells(self.tuftRS5, self.axax56, 0.027, 1, 1)
        connectcells(self.tuftRS5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftRS5, self.nontuftRS6, 1.164, 1, 1)
        connectcells(self.tuftRS5, self.spinstel4, 0.161, 1, 1)
        '''Возможно поделить на 2 количество syn в следующих двух соединениях add NMDA'''
        connectcells(self.tuftRS5, self.syppyrRS, 0.36, 1, 1)
        connectcells(self.tuftRS5, self.syppyrFRB, 0.36, 1, 1)
        connectcells(self.tuftRS5, self.syppyrRS, 0.36, 1, 0)
        connectcells(self.tuftRS5, self.syppyrFRB, 0.36, 1, 0)
        connectcells(self.tuftRS5, self.bask23, 0.017, 1, 1)
        connectcells(self.tuftRS5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftRS5, self.axax23, 0.004, 1, 1)
        connectcells(self.tuftRS5, self.LTS23, 0.019, 1, 1)
        connectcells(self.tuftRS5, self.lts56, 0.284, 1, 1)
        connectcells(self.tuftRS5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftRS5, self.tuftIB5, 1.916, 1, 1)
        connectcells(self.tuftRS5, self.tuftIB5, 0.916, 1, 0)


        connectcells(self.tuftIB5, self.LTS23, 0.013, 1, 1)
        connectcells(self.tuftIB5, self.lts56, 0.279, 1, 1)
        connectcells(self.tuftIB5, self.axax56, 0.027, 1, 1)
        connectcells(self.tuftIB5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftIB5, self.tuftRS5, 1.916, 1, 1)
        connectcells(self.tuftIB5, self.axax23, 0.004, 1, 1)
        connectcells(self.tuftIB5, self.syppyrRS, 0.36, 1, 1)
        connectcells(self.tuftIB5, self.syppyrFRB, 0.36, 1, 1)
        connectcells(self.tuftIB5, self.nontuftRS6, 1.164, 1, 1)
        connectcells(self.tuftIB5, self.syppyrRS, 0.36, 1, 0)
        connectcells(self.tuftIB5, self.syppyrFRB, 0.36, 1, 0)
        connectcells(self.tuftIB5, self.nontuftRS6, 0.64, 1, 0)
        connectcells(self.tuftIB5, self.spinstel4, 0.156, 1, 1)
        connectcells(self.tuftIB5, self.bask23, 0.017, 1, 1)
        connectcells(self.tuftIB5, self.tuftIB5, 1.916, 1, 1)
        connectcells(self.tuftIB5, self.tuftIB5, 0.916, 1, 0)


        connectcells(self.nontuftRS6, self.nontuftRS6, 0.68, 1, 1)
        connectcells(self.nontuftRS6, self.bask23, 0.004, 1, 1)
        connectcells(self.nontuftRS6, self.nontuftRS6, 0.68, 1, 1)
        connectcells(self.nontuftRS6, self.spinstel4, 0.044, 1, 1)
        connectcells(self.nontuftRS6, self.syppyrFRB, 0.093, 1, 1)
        connectcells(self.nontuftRS6, self.syppyrRS, 0.093, 1, 1)
        connectcells(self.nontuftRS6, self.bask56, 0.057, 1, 1)
        connectcells(self.nontuftRS6, self.axax56, 0.014, 1, 1)
        connectcells(self.nontuftRS6, self.lts56, 0.16, 1, 1)
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


    def addpool(self, cell, name="test"):
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

        # for i in range(rank, len(cell_list)-1, nhost):
            # cell = cell_list[i]
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
        # gids.append(gid)
        pc.set_gid2node(gid, rank)
        pc.cell(gid, cell._spike_detector)

        return gid

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

        for i in range(rank, nhost+1, nhost):
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
                nc.weight[0] = random.gauss(weight, weight / 5) * 2
                nc.delay = random.gauss(delay, 1 / 4) + 1 # idk but should be more than 1 for parallel

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

def spiketimeout(pool, id, name, v_vec):
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
        with open('./results/spiketime_{}_{}.txt'.format(id, name),'w') as spk_file:
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

    for group, layer, recorder in zip(CC_c.groups, CC_c.layers, spike_rec):
        spiketimeout(group[k_nrns], layer[k_name], group[k_name], recorder)


    logging.info("done")


    finish()
