import logging
import json

# from SD.rxd_ecs.Thalamus import thalamus_cell

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
num_syn = [0]

conn_dict = {}

# rxd.options.enable.extracellular = True

# simulation parameters
time_sim = 150
Lx, Ly, Lz = 200, 200, 1700
Kcell = 15.0  # threshold used to determine wave speed
Ncell = int(9e4 * (Lx * Ly * Lz * 1e-9))

# L2/3 (0-400)
Nbask23 = 90  # 59
Naxax23 = 90  # 59
NLTS23 = 90  # 59
NsyppyrFRB = 50  # 40
NsyppyrRS = 500  # 1000
# L4 (400-700)
Nspinstel4 = 240
NLTS4 = 90  # 40
# L5 (700-1200)
NtuftRS5 = 200
Nbask56 = 100
NtuftIB5 = 250  # 800 #400

# L5/6 (700-1700)
Naxax56 = 100
NLTS56 = 100  # 250

# L6(1200-1700)
NnontuftRS6 = 250  # 500  # 250

# tlms
NTCR = 250  # 100  # 250
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

# 0-400

data = {}
data['cells'] = []

value = 0  # 100 #% epilepsy


class CC_circuit:
    def __init__(self):

        self.data = {}
        self.data['cells'] = []
        self.groups = []
        self.neurons = []
        self.layers = []

        nsyn_AMPA = 0
        nsyn_GABA = 0
        nsyn_NMDA = 0

        logging.info('start creating neurons')

        self.syppyrFRB = []

        num = 0

        epi = int(value * NsyppyrFRB / 100)
        logging.info(f'epi{epi}')

        for i in range(rank, NsyppyrFRB - epi, nhost):
            self.syppyrFRB.append(self.addpool(SyppyrFRB(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-850 + somaR, -450),
                i + num)))

        num += NsyppyrFRB - epi

        if value != 0:
            for i in range(rank, epi, nhost):
                self.syppyrFRB.append(self.addpool(EpilepsySyppyrFRB(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-850 + somaR, -450),
                    i + num)))

        num += epi

        self.groups.append((self.syppyrFRB, pc.gid2cell(self.syppyrFRB[0]).name))
        self.layers.append((self.syppyrFRB, pc.gid2cell(self.syppyrFRB[0]).id))
        logging.info(f'fbr{self.syppyrFRB}')

        self.syppyrRS = []
        epi = int(value * NsyppyrRS / 100)
        for i in range(rank, NsyppyrRS - epi, nhost):
            self.syppyrRS.append(self.addpool(SyppyrRS(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-850 + somaR, -450),
                i + num)))

        num += NsyppyrRS - epi

        if value != 0:
            for i in range(rank, epi, nhost):
                self.syppyrRS.append(self.addpool(EpilepsySyppyrRS(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-850 + somaR, -450),
                    i + num)))

        num += epi
        self.groups.append((self.syppyrRS, pc.gid2cell(self.syppyrRS[0]).name))
        self.layers.append((self.syppyrRS, pc.gid2cell(self.syppyrRS[0]).id))
        logging.info(f'rs{self.syppyrRS}')

        self.LTS23 = []
        for i in range(rank, NLTS23, nhost):
            self.LTS23.append(self.addpool(LTS23(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-850 + somaR, -450),
                i + num)))

        self.groups.append((self.LTS23, pc.gid2cell(self.LTS23[0]).name))
        self.layers.append((self.LTS23, pc.gid2cell(self.LTS23[0]).id))
        num += NLTS23

        self.bask23 = []
        for i in range(rank, Nbask23, nhost):
            self.bask23.append(self.addpool(Bask23(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-850 + somaR, -450),
                i + num)))

        self.groups.append((self.bask23, pc.gid2cell(self.bask23[0]).name))
        self.layers.append((self.bask23, pc.gid2cell(self.bask23[0]).id))

        num += Nbask23

        self.axax23 = []
        for i in range(rank, Naxax23, nhost):
            self.axax23.append(self.addpool(Axax23(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-850 + somaR, -450),
                i + num)))

        self.groups.append((self.axax23, pc.gid2cell(self.axax23[0]).name))
        self.layers.append((self.axax23, pc.gid2cell(self.axax23[0]).id))
        num += Naxax23

        # 400-700
        self.spinstel4 = []
        epi = int(value * Nspinstel4 / 100)
        for i in range(rank, Nspinstel4 - epi, nhost):
            self.spinstel4.append(self.addpool(Spinstel4(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-450, -150), i + num)))

        num += Nspinstel4 - epi

        if value != 0:
            for i in range(rank, epi, nhost):
                self.spinstel4.append(self.addpool(EpilepsySpinstel4(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-450, -150), i + num)))

        self.groups.append((self.spinstel4, pc.gid2cell(self.spinstel4[0]).name))
        self.layers.append((self.spinstel4, pc.gid2cell(self.spinstel4[0]).id))
        num += epi

        self.LTS4 = []
        for i in range(rank, NLTS4, nhost):
            self.LTS4.append(self.addpool(LTS4(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-450, -150), i + num)))

        self.groups.append((self.LTS4, pc.gid2cell(self.LTS4[0]).name))
        self.layers.append((self.LTS4, pc.gid2cell(self.LTS4[0]).id))
        num += NLTS4

        self.tuftIB5 = []
        epi = int(value * NtuftIB5 / 100)
        for i in range(rank, NtuftIB5 - epi, nhost):
            self.tuftIB5.append(self.addpool(TuftIB5(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-150, 350), i + num)))
        num += NtuftIB5 - epi

        if value != 0:
            for i in range(rank, epi, nhost):
                self.tuftIB5.append(self.addpool(EpilepsyTuftIB5(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-150, 350), i + num)))

        self.groups.append((self.tuftIB5, pc.gid2cell(self.tuftIB5[0]).name))
        self.layers.append((self.tuftIB5, pc.gid2cell(self.tuftIB5[0]).id))
        num += epi

        # 700-1200
        self.tuftRS5 = []
        epi = int(value * NtuftRS5 / 100)
        for i in range(rank, NtuftRS5 - epi, nhost):
            self.tuftRS5.append(self.addpool(TuftRS5(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-150, 350), i + num)))
        num += NtuftRS5 - epi

        if value != 0:
            for i in range(rank, epi, nhost):
                self.tuftRS5.append(self.addpool(EpilepsyTuftRS5(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(-150, 350), i + num)))

        self.groups.append((self.tuftRS5, pc.gid2cell(self.tuftRS5[0]).name))
        self.layers.append((self.tuftRS5, pc.gid2cell(self.tuftRS5[0]).id))
        num += epi

        self.bask56 = []
        for i in range(rank, Nbask56, nhost):
            self.bask56.append(self.addpool(Bask56(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-150, 350), i + num)))

        self.groups.append((self.bask56, pc.gid2cell(self.bask56[0]).name))
        self.layers.append((self.bask56, pc.gid2cell(self.bask56[0]).id))
        num += Nbask56

        # 700-1700
        self.axax56 = []
        for i in range(rank, Naxax56, nhost):
            self.axax56.append(self.addpool(Axax56(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-150, 350), i + num)))

        self.groups.append((self.axax56, pc.gid2cell(self.axax56[0]).name))
        self.layers.append((self.axax56, pc.gid2cell(self.axax56[0]).id))
        num += Naxax56

        self.lts56 = []
        for i in range(rank, NLTS56, nhost):
            self.lts56.append(self.addpool(LTS56(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(-150, 350), i + num)))

        self.groups.append((self.lts56, pc.gid2cell(self.lts56[0]).name))
        self.layers.append((self.lts56, pc.gid2cell(self.lts56[0]).id))
        num += NLTS56

        self.nontuftRS6 = []
        epi = int(value * NnontuftRS6 / 100)
        for i in range(rank, NnontuftRS6 - epi, nhost):
            self.nontuftRS6.append(self.addpool(NontuftRS6(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(350, 850 - somaR), i + num)))
        num += NnontuftRS6 - epi

        if value != 0:
            for i in range(rank, epi, nhost):
                self.nontuftRS6.append(self.addpool(EpilepsyNontuftRS6(
                    random.uniform(somaR, Lx - somaR),
                    random.uniform(somaR, Ly - somaR),
                    random.uniform(350, 850 - somaR), i + num)))
        num += epi
        self.groups.append((self.nontuftRS6, pc.gid2cell(self.nontuftRS6[0]).name))
        self.layers.append((self.nontuftRS6, pc.gid2cell(self.nontuftRS6[0]).id))

        self.tcr = []
        for i in range(rank, NTCR, nhost):
            self.tcr.append(self.addpool(TCR(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(1000, 1300 - somaR), i + num)))

        self.groups.append((self.tcr, pc.gid2cell(self.tcr[0]).name))
        self.layers.append((self.tcr, pc.gid2cell(self.tcr[0]).id))
        num += NTCR

        self.nrt = []
        for i in range(rank, NnRT, nhost):
            self.nrt.append(self.addpool(nRT(
                random.uniform(somaR, Lx - somaR),
                random.uniform(somaR, Ly - somaR),
                random.uniform(1100, 1300 - somaR), i + num)))

        self.groups.append((self.nrt, pc.gid2cell(self.nrt[0]).name))
        self.layers.append((self.nrt, pc.gid2cell(self.nrt[0]).id))
        num += NnRT

        self.thalamus_generator = self.addgener(2, 10, 10)

        # rec_neurons16=[]
        # for i in range(rank, NnRT, nhost):
        #    rec_neurons16.append(thalamus_cell(
        #        random.uniform(somaR,Lx-somaR),
        #        random.uniform(somaR,Ly-somaR),
        #        random.uniform(-500,-200-somaR),i+num))
        # self.nt=self.addpool(rec_neurons16)
        # num+=NnRT

        logging.info('created neurons, start adding conections')

        ''' CONNECTIONS '''

        '''connections thalamus'''
        connectcells(self.thalamus_generator, self.tcr, 5, 1, 1)
        connectcells(self.thalamus_generator, self.nrt, 5, 1, 1)
        connectcells(self.tcr, self.spinstel4, 5, 1, 1)
        connectcells(self.tcr, self.spinstel4, 5/3, 1, 0)
        connectcells(self.tcr, self.nrt, 3, 1, 1)
        connectcells(self.tcr, self.nrt, 3/3, 1, 0)
        # connectcells(self.tcr, self.tuftRS5, 3, 1, 1)
        # connectcells(self.tcr, self.tuftRS5, 3/3, 1, 0)
        # connectcells(self.tcr, self.tuftIB5, 3, 1, 1)
        # connectcells(self.tcr, self.tuftIB5, 3/3, 1, 0)

        # connectcells(self.tcr, self.bask56, 1.5, 1, 1)
        # connectcells(self.tcr, self.bask56, 1.5/3, 1, 0)
        # connectcells(self.tcr, self.axax56, 1.5, 1, 1)
        # connectcells(self.tcr, self.axax56, 1.5/3, 1, 0)
        # connectcells(self.tcr, self.nontuftRS6, 1.5, 1, 1)
        # connectcells(self.tcr, self.nontuftRS6, 1.5/3, 1, 0)

        # connectcells(self.tcr, self.syppyrFRB, 0.25/2, 1, 1)
        # connectcells(self.tcr, self.syppyrFRB, 0.083, 1, 0)
        # connectcells(self.tcr, self.syppyrRS, 0.25/2, 1, 1)
        # connectcells(self.tcr, self.syppyrRS, 0.083, 1, 0)
        # connectcells(self.nrt, self.bask23, 0.25/2, 1, 1)
        # connectcells(self.nrt, self.axax23, 0.25/2, 1, 1)
        connectcells(self.nrt, self.tcr, 3, 1, -1)
        connectcells(self.nrt, self.nrt, 3/3, 1, -1)

        '''
        Connections AMPA and NMDA
        '''

        connectcells(self.syppyrFRB, self.bask23, 0.23, 1, 1)
        connectcells(self.syppyrFRB, self.bask23, 0.077, 1, 0)
        connectcells(self.syppyrFRB, self.syppyrFRB, 9.373/3, 1, 1)
        connectcells(self.syppyrFRB, self.syppyrFRB, 3.124/2, 1, 0)
        connectcells(self.syppyrFRB, self.syppyrRS, 9.373/3, 1, 1)
        connectcells(self.syppyrFRB, self.syppyrRS, 3.124/2, 1, 0)

        connectcells(self.syppyrFRB, self.axax23, 0.08*2, 1, 1)
        connectcells(self.syppyrFRB, self.axax23, 0.027*2, 1, 0)
        connectcells(self.syppyrFRB, self.tuftRS5, 4.444, 1, 1)
        connectcells(self.syppyrFRB, self.tuftRS5, 1.48, 1, 0)
        # connectcells(self.syppyrFRB, self.bask56, 4.444, 1, 1)
        # connectcells(self.syppyrFRB, self.bask56, 1.48, 1, 0)

        connectcells(self.syppyrFRB, self.nontuftRS6, 1.485, 1, 1)
        connectcells(self.syppyrFRB, self.nontuftRS6, 0.495, 1, 0)
        # connectcells(self.syppyrFRB, self.axax56, 1.485, 1, 1)
        # connectcells(self.syppyrFRB, self.axax56, 0.495, 1, 0)

        connectcells(self.syppyrFRB, self.bask56, 0.1113, 1, 1)
        connectcells(self.syppyrFRB, self.bask56, 0.0371, 1, 0)
        connectcells(self.syppyrFRB, self.tuftIB5, 4.444, 1, 1)
        connectcells(self.syppyrFRB, self.tuftIB5, 1.48, 1, 0)
        # connectcells(self.syppyrFRB, self.lts56, 4.444, 1, 1)
        # connectcells(self.syppyrFRB, self.lts56, 1.48, 1, 0)

        connectcells(self.syppyrFRB, self.lts56, 0.27, 1, 1)
        connectcells(self.syppyrFRB, self.axax56, 0.03, 1, 1)
        connectcells(self.syppyrFRB, self.axax56, 0.01, 1, 0)
        connectcells(self.syppyrFRB, self.LTS23, 0.55, 1, 1)
        connectcells(self.syppyrFRB, self.LTS23, 0.18, 1, 0)

        connectcells(self.syppyrFRB, self.spinstel4, 0.3253, 1, 0)

        connectcells(self.syppyrRS, self.LTS23, 0.55, 1, 1)
        connectcells(self.syppyrRS, self.LTS23, 0.18, 1, 0)
        connectcells(self.syppyrRS, self.bask23, 0.228, 1, 1)
        connectcells(self.syppyrRS, self.bask23, 0.076, 1, 0)
        connectcells(self.syppyrRS, self.axax23, 0.08, 1, 1)
        connectcells(self.syppyrRS, self.axax23, 0.027, 1, 0)
        connectcells(self.syppyrRS, self.syppyrFRB, 9.37, 1, 1)
        connectcells(self.syppyrRS, self.syppyrFRB, 3.124, 1, 0)
        connectcells(self.syppyrRS, self.tuftIB5, 4.95, 1, 1)
        connectcells(self.syppyrRS, self.tuftIB5, 1.65, 1, 0)
        # connectcells(self.syppyrRS, self.lts56, 4.95, 1, 1)
        # connectcells(self.syppyrRS, self.lts56, 1.65, 1, 0)

        connectcells(self.syppyrRS, self.lts56, 0.53, 1, 1)
        connectcells(self.syppyrRS, self.lts56, 0.177, 1, 0)
        connectcells(self.syppyrRS, self.axax56, 0.03, 1, 1)
        connectcells(self.syppyrRS, self.axax56, 0.01, 1, 0)
        connectcells(self.syppyrRS, self.syppyrRS, 9.37, 1, 1)
        connectcells(self.syppyrRS, self.syppyrRS, 3.124, 1, 0)
        connectcells(self.syppyrRS, self.tuftRS5, 4.44, 1, 1)
        connectcells(self.syppyrRS, self.tuftRS5, 1.48, 1, 0)
        # connectcells(self.syppyrRS, self.bask56, 4.44, 1, 1)
        # connectcells(self.syppyrRS, self.bask56, 1.48, 1, 0)

        connectcells(self.syppyrRS, self.bask56, 0.11, 1, 1)
        connectcells(self.syppyrRS, self.bask56, 0.037, 1, 0)
        connectcells(self.syppyrRS, self.nontuftRS6, 1.48, 1, 1)
        connectcells(self.syppyrRS, self.nontuftRS6, 0.49, 1, 0)
        # connectcells(self.syppyrRS, self.axax56, 1.48, 1, 1)
        # connectcells(self.syppyrRS, self.axax56, 0.49, 1, 0)

        connectcells(self.syppyrRS, self.spinstel4, 0.3253, 1, 0)

        connectcells(self.spinstel4, self.LTS4, 0.03, 1, 1)
        connectcells(self.spinstel4, self.LTS4, 0.0033*2, 1, 0)
        connectcells(self.LTS4, self.spinstel4, 0.02, 1, 1)
        connectcells(self.LTS4, self.spinstel4, 0.0033, 1, 0)
        connectcells(self.spinstel4, self.LTS23, 0.3*2, 1, 1)
        connectcells(self.spinstel4, self.LTS23, 0.1*2, 1, 0)
        connectcells(self.spinstel4, self.spinstel4, 0.099*5, 1, 1)
        connectcells(self.spinstel4, self.spinstel4, 0.033*5, 1, 0)
        connectcells(self.spinstel4, self.bask23, 0.02*2, 1, 1)
        connectcells(self.spinstel4, self.bask23, 0.0067*2, 1, 0)
        connectcells(self.spinstel4, self.syppyrFRB, 0.58*2, 1, 1)
        connectcells(self.spinstel4, self.syppyrFRB, 0.19*2, 1, 0)
        connectcells(self.spinstel4, self.syppyrRS, 0.58*1, 1, 1)
        connectcells(self.spinstel4, self.syppyrRS, 0.19*2, 1, 0)
        connectcells(self.spinstel4, self.bask56, 0.0108*2, 1, 1)
        connectcells(self.spinstel4, self.bask56, 0.0036*2, 1, 0)
        connectcells(self.spinstel4, self.nontuftRS6, 0.14*2, 1, 1)
        connectcells(self.spinstel4, self.nontuftRS6, 0.0467*2, 1, 0)
        # connectcells(self.spinstel4, self.axax56, 0.14, 1, 1)
        # connectcells(self.spinstel4, self.axax56, 0.0467, 1, 0)

        connectcells(self.spinstel4, self.axax23, 0.0054*5, 1, 1)
        connectcells(self.spinstel4, self.axax23, 0.0018*5, 1, 0)
        connectcells(self.spinstel4, self.axax56, 0.0036*2, 1, 1)
        connectcells(self.spinstel4, self.axax56, 0.0012*2, 1, 0)
        connectcells(self.spinstel4, self.lts56, 0.031*2, 1, 1)
        connectcells(self.spinstel4, self.lts56, 0.01*2, 1, 0)
        connectcells(self.spinstel4, self.tuftRS5, 0.157*2, 1, 0)
        connectcells(self.spinstel4, self.tuftIB5, 0.157*2, 1, 0)
        # connectcells(self.spinstel4, self.bask56, 0.157, 1, 0)
        # connectcells(self.spinstel4, self.lts56, 0.157, 1, 0)

        connectcells(self.tuftRS5, self.tuftRS5, 2.25/4, 1, 1)
        connectcells(self.tuftRS5, self.axax56, 0.027/4, 1, 1)
        connectcells(self.tuftRS5, self.bask56, 0.127/4, 1, 1)
        connectcells(self.tuftRS5, self.nontuftRS6, 0.976/5, 1, 1)
        connectcells(self.tuftRS5, self.spinstel4, 0.108, 1, 1)
        connectcells(self.tuftRS5, self.syppyrRS, 0.36, 1, 1)
        connectcells(self.tuftRS5, self.syppyrFRB, 0.36, 1, 1)
        connectcells(self.tuftRS5, self.bask23, 0.0128, 1, 1)
        connectcells(self.tuftRS5, self.axax23, 0.004*5, 1, 1)
        connectcells(self.tuftRS5, self.LTS23, 0.019, 1, 1)
        connectcells(self.tuftRS5, self.lts56, 0.2787, 1, 1)
        connectcells(self.tuftRS5, self.tuftIB5, 1.916/4, 1, 1)

        connectcells(self.tuftIB5, self.LTS23, 0.013, 1, 1)
        connectcells(self.tuftIB5, self.LTS23, 0.0043, 1, 0)
        connectcells(self.tuftIB5, self.lts56, 0.279, 1, 1)
        connectcells(self.tuftIB5, self.lts56, 0.093, 1, 0)
        connectcells(self.tuftIB5, self.axax56, 0.027, 1, 1)
        connectcells(self.tuftIB5, self.axax56, 0.009, 1, 0)
        connectcells(self.tuftIB5, self.bask56, 0.127, 1, 1)
        connectcells(self.tuftIB5, self.tuftRS5, 1.916, 1, 1)
        connectcells(self.tuftIB5, self.tuftRS5, 0.6387, 1, 0)
        connectcells(self.tuftIB5, self.axax23, 0.004*4, 1, 1)
        connectcells(self.tuftIB5, self.axax23, 0.0013*4, 1, 0)
        connectcells(self.tuftIB5, self.syppyrRS, 0.36, 1, 1)
        connectcells(self.tuftIB5, self.syppyrRS, 0.12, 1, 0)
        connectcells(self.tuftIB5, self.syppyrFRB, 0.36, 1, 1)
        connectcells(self.tuftIB5, self.syppyrFRB, 0.12, 1, 0)
        connectcells(self.tuftIB5, self.nontuftRS6, 0.9763/5, 1, 1)
        connectcells(self.tuftIB5, self.nontuftRS6, 0.325/5, 1, 0)
        connectcells(self.tuftIB5, self.spinstel4, 0.108, 1, 1)
        connectcells(self.tuftIB5, self.spinstel4, 0.036, 1, 0)
        connectcells(self.tuftIB5, self.bask23, 0.0128, 1, 1)
        connectcells(self.tuftIB5, self.tuftIB5, 1.916/6, 1, 1)

        connectcells(self.nontuftRS6, self.nontuftRS6, 0.68/5, 1, 1)
        connectcells(self.nontuftRS6, self.nontuftRS6, 0.23/5, 1, 0)
        connectcells(self.nontuftRS6, self.bask23, 0.004, 1, 1)
        connectcells(self.nontuftRS6, self.bask23, 0.0013, 1, 0)
        connectcells(self.nontuftRS6, self.spinstel4, 0.044, 1, 1)
        connectcells(self.nontuftRS6, self.spinstel4, 0.0147, 1, 0)
        connectcells(self.nontuftRS6, self.syppyrFRB, 0.093, 1, 1)
        connectcells(self.nontuftRS6, self.syppyrFRB, 0.031, 1, 0)
        connectcells(self.nontuftRS6, self.syppyrRS, 0.093, 1, 1)
        connectcells(self.nontuftRS6, self.syppyrRS, 0.031, 1, 0)
        connectcells(self.nontuftRS6, self.bask56, 0.072/2, 1, 1)
        connectcells(self.nontuftRS6, self.bask56, 0.024/2, 1, 0)
        connectcells(self.nontuftRS6, self.axax56, 0.014/2, 1, 1)
        connectcells(self.nontuftRS6, self.lts56, 0.16/2, 1, 1)
        connectcells(self.nontuftRS6, self.lts56, 0.053/2, 1, 0)
        connectcells(self.nontuftRS6, self.tuftRS5, 0.85/5, 1, 1)
        connectcells(self.nontuftRS6, self.tuftIB5, 0.85/5, 1, 1)
        connectcells(self.nontuftRS6, self.tuftIB5, 0.283/5, 1, 0)
        connectcells(self.nontuftRS6, self.axax23, 0.00096, 1, 1)
        connectcells(self.nontuftRS6, self.nrt, 0.5/4, 1, 1)
        connectcells(self.nontuftRS6, self.tcr, 0.5, 1, 1)
        connectcells(self.nontuftRS6, self.nrt, 0.17/4, 1, 0)
        connectcells(self.nontuftRS6, self.tcr, 0.17, 1, 0)

        '''
            Connections GABA
        '''

        connectcells(self.bask23, self.syppyrFRB, 9.37, 1, -1)

        connectcells(self.axax23, self.tuftIB5, 0.082, 1, -1)

        connectcells(self.LTS23, self.bask23, 0.446, 1, -1)
        # connectcells(self.LTS23, self.bask23, 0.446*3, 1, -1)
        connectcells(self.LTS23, self.syppyrFRB, 0.74, 1, -1)
        connectcells(self.LTS23, self.LTS23, 0.301, 1, -1)
        # connectcells(self.LTS23, self.LTS23, 0.301*3, 1, -1)

        connectcells(self.axax56, self.tuftIB5, 0.108, 1, -1)
        connectcells(self.axax56, self.nontuftRS6, 0.014 * 10, 1, -1)

        connectcells(self.lts56, self.axax56, 0.0102*5, 1, -1)
        connectcells(self.lts56, self.lts56, 0.103*5, 1, -1)
        connectcells(self.lts56, self.tuftIB5, 3.761 * 5, 1, -1)

        connectcells(self.bask56, self.nontuftRS6, 0.395 * 5, 1, -1)
        connectcells(self.bask56, self.tuftIB5, 1.324 * 5, 1, -1)

        connectcells(self.bask56, self.bask56, 0.0765*5, 1, -1)

        '''
        Connections GABA NEW
        '''
        connectcells(self.bask23, self.LTS23, 0.149*3, 1, -1)
        # connectcells(self.bask23, self.LTS23, 0.149*3, 1, -1)
        connectcells(self.axax23, self.syppyrFRB, 0.271*3, 1, -1)

        connectcells(self.LTS23, self.axax23, 0.03*3, 1, -1)

        connectcells(self.bask23, self.spinstel4, 0.1352, 1, -1)
        connectcells(self.axax23, self.spinstel4, 0.0161, 1, -1)
        connectcells(self.LTS23, self.spinstel4, 0.105, 1, -1)

        connectcells(self.axax23, self.nontuftRS6, 0.018 * 10, 1, -1)

        connectcells(self.LTS23, self.nontuftRS6, 0.13 * 5, 1, -1)

        connectcells(self.LTS23, self.tuftIB5, 1.66 * 5, 1, -1)
        connectcells(self.LTS23, self.tuftRS5, 1.66 * 5, 1, -1)

        connectcells(self.LTS23, self.axax56, 0.0014*5, 1, -1)
        connectcells(self.LTS23, self.lts56, 0.0047*5, 1, -1)

        connectcells(self.bask56, self.axax56, 0.0057*5, 1, -1)

        connectcells(self.lts56, self.nontuftRS6, 0.612 * 10, 1, -1)

        connectcells(self.lts56, self.bask56, 0.028*5, 1, -1)
        connectcells(self.bask56, self.lts56, 0.082*5, 1, -1)
        connectcells(self.bask56, self.spinstel4, 0.144*5, 1, -1)
        connectcells(self.lts56, self.spinstel4, 0.27, 1, -1)
        connectcells(self.bask56, self.tuftRS5, 1.589 * 5, 1, -1)
        connectcells(self.lts56, self.tuftRS5, 1.877 * 5, 1, -1)
        connectcells(self.axax56, self.tuftRS5, 0.056 * 5, 1, -1)

        connectcells(self.lts56, self.syppyrRS, 4.1, 1, -1)
        connectcells(self.lts56, self.LTS23, 0.163*3, 1, -1)
        # connectcells(self.lts56, self.LTS23, 0.163*3, 1, -1)

        connectcells(self.lts56, self.axax23, 0.0105*3, 1, -1)
        # connectcells(self.lts56, self.axax23, 0.0105*3, 1, -1)
        connectcells(self.lts56, self.bask23, 0.0496*3, 1, -1)
        # connectcells(self.lts56, self.bask23, 0.0496*3, 1, -1)
        connectcells(self.axax56, self.syppyrRS, 0.018, 1, -1)

        connectcells(self.bask23, self.bask23, 0.093, 1, -1)
        # connectcells(self.bask23, self.bask23, 0.093, 1, -1)
        connectcells(self.bask23, self.syppyrRS, 5.519, 1, -1)

        connectcells(self.axax23, self.syppyrRS, 0.271, 1, -1)
        connectcells(self.axax23, self.tuftRS5, 0.0806 * 5, 1, -1)

        connectcells(self.LTS23, self.syppyrRS, 7.425, 1, -1)
        connectcells(self.LTS23, self.bask56, 0.0021*5, 1, -1)

        connectcells(self.axax56, self.syppyrFRB, 0.0183, 1, -1)

        connectcells(self.lts56, self.syppyrFRB, 4.0983, 1, -1)
        #
        # connectcells(self.bask23, self.tuftIB5, 1.27486*25, 1, -1)
        # connectcells(self.bask23, self.tuftRS5, 1.27486*25, 1, -1)
        # connectcells(self.bask23, self.nontuftRS6, 0.1618*, 1, -1)

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
            'y': cell.y,
            'z': cell.z
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

        for i in range(rank, nhost + 1, nhost):
            stim = h.NetStim()
            stim.number = nums
            if r:
                stim.start = random.uniform(start - 3, start + 3)
                stim.noise = 0.05
            else:
                stim.start = start
            stim.interval = int(1000 / freq)
            # skinstim.noise = 0.1
            self.neurons.append(stim)
            while pc.gid_exists(gid) != 0:
                gid += 1
            pc.set_gid2node(gid, rank)
            ncstim = h.NetCon(stim, None)
            pc.cell(gid, ncstim)

            gids.append(gid)

        return gids


