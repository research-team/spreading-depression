import logging
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
from cells import *
import json
import neuron.rxd as rxd
from neuron.units import ms, mV

pc = h.ParallelContext()
rank = int(pc.id())
nhost = int(pc.nhost())

AMPA_nclist = []
GABA_nclist = []
NMDA_nclist = []

#time =300
rxd.options.enable.extracellular = True

# simulation parameters
time_sim = 10
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

        logging.info('created neurons, start adding conections')

        ''' CONNECTIONS '''

        connectcells(self.syppyrFRB, self.bask23, 0.23, 1, 1)

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
            nc = cell.connect2target(None)
            pc.cell(gid, nc)

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
                nc.weight[0] = random.gauss(weight, weight / 5)
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

    CC_c = CC_circuit()
    logging.info("created")

    print("- " * 10, "\nstart")
    prun()
    print("- " * 10, "\nend")

    logging.info("done")


    finish()
