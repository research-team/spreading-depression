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
import json

h.nrnmpi_init()
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
root = 0


#time =300
rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37

numpy.random.seed(6324555 + pcid)
outdir = os.path.abspath('tests/721_tW')


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
NsyppyrFRB = 50
NsyppyrRS = 1000
#0-400

data={}
data['cells']=[]
rec_neurons12=[]
for i in range(0,NsyppyrFRB):
    rec_neurons12.append(SyppyrFRB(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(somaR,400),
    i+num))
    data['cells'].append({
        'name': rec_neurons12[i].name,
        'id': rec_neurons12[i].id,
        'num': rec_neurons12[i].number,
        'x': rec_neurons12[i].x,
        'y' : rec_neurons12[i].y,
        'z' : rec_neurons12[i].z
    })

num+=50

rec_neurons13 = []
for i in range(0,NsyppyrRS):
    rec_neurons13.append(SyppyrRS(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(somaR,400),
    i+num))
    data['cells'].append({
        'name': rec_neurons13[i].name,
        'id': rec_neurons13[i].id,
        'num': rec_neurons13[i].number,
        'x': rec_neurons13[i].x,
        'y': rec_neurons13[i].y,
        'z': rec_neurons13[i].z
    })


num+=1000

rec_neurons1 = []
for i in range(0,NLTS23):
    rec_neurons1.append(LTS23(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(somaR,400),
    i+num))
    data['cells'].append({
        'name': rec_neurons1[i].name,
        'id': rec_neurons1[i].id,
        'num': rec_neurons1[i].number,
        'x': rec_neurons1[i].x,
        'y': rec_neurons1[i].y,
        'z': rec_neurons1[i].z
    })


num+=NLTS23
rec_neurons2=[]
for i in range(0,Nbask23):
    rec_neurons2.append(Bask23(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(somaR,400),
    i+num))
    data['cells'].append({
        'name': rec_neurons2[i].name,
        'id': rec_neurons2[i].id,
        'num': rec_neurons2[i].number,
        'x': rec_neurons2[i].x,
        'y': rec_neurons2[i].y,
        'z': rec_neurons2[i].z
    })

num+=Nbask23
rec_neurons3=[]
for i in range(0,Naxax23):
    rec_neurons3.append(Axax23(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(somaR,400),
    i+num))
    data['cells'].append({
        'name': rec_neurons3[i].name,
        'id': rec_neurons3[i].id,
        'num': rec_neurons3[i].number,
        'x': rec_neurons3[i].x,
        'y': rec_neurons3[i].y,
        'z': rec_neurons3[i].z
    })


num+=Naxax23
#400-700
rec_neurons4=[]
for i in range(0,Nspinstel4):
    rec_neurons4.append(Spinstel4(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(400,700), i+num))
    data['cells'].append({
        'name': rec_neurons4[i].name,
        'id': rec_neurons4[i].id,
        'num': rec_neurons4[i].number,
        'x': rec_neurons4[i].x,
        'y': rec_neurons4[i].y,
        'z': rec_neurons4[i].z
    })



num+=Nspinstel4
rec_neurons5=[]
for i in range(0,NtuftIB5):
    rec_neurons5.append(TuftIB5(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(400,700), i+num))
    data['cells'].append({
        'name': rec_neurons5[i].name,
        'id': rec_neurons5[i].id,
        'num': rec_neurons5[i].number,
        'x': rec_neurons5[i].x,
        'y': rec_neurons5[i].y,
        'z': rec_neurons5[i].z
    })



num+=NtuftIB5
'''
rec_neurons11 = [Bask4(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(400,700), i)
    for i in range(num, num+Bask_4)]

num+=Bask_4
'''
#700-1200
rec_neurons6=[]
for i in range(0,NtuftRS5):
    rec_neurons6.append(TuftRS5(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,1200), i+num))
    data['cells'].append({
        'name': rec_neurons6[i].name,
        'id': rec_neurons6[i].id,
        'num': rec_neurons6[i].number,
        'x': rec_neurons6[i].x,
        'y': rec_neurons6[i].y,
        'z': rec_neurons6[i].z
    })


num+=NtuftRS5
rec_neurons7=[]
for i in range(0,Nbask56):
    rec_neurons7.append(Bask56(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,1200), i+num))
    data['cells'].append({
        'name': rec_neurons7[i].name,
        'id': rec_neurons7[i].id,
        'num': rec_neurons7[i].number,
        'x': rec_neurons7[i].x,
        'y': rec_neurons7[i].y,
        'z': rec_neurons7[i].z
    })


num+=Nbask56