def connectcells(pre, post, weight, delay, type, N=50):
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
    nsyn = random.randint(N - 15, N)
    num_syn[0] += nsyn

    for i in post:
        if pc.gid_exists(i):
            for j in range(nsyn):
                srcgid = random.randint(pre[0], pre[-1])
                target = pc.gid2cell(i)
                if (type == 1):
                    syn = target.AMPA_syns[j]
                    nc = pc.gid_connect(srcgid, syn)
                    AMPA_nclist.append(nc)
                elif (type == -1):
                    syn = target.GABA_syns[j]
                    nc = pc.gid_connect(srcgid, syn)
                    GABA_nclist.append(nc)
                elif (type == 0):
                    syn = target.NMDA_syns[j]
                    nc = pc.gid_connect(srcgid, syn)
                    NMDA_nclist.append(nc)
                    # nc.weight[0] = random.gauss(weight, weight / 6) # str

                w = random.gauss(weight, weight / 5) * 2
                nc.weight[0] = w
                # nc.weight[0] = random.gauss(weight, weight / 6) * 2
                nc.delay = random.gauss(delay, 1 / 4) + 1  # idk but should be more than 1 for parallel
                # nc.delay = random.gauss(delay, 1 / 5) + 1  # idk but should be more than 1 for parallel
                from_cell = pc.gid2cell(pre[0]).__str__().split(' ')[0].split('.')[-1]
                to_cell = target.__str__().split(' ')[0].split('.')[-1]
                key = str(type) + ' - ' + from_cell + ' - ' + to_cell
                if key in conn_dict:
                    conn_dict[key][0] += 1
                    conn_dict[key][1] += w
                else:
                    conn_dict[key] = list()
                    conn_dict[key].append(1)
                    conn_dict[key].append(w)



def prun():
    ''' simulation control
    Parameters
    ----------
    speed: int
      duration of each layer
    Returns
    -------
    t: list of h.Vector()
      recorded time
    '''
    pc.timeout(0)
    t = h.Vector().record(h._ref_t)
    tstop = time_sim  # 25 + (6 * speed + 125) * step_number
    # pc.set_maxstep(100 * ms)
    # h.finitialize(-70 * mV)
    # pc.psolve(tstop * ms)
    pc.set_maxstep(10)
    h.finitialize(-70 * mV)
    pc.psolve(tstop)
    return t


def spike_recording(pool, extra=False):  # new
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


def time_recording(pool, extra=False):  # new
    '''Record spikes from gids
    Parameters
    ----------
    pool: list
      list of neurons gids
    Returns
    -------
    t_vec: list of h.Vector()
        recorded time
    '''
    t_vec = []
    for i in pool:
        cell = pc.gid2cell(i)
        t_vec.append(cell.t_vec)
    return t_vec


def spikeout(pool, id, name, v_vec):
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
        with hdf5.File('./results/voltage_{}_{}.hdf5'.format(id, name), 'w') as file:
            file.create_dataset('#0_step', data=np.array(result), compression="gzip")
    else:
        logging.info(rank)


def timeout(pool, id, name, t_vec):
    ''' Reports simulation results
      Parameters
      ----------
      pool: list
        list of neurons gids
      name: string
        pool name
      version: int
          test number
      t_vec: list of h.Vector()
          recorded time
    '''
    global rank
    pc.barrier()
    vec = h.Vector()
    for i in range(nhost):
        if i == rank:
            outavg = []
            for j in range(len(pool)):
                outavg.append(list(t_vec[j]))
            outavg = np.mean(np.array(outavg), axis=0, dtype=np.float32)
            vec = vec.from_python(outavg)
        pc.barrier()
    pc.barrier()
    result = pc.py_gather(vec, 0)
    if rank == 0:
        logging.info("start recording")
        result = np.mean(np.array(result), axis=0, dtype=np.float32)
        time_name = 'time'
        if value == 100:
            time_name = 'time_e'
        with hdf5.File('./results/{}_{}_{}.hdf5'.format(time_name, id, name), 'w') as file:
            file.create_dataset('#0_step', data=np.array(result), compression="gzip")
    else:
        logging.info(rank)