#700-1700
rec_neurons8=[]
for i in range(0,Naxax56):
    rec_neurons8.append(Axax56(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,1700), i+num))
    data['cells'].append({
        'name': rec_neurons8[i].name,
        'id': rec_neurons8[i].id,
        'num': rec_neurons8[i].number,
        'x': rec_neurons8[i].x,
        'y': rec_neurons8[i].y,
        'z': rec_neurons8[i].z
    })


num+=Naxax56
rec_neurons9=[]
for i in range(0,NLTS56):
    rec_neurons9.append(LTS56(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,1700), i+num))
    data['cells'].append({
        'name': rec_neurons9[i].name,
        'id': rec_neurons9[i].id,
        'num': rec_neurons9[i].number,
        'x': rec_neurons9[i].x,
        'y': rec_neurons9[i].y,
        'z': rec_neurons9[i].z
    })


num+=NLTS56
rec_neurons10=[]
for i in range(0,NnontuftRS6):
    rec_neurons10.append(NontuftRS6(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(1200,1700-somaR), i+num))
    data['cells'].append({
        'name': rec_neurons10[i].name,
        'id': rec_neurons10[i].id,
        'num': rec_neurons10[i].number,
        'x': rec_neurons10[i].x,
        'y': rec_neurons10[i].y,
        'z': rec_neurons10[i].z
    })


num += NnontuftRS6

#2710
cell=[rec_neurons12, rec_neurons13, rec_neurons1, rec_neurons2, rec_neurons3, rec_neurons4, rec_neurons5, rec_neurons6, rec_neurons7, rec_neurons8, rec_neurons9, rec_neurons10]
#------for test----------
#i4 = random.randint(0, Nspinstel4)
#i5=random.randint(0, NtuftIB5)
#i6 = random.randint(0, NtuftRS5)



'''
stim4 = h.IClamp(rec_neurons4[random.randint(0, Nspinstel4)].soma(0.5))
stim4.delay = 10
stim4.dur = 1
stim4.amp = 1

stim = h.NetStim(rec_neurons4[random.randint(0, Nspinstel4)].soma(0.5))
stim.number = 5
stim.start = 10
'''


'''
stim5 = h.IClamp(rec_neurons5[random.randint(0, NtuftIB5)].soma(0.5))
stim5.delay = 10
stim5.dur = 1
stim5.amp = 1

stim6 = h.IClamp(rec_neurons6[random.randint(0, NtuftRS5)].soma(0.5))
stim6.delay = 10
stim6.dur = 1
stim6.amp = 1
'''


data['pyramidal regular spiking']=[] #13
for i in rec_neurons13:
    n=rec_neurons13[random.randint(0, NsyppyrRS - 1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source' : i.number,
        'target' : n.number,
        'id' : 1
    })

    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons1[random.randint(0,NLTS23-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,1)
    data['pyramidal regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    count_syn+=11
    #count_cells+=1
data['pyramidal fast rythmic bursting']=[]
for i in rec_neurons12:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons1[random.randint(0,NLTS23-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,1)
    data['pyramidal fast rythmic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    count_syn+=11
    #count_cells+=1
data['spiny stellate']=[]

for i in rec_neurons4:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons1[random.randint(0,NLTS23-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,1)
    data['spiny stellate'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    count_syn+=9
    #count_cells+=1
data['superficial interneurons axoaxonic']=[]
for i in rec_neurons2:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,-1)
    data['superficial interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,-1)
    data['superficial interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,-1)
    data['superficial interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,-1)
    data['superficial interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons1[random.randint(0,NLTS23-1)]
    i.connect(n,-1)
    data['superficial interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n,-1)
    data['superficial interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    count_syn+=6

data['superficial interneurons low threshold spiking']=[]
for i in rec_neurons3:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,-1)
    data['superficial interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,-1)
    data['superficial interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,-1)
    data['superficial interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n,-1)
    data['superficial interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,-1)
    data['superficial interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,-1)
    data['superficial interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,-1)
    data['superficial interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    count_syn+=7
data['superficial interneurons basket']=[]
for i in rec_neurons1:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons1[random.randint(0,NLTS23-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,-1)
    data['superficial interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    count_syn+=12

data['pyramidal tufted intrinsic bursting']=[]
for i in rec_neurons5:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons1[random.randint(0,NLTS23-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,1)
    data['pyramidal tufted intrinsic bursting'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    count_syn+=12
    #count_cells+=1
data['deep interneurons basket']=[]
for i in rec_neurons7:
    n=rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,-1)
    data['deep interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n, -1)
    data['deep interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,-1)
    data['deep interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,-1)
    data['deep interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,-1)
    data['deep interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,-1)
    data['deep interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,-1)
    data['deep interneurons basket'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    count_syn+=7
data['pyramidal tufted regular spiking']=[]
for i in rec_neurons6:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons1[random.randint(0,NLTS23-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n = rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n =rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,1)
    data['pyramidal tufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })
    count_syn+=12
    #count_cells+=1

data['pyramidal nontufted regular spiking']=[]
for i in rec_neurons10:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,1)
    data['pyramidal nontufted regular spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': 1
    })

    count_syn+=11
    #count_cells+=1
data['deep interneurons axoaxonic']=[]
for i in rec_neurons8:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,-1)
    data['deep interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,-1)
    data['deep interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,-1)
    data['deep interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,-1)
    data['deep interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })

    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,-1)
    data['deep interneurons axoaxonic'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    count_syn+=5
data['deep interneurons low threshold spiking']=[]
for i in rec_neurons9:
    n=rec_neurons13[random.randint(0,NsyppyrRS-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons12[random.randint(0,NsyppyrFRB-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons2[random.randint(0,Nbask23-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons3[random.randint(0,Naxax23-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons1[random.randint(0,NLTS23-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons4[random.randint(0,Nspinstel4-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons5[random.randint(0,NtuftIB5-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons6[random.randint(0,NtuftRS5-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons10[random.randint(0,NnontuftRS6-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons8[random.randint(0,Naxax56-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons9[random.randint(0,NLTS56-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    n=rec_neurons7[random.randint(0,Nbask56-1)]
    i.connect(n,-1)
    data['deep interneurons low threshold spiking'].append({
        'source': i.number,
        'target': n.number,
        'id': -1
    })
    count_syn+=12

'''
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
'''



with open(os.path.join(outdir,'data.json'), 'w') as outfile:
    json.dump(data, outfile)

alpha = alpha1
tort = tort1


time = h.Vector().record(h._ref_t)
'''
ecs = rxd.Extracellular(-Lx / 2.0, -Ly / 2.0,
                        -Lz / 2.0, Lx / 2.0, Ly / 2.0, Lz / 2.0, dx=(20, 20, 20),  # dx - скорость распространнения в разные стороны - различны по осям
                        volume_fraction=alpha, tortuosity=tort)


k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial= 3.5,
                ecs_boundary_conditions=3.5)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=142,
                 ecs_boundary_conditions=142)

'''

stim = h.NetStim()
stim.number = 5
stim.start = 10
ncstim = h.NetCon(stim, rec_neurons4[random.randint(0, Nspinstel4)].synlistex[0])
ncstim.delay = 1
ncstim.weight[0] = 0.5

#kecs = h.Vector()
#kecs.record(k[ecs].node_by_location(0, 0, 0)._ref_value)
pc.set_maxstep(100)

# initialize and set the intracellular concentrations
h.finitialize()
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

def plot_volt(data):
    fig = px.scatter(data, x='x', y='y', z='z', animation_frame="v", animation_group="v",
                      color="v")

    fig["layout"].pop("updatemenus")
    fig.write_html(os.path.join(outdir, 'volt.html'))

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
                for i in range(num):
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
    pyplot.imshow(data, extent=k[ecs].extent('xz'), vmin=min_val,
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
    pyplot.ylim(k[ecs].extent('z'))
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
    volt = []
    
    while pc.t(0) <= tstop:

        for j in cell:
            for n in j:
                volt.append({"t" : int(pc.t(0)),
                                "x" : n.x,
                                "y" : n.y,
                                "z" : n.z,
                                "v" : n.somaV[-1],
                                "id": n.id,
                                "num": n.number})


        #if int(pc.t(0)) % 100 == 0:
         #   if pcid == 0:
                #plot_image_data(k[ecs].states3d.mean(2), 3.5, 40,
                             #   'k_mean_%05d' % int(pc.t(0) / 100),
                             #   'Potassium concentration; t = %6.0fms'
                             #   % pc.t(0))

            
        if pcid == 0: progress_bar(tstop)
        pc.psolve(pc.t(0) + h.dt)
        
    if pcid == 0:
        #progress_bar(tstop)
       # for i in [0, 108] :
            #plot_spike(rec_neurons[i], time , i)
        print("\nSimulation complete. Plotting membrane potentials")
        #plot_K_ecs_in_point_000(kecs ,range(0,tstop))

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
            #plot_spike_html(n, time, n.number)


    #pout = open(os.path.join(outdir, "membrane_potential_%i.pkl" % pcid), 'wb')
    #pickle.dump([soma, dend, pos, data], pout)
    #pout.close()
    d3_data = pd.DataFrame(dict(x=x_pos, y=y_pos, z=z_pos, id=id_color, name=listname))
    pc.barrier()
    if pcid == 0:

        #plot_3D_data(d3_data)
        voltToCSV = pd.DataFrame(volt)
        voltToCSV.to_csv(os.path.join(outdir, 'volt.csv'))
        #plot_volt(volt)
        #plot_rec_neurons()
    exit(0)


run(200)