def datacel(data_cells):
    ''' Reports simulation results
      Parameters
      ----------
      data_cells: list
        list of data cells
    '''
    global rank
    pc.barrier()
    separator = len(data_cells) // nhost
    for i in range(nhost):
        if i == rank:
            start = i * separator
            end = i * separator + separator
            if i == nhost - 1:
                end = len(data_cells)
            for j in range(start, end):
                with open('./results_csv/cells_{}.csv'.format(i), 'a') as file:
                    writer = csv.writer(file, delimiter='\t')
                    writer.writerow([data_cells[j][key] for key in data_cells[j].keys()])
            if rank == 0:
                with open('./results_csv/cells.csv', 'a') as file:
                    writer = csv.writer(file, delimiter='\t')
                    writer.writerow(list(data_cells[0].keys()))
        pc.barrier()
    pc.barrier()
    if rank == 0:
        logging.info("start recording")
        for i in range(nhost):
            with open('./results_csv/cells_{}.csv'.format(i), 'r') as file:
                csv_file = csv.reader(file, delimiter='\t')
                with open('./results_csv/cells.csv', 'a') as f_cells:
                    writer = csv.writer(f_cells, delimiter='\t')
                    writer.writerow(list(csv_file))
            os.remove('./results_csv/cells_{}.csv'.format(i))


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
    result = pc.py_gather(vec, 0)
    if rank == 0:
        logging.info("start recording")
        flat_result = [item for sublist in result for item in sublist]
        s_id = str(id)
        if value == 100:
            s_id += 'e'
        with open('./results/spiketime_{}_{}.txt'.format(s_id, name), 'w') as spk_file:
                for time in flat_result:
                    spk_file.write(str(time) + "\n")
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
    if rank == 0:
        if os.path.exists('./results_csv/connections.csv'):
            os.remove('./results_csv/connections.csv')
        # if os.path.exists('./results/cells.csv'):
        #     os.remove('./results/cells.csv')
        with open('./results_csv/connections.csv', 'a') as ofile:
            writer = csv.writer(ofile, delimiter='\t')
            writer.writerow(['type', 'source', 'target', 'count', 'weight', 'count/weight'])

    CC_c = CC_circuit()
    logging.info("created")
    recorders = []
    # time_recorders = []
    spike_rec = []

    for group in CC_c.groups:
        recorders.append(spike_recording(group[k_nrns]))
        # time_recorders.append(time_recording(group[k_nrns]))
        spike_rec.append(spike_time_rec(group[k_nrns]))

    logging.info("added recorders")

    print("- " * 10, "\nstart")
    t = prun()

    with open('./results/time.txt', 'w') as time_file:
        for time in t:
            time_file.write(str(time) + "\n")
    print("- " * 10, "\nend")

    for group, layer, recorder in zip(CC_c.groups, CC_c.layers, recorders):
        spikeout(group[k_nrns], layer[k_name], group[k_name], recorder)

    # for group, layer, recorder in zip(CC_c.groups, CC_c.layers, time_recorders):
    #     timeout(group[k_nrns], layer[k_name], group[k_name], recorder)

    for group, layer, recorder in zip(CC_c.groups, CC_c.layers, spike_rec):
        spiketimeout(group[k_nrns], layer[k_name], group[k_name], recorder)


    # datacel(CC_c.data['cells'])

    if rank == 0:
        with open('./results_csv/connections.csv', 'a') as file:
            writer = csv.writer(file, delimiter='\t')
            for key, value in conn_dict.items():
                splited = key.split(' - ')
                writer.writerow([splited[0], splited[1], splited[2], value[0], value[1], value[1]/value[0]])

        with open('./results/AGN.txt', 'w') as n_file:
            logging.info("in file AGN")
            syn = num_syn[0]
            a = len(AMPA_nclist)
            g = len(GABA_nclist)
            n = len(NMDA_nclist)
            c = {'AMPA ': a, ' GABA ': g, ' NMDA ': n, ' Count synapses ': syn}
            n_file.write(c.__str__())
            logging.info("created AGN")

    logging.info("done")

    finish()
