import random
import os
import sys
import csv
from cells import *
import json
import logging
import neuron.rxd as rxd
#h.nrnmpi_init()
pc = h.ParallelContext()
pcid = int(pc.id())
nhost = pc.nhost()
root = 0
pc.set_maxstep(10)
import numpy as np
import plotly.graph_objects as go
import pandas as pd

logging.basicConfig(filename='logs.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
logging.info("let's get it started")

#time =300
rxd.options.enable.extracellular = True

h.load_file('stdrun.hoc')
h.celsius = 37

#numpy.random.seed(6324555 + pcid)
outdir = os.path.abspath('tests/902_tW')


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
pc.barrier()
# simulation parameters
Lx, Ly, Lz = 100, 100, 1700 
Kceil = 15.0  # threshold used to determine wave speed
Ncell = int(9e4 * (Lx * Ly * Lz * 1e-9))

#L2/3 (0-400)
Nbask23 = 90 #59
Naxax23 = 90 #59
NLTS23 = 90 #59
NsyppyrFRB = 50
NsyppyrRS = 1000
#L4 (400-700)
Nspinstel4 = 240
Nbask4=36
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

data={}
data['cells']=[]
rec_neurons12=[]
logging.info('Create neurons')

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
cell = [rec_neurons4]

#------for test----------
#i4 = random.randint(0, Nspinstel4)
#i5=random.randint(0, NtuftIB5)
#i6 = random.randint(0, NtuftRS5)
#print('start connect_cells.')
logging.info('start connect_cells')
#---------------------- 2/3 (0-400) ---------------------
#count_cells_23=Nbask23+Naxax23+NsyppyrFRB+NsyppyrRS+NLTS23
#count_links_23=0
#count_in_23=0
##count_out_23=0
#
#for i in rec_neurons13:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:50]:
#        j.connect_cells(i, 1, 0.00025)
#        j.connect_cells(i, 0, 0.0000025)
#        count_links_23=count_links_23+2*50
#    #print('cc13')
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:15]:
#        j.connect_cells(i, 1, 0.00025)
#        j.connect_cells(i, 0, 0.0000025)
#        count_links_23=count_links_23+2*15
#    random.shuffle(rec_neurons1)
#    for j in rec_neurons1[0:20]:
#        j.connect_cells(i, -1, 0.0000025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons2)
#    for j in rec_neurons2[0:20]:
#        j.connect_cells(i, -1,0.000025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons3)
#    for j in rec_neurons3[0:20]:
#        j.connect_cells(i, -1, 0.000025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:100]:
#        j.connect_cells(i, 1,0.025)
#        j.connect_cells(i, 0,0.000025)
#        count_in_23 = count_in_23 + 2*100
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:50]:
#        j.connect_cells(i, 0, 0.000025)
#        j.connect_cells(i, 1, 0.025)
#        count_in_23 = count_in_23 + 2*50
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:50]:
#        j.connect_cells(i, 1, 0.025)
#        count_in_23 = count_in_23 + 1*50
#    random.shuffle(rec_neurons8)
#    for j in rec_neurons8[0:5]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_23 = count_in_23 + 1*5
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:10]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_23 = count_in_23 + 1*10
#    #random.shuffle(rec_neurons10)
#    #for j in rec_neurons10[0:10]:
#    #    j.connect_cells(i, 1, 0.00025)
#    #    j.connect_cells(i, 0, 0.0000025)
#    #    count_in_23 = count_in_23 + 2*10
#
#
#for i in rec_neurons12:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:50]:
#        j.connect_cells(i, 1, 0.025)
#        j.connect_cells(i, 0, 0.00025)
#        count_links_23=count_links_23+2*50
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:200]:
#        j.connect_cells(i, 1, 0.025)
#        j.connect_cells(i, 0, 0.00025)
#        count_links_23=count_links_23+2*20
#    random.shuffle(rec_neurons1)
#    for j in rec_neurons1[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons2)
#    for j in rec_neurons2[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons3)
#    for j in rec_neurons3[0:20]:
#        j.connect_cells(i, -1, 0.0025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:100]:
#        j.connect_cells(i, 1, 0.025)
#        j.connect_cells(i, 0, 0.0025)
#        count_in_23 = count_in_23 + 2*100
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:100]:
#        j.connect_cells(i, 0, 0.00025)
#        j.connect_cells(i, 1, 0.025)
#        count_in_23 = count_in_23 + 2*50
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:50]:
#        j.connect_cells(i, 1, 0.25)
#        count_in_23 = count_in_23 + 1*50
#    random.shuffle(rec_neurons8)
#    for j in rec_neurons8[0:5]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_23 = count_in_23 + 1*5
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:10]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_23 = count_in_23 + 1*5
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.0025)
#        j.connect_cells(i, 0, 0.0025)
#        count_in_23 = count_in_23 + 2*10
#
#
#for i in rec_neurons1:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:90]:
#        j.connect_cells(i, 1, 0.025)
#        #j.connect_cells(i, 0)
#        count_links_23=count_links_23+1*90
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:5]:
#        j.connect_cells(i, 1, 0.025)
#        #j.connect_cells(i, 0)
#        count_links_23=count_links_23+1*5
#    random.shuffle(rec_neurons1)
#    for j in rec_neurons1[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons3)
#    for j in rec_neurons3[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:20]:
#        #j.connect_cells(i, 0)
#        j.connect_cells(i, 1, 0.00025)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:10]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_23 = count_in_23 + 1*10
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.00025)
#        count_in_23 = count_in_23 + 1*10
#
#
#
#
#
#
#for i in rec_neurons2:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:90]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_links_23=count_links_23+1*90
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:5]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_links_23=count_links_23+1*5
#    random.shuffle(rec_neurons1)
#    for j in rec_neurons1[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons3)
#    for j in rec_neurons3[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:20]:
#        #j.connect_cells(i, 0)
#        j.connect_cells(i, 1, 0.00025)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:10]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_23 = count_in_23 + 1*10
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.00025)
#        count_in_23 = count_in_23 + 1*10
#
#
#
#
#for i in rec_neurons3:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:90]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_links_23=count_links_23+ 1*90
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:5]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_links_23 = count_links_23 + 1*5
#    random.shuffle(rec_neurons1)
#    for j in rec_neurons1[0:20]:
#        j.connect_cells(i, -1, 0.0000025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons3)
#    for j in rec_neurons3[0:20]:
#        j.connect_cells(i, -1, 0.0000025)
#        count_links_23 = count_links_23 + 1*20
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:20]:
#        #j.connect_cells(i, 0)
#        j.connect_cells(i, 1, 0.00025)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        count_in_23 = count_in_23 + 1*20
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:10]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_23 = count_in_23 + 1*10
#
#
#dg={}
#dg['2-3'] = []
#dg['2-3'].append({
#    'count_cells' : [count_cells_23],
#    'count_links' : [count_links_23],
#    'count_in' : [count_in_23]
#    })
#logging.info('level 2-3')
#_________________________ 4 (400-700)______________________________
count_cells_4=Nspinstel4+Nbask4
count_links_4=0
count_in_4=0

for i in rec_neurons4:
    #random.shuffle(rec_neurons13)
    #for j in rec_neurons13[0:3]:
    #    j.connect_cells(i, 0, 0.000025)
    #    j.connect_cells(i, 1, 0.00025)
    #    count_in_4=count_in_4+2*3
    ##random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:20]:
    #    j.connect_cells(i, 1, 0.00025)
    #    count_in_4 = count_in_4 + 1*20
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:30]:
    #    j.connect_cells(i, 1, 0.025)
    #    j.connect_cells(i, 0, 0.00025)
    #    count_in_4 = count_in_4 + 2*30
    #random.shuffle(rec_neurons12)
    #for j in rec_neurons12[0:2]:
    #    j.connect_cells(i, 0, 0.0000025)
    #    j.connect_cells(i, 1, 0.00025)
    #    count_in_4 = count_in_4 + 1*2
    #random.shuffle(rec_neurons1)
    #for j in rec_neurons1[0:20]:
    #    j.connect_cells(i, -1, 0.00025)
    #    count_in_4 = count_in_4 + 1*20
    #random.shuffle(rec_neurons2)
    #for j in rec_neurons2[0:5]:
    #    j.connect_cells(i, -1, 0.00025)
    #    count_in_4 = count_in_4 + 1*5
    #random.shuffle(rec_neurons3)
    #for j in rec_neurons3[0:20]:
    #    j.connect_cells(i, -1, 0.00025)
    #    count_in_4 = count_in_4 + 1*20
    #random.shuffle(rec_neurons7)
    #for j in rec_neurons7[0:20]:
    #    j.connect_cells(i, -1, 0.00025)
    #    count_in_4 = count_in_4 + 1*20
    #random.shuffle(rec_neurons9)
    #for j in rec_neurons9[0:20]:
    #    j.connect_cells(i, -1, 0.00025)
    #    count_in_4 = count_in_4 + 1*20
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:100]:
        j.connect_cells(i, 1, 0.25)
        j.connect_cells(i, 0, 0.0025)
        count_links_4 = count_links_4 + 2*100
    #random.shuffle(rec_neurons16)
    #for j in rec_neurons16[0:10]:
    #    j.connect_cells(i, 1, 0.000025)
    #    count_in_4 = count_in_4 + 1 * 10
    #random.shuffle(rec_neurons5)
    #for j in rec_neurons5[0:3]:
    #    j.connect_cells(i, 0)
    #    j.connect_cells(i, 1)
    #    count_links_4 = count_links_4 + 2



#for i in rec_neurons16:
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:3]:
#        j.connect_cells(i, -1, 0.00025)
#        #j.connect_cells(i, 1, 0.00025)
#        count_in_4=count_in_4+1*3


#dg['4'] = {
#    'count_cells' : [count_cells_4],
#    'count_links' : [count_links_4],
#    'count_in' : [count_in_4]
#    }
#logging.info('level 4')
##_____________________5 (700-1200)___________________________________
#count_cells_5=NtuftRS5 + Nbask56+NtuftIB5
#count_links_5=0
#count_in_5=0
#
#for i in rec_neurons5:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:500]:
#        j.connect_cells(i, 1, 0.25)
#        j.connect_cells(i, 0, 0.00025)
#        count_in_5=count_in_5+2*60
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6:
#        j.connect_cells(i, 1, 0.25)
#        count_links_5 = count_links_5 + 1*200
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.025)
#        j.connect_cells(i, 0, 0.0000025)
#        count_in_5 = count_in_5 + 2*10
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:30]:
#        j.connect_cells(i, 1, 0.25)
#        j.connect_cells(i, 0, 0.00025)
#        count_in_5 = count_in_5 + 2*3
#    random.shuffle(rec_neurons2)
#    for j in rec_neurons2[0:5]:
#        j.connect_cells(i, -1, 0.0000025)
#        count_in_5 = count_in_5 + 1*5
#    random.shuffle(rec_neurons3)
#    for j in rec_neurons3[0:20]:
#        j.connect_cells(i, -1, 0.000025)
#        count_in_5 = count_in_5 + 1*20
#    random.shuffle(rec_neurons7)
#    for j in rec_neurons7[0:20]:
#        j.connect_cells(i, -1, 0.025)
#        count_links_5 = count_links_5 + 1*20
#    random.shuffle(rec_neurons8)
#    for j in rec_neurons8[0:20]:
#        j.connect_cells(i, -1, 0.025)
#        count_in_5 = count_in_5 + 1*20
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:20]:
#        j.connect_cells(i, -1, 0.025)
#        count_in_5 = count_in_5 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5:
#        j.connect_cells(i, 0, 0.0000025)
#        j.connect_cells(i, 1, 0.025)
#        count_links_5 = count_links_5 + 2*50
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:20]:
#        j.connect_cells(i, 1, 0.0025)
#        count_in_5 = count_in_5 + 1*20
#
#
#for i in rec_neurons6:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:300]:
#        j.connect_cells(i, 1, 0.025)
#        j.connect_cells(i, 0, 0.00025)
#        count_in_5=count_in_5+2*300
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:10]:
#        j.connect_cells(i, 1, 0.025)
#        count_links_5 = count_links_5 + 1*10
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.025)
#        j.connect_cells(i, 0, 0.00025)
#        count_in_5 = count_in_5 + 2*10
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:30]:
#        j.connect_cells(i, 1, 0.025)
#        j.connect_cells(i, 0, 0.00025)
#        count_in_5 = count_in_5 + 2*30
#    random.shuffle(rec_neurons7)
#    for j in rec_neurons7[0:20]:
#        j.connect_cells(i, -1, 0.25)
#        count_links_5 = count_links_5 + 1*20
#    random.shuffle(rec_neurons8)
#    for j in rec_neurons8[0:5]:
#        j.connect_cells(i, -1, 0.0025)
#        count_links_5 = count_links_5 + 1*5
#    random.shuffle(rec_neurons3)
#    for j in rec_neurons3[0:20]:
#        j.connect_cells(i, -1, 0.000025)
#        count_in_5 = count_in_5 + 1*20
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:20]:
#        j.connect_cells(i, -1, 0.0025)
#        count_in_5 = count_in_5 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:20]:
#        j.connect_cells(i, 0, 0.00025)
#        j.connect_cells(i, 1, 0.025)
#        count_in_5 = count_in_5 + 2*20
#
#
#
#
#
#for i in rec_neurons7:
#    random.shuffle(rec_neurons7)
#    for j in rec_neurons7[0:30]:
#        j.connect_cells(i, -1, 0.00025)
#    #    #j.connect_cells(i, 0)
#        count_in_5=count_in_5+1*30
#        random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        count_links_5 = count_links_5 + 1*20
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_in_5 = count_in_5 + 1*10
#    #random.shuffle(rec_neurons12)
#    #for j in rec_neurons12[0:3]:
#    #    j.connect_cells(i, -1, 0.0000025)
#    #    #j.connect_cells(i, 0)
#    #    count_in_5 = count_in_5 + 1*3
#    #random.shuffle(rec_neurons3)
#    #for j in rec_neurons3[0:20]:
#    #    j.connect_cells(i, -1, 0.0000025)
#    #    count_in_5 = count_in_5 + 1*20
#    random.shuffle(rec_neurons7)
#    for j in rec_neurons7[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_links_5 = count_links_5 + 1*20
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_5 = count_in_5 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:20]:
#        #j.connect_cells(i, 0)
#        j.connect_cells(i, 1, 0.00025)
#        count_in_5 = count_in_5 + 1*20
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_in_5 = count_in_5 + 1*20
#
#dg['5 (700-1200)'] = {
#    'count_cells' : [count_cells_5],
#    'count_links' : [count_links_5],
#    'count_in' : [count_in_5]
#    }
#logging.info('level 5')
##______________________5-6 (700-1700)__________________________________
#count_cells_56=Naxax56+NLTS56
#count_links_56=0
#count_in_56=0
#
#
#for i in rec_neurons8:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:30]:
#        j.connect_cells(i, -1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_in_56=count_in_56+1*30
#    #random.shuffle(rec_neurons7)
#    #for j in rec_neurons7[0:20]:
#    #    j.connect_cells(i, -1, 0.0000025)
#    #    count_in_56 = count_in_56 + 1*20
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.0025)
#        #j.connect_cells(i, 0)
#        count_in_56 = count_in_56 + 1*10
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:3]:
#        j.connect_cells(i, 1, 0.0025)
#        #j.connect_cells(i, 0)
#        count_in_56 = count_in_56 + 1*3
#    #random.shuffle(rec_neurons4)
#    #for j in rec_neurons4[0:20]:
#    #    j.connect_cells(i, -1, 0.0000025)
#    #    #j.connect_cells(i, 0)
#    #    count_in_56 = count_in_56 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:20]:
#        #j.connect_cells(i, 0)
#        j.connect_cells(i, 1, 0.0025)
#        count_in_56 = count_in_56 + 2*20
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:20]:
#        j.connect_cells(i, 1, 0.0025)
#        count_in_56 = count_in_56 + 1*20
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:20]:
#        j.connect_cells(i, -1, 0.0025)
#        count_links_56 = count_links_56 + 1*20
#
#
#
#
#for i in rec_neurons9:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:30]:
#        j.connect_cells(i, 1, 0.0025)
#        #j.connect_cells(i, 0)
#        count_in_56=count_in_56+1*30
#    random.shuffle(rec_neurons7)
#    for j in rec_neurons7[0:20]:
#        j.connect_cells(i, -1, 0.0025)
#        count_in_56 = count_in_56 + 1*20
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.0025)
#        #j.connect_cells(i, 0)
#        count_in_56 = count_in_56 + 1*10
#    random.shuffle(rec_neurons12)
#    for j in rec_neurons12[0:3]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_in_56 = count_in_56 + 1*3
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:20]:
#        j.connect_cells(i, 1, 0.00025)
#        #j.connect_cells(i, 0)
#        count_in_56 = count_in_56 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:20]:
#        #j.connect_cells(i, 0)
#        j.connect_cells(i, 1, 0.00025)
#        count_in_56 = count_in_56 + 1*20
#    random.shuffle(rec_neurons7)
#    for j in rec_neurons7[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_56 = count_in_56 + 1*20
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_links_56 = count_links_56 + 1*20
#
#
#dg['5-6 (700-1700)'] = {
#    'count_cells' : [count_cells_56],
#    'count_links' : [count_links_56],
#    'count_in' : [count_in_56]
#    }
#logging.info('level 5-6')
##_________________________ 6 (1200-1700)___________________________________________
#count_cells_6=NnontuftRS6
#count_links_6=0
#count_in_6=0
#
#for i in rec_neurons10:
#    random.shuffle(rec_neurons13)
#    for j in rec_neurons13[0:3]:
#        j.connect_cells(i, 1, 0.00025)
#        j.connect_cells(i, 0, 0.00025)
#        count_in_6=count_in_6+2*3
#    random.shuffle(rec_neurons6)
#    for j in rec_neurons6[0:20]:
#        j.connect_cells(i, 1, 0.025)
#        count_in_6 = count_in_6 + 1*20
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:20]:
#        j.connect_cells(i, 1, 0.025)
#        j.connect_cells(i, 0, 0.0000025)
#        count_links_6 = count_links_6 + 2*20
#    random.shuffle(rec_neurons7)
#    for j in rec_neurons7[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_6 = count_in_6 + 1*20
#    random.shuffle(rec_neurons8)
#    for j in rec_neurons8[0:5]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_6 = count_in_6 + 1*5
#    random.shuffle(rec_neurons9)
#    for j in rec_neurons9[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_6 = count_in_6 + 1*20
#    #random.shuffle(rec_neurons12)
#    #for j in rec_neurons12[0:1]:
#    #    j.connect_cells(i, 1)
#    #    j.connect_cells(i, 0)
#    #    count_in_6 = count_in_6 + 2
#    random.shuffle(rec_neurons3)
#    for j in rec_neurons3[0:20]:
#        j.connect_cells(i, -1, 0.00025)
#        count_in_6 = count_in_6 + 1*20
#    random.shuffle(rec_neurons5)
#    for j in rec_neurons5[0:20]:
#        j.connect_cells(i, 1, 0.25)
#        j.connect_cells(i, 0, 0.0025)
#        count_in_6 = count_in_6 + 2*20
#    random.shuffle(rec_neurons4)
#    for j in rec_neurons4[0:20]:
#        j.connect_cells(i, 1, 0.25)
#        count_in_6 = count_in_6 + 1*20
#    random.shuffle(rec_neurons14)
#    for j in rec_neurons14[0:30]:
#        j.connect_cells(i, 1, 0.0025)
#    random.shuffle(rec_neurons15)
#    for j in rec_neurons15[0:30]:
#        j.connect_cells(i, 1, 0.0025)
#
#dg['6 (1200-1700)'] = {
#    'count_cells' : [count_cells_6],
#    'count_links' : [count_links_6],
#    'count_in' : [count_in_6]
#    }
logging.info('level 6')

#_____________________________thalamus___________________________________

#for i in rec_neurons14:
#    #random.shuffle(rec_neurons13)
#    #for j in rec_neurons13[0:3]:
#    #    j.connect_cells(i, 1, 0.0000025)
#    #random.shuffle(rec_neurons12)
#    #for j in rec_neurons12[0:3]:
#    #    j.connect_cells(i, 1, 0.0000025)
#    #random.shuffle(rec_neurons1)
#    #for j in rec_neurons1[0:3]:
#    #    j.connect_cells(i, 1, 0.0000025)
#    #random.shuffle(rec_neurons2)
#    #for j in rec_neurons2[0:3]:
#    #    j.connect_cells(i, 1, 0.0000025)
#    #random.shuffle(rec_neurons4)
#    #for j in rec_neurons4[0:40]:
#    #    j.connect_cells(i, 1, 0.0025)
#    #random.shuffle(rec_neurons5)
#    #for j in rec_neurons5[0:10]:
#    #    j.connect_cells(i, 1, 0.000025)
#    #random.shuffle(rec_neurons6)
#    #for j in rec_neurons6[0:10]:
#    #    j.connect_cells(i, 1, 0.000025)
#    random.shuffle(rec_neurons10)
#    for j in rec_neurons10[0:10]:
#        j.connect_cells(i, 1, 0.0025)
#    random.shuffle(rec_neurons15)
#    for j in rec_neurons15[0:10]:
#        j.connect_cells(i, 1, 0.0025)
#
#for i in rec_neurons15:
#    random.shuffle(rec_neurons14)
#    for j in rec_neurons14[0:3]:
#        j.connect_cells(i, 1, 0.025)
#    random.shuffle(rec_neurons15)
#    for j in rec_neurons15[0:3]:
#        j.connect_cells(i, 1, 0.00025)

logging.info('done')


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
logging.info('add stims')
stims=[]
for i in range(0,200):
    for j in range(0,30):
        stim = h.NetStim()
        stim.number = 3
        stim.start = random.randint(3,5)
        ncstim = h.NetCon(stim, rec_neurons4[i].synlistexE[j])
        ncstim.delay = 0.5#random.randint(1,5)
        ncstim.weight[0] = 1
        stims.append(ncstim)
        stims.append(stim)
#for i in range(0,200):
#    stim = h.NetStim()
#    stim.number = 1
#    stim.start = random.randint(3,5)
#    ncstim = h.NetCon(stim, rec_neurons4[i].synlistexE[0])
#    ncstim.delay = 0.5#random.randint(1,5)
#    ncstim.weight[0] = 1
#    stims.append(ncstim)
#    stims.append(stim)

#kecs = h.Vector()
#kecs.record(k[ecs].node_by_location(0, 0, 0)._ref_value)


# initialize and set the intracellular concentrations
logging.info('initialize-start')
h.finitialize()
logging.info('initialize-go')

def progress_bar(tstop, size=40):
    """ report progress of the simulation """
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()

h.dt = 0.1

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


def csv_writer(data, path, arr):
    """
    Write data to a CSV file path
    """
    with open(path, "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = arr)
        for line in data:
            writer.writerow(line)


def run(tstop):
    volt_gada = []
    volt=[]
    all=[]
    all_volt = []
    while pc.t(0) <= tstop:
        if int(pc.t(0) * 10) % 5 == 0 and pcid == 0:
            progress_bar(tstop)
            for j in cell:
                for n in j:
                    all_volt.append({"t": int(pc.t(0)),
                                 "x": n.x,
                                 "y": n.y,
                                 "z": n.z,
                                 "v": n.somaV[-1],
                                 "id": n.id,
                                 "num": n.number,
                                 "name": n.name})
                    if n.Excitatory==1:
                        volt.append({"t" : int(pc.t(0)),
                                        "x" : n.x,
                                        "y" : n.y,
                                        "z" : n.z,
                                        "v" : n.somaV[-1],
                                        "id": n.id,
                                        "num": n.number,
                                        "name": n.name})
                    else:
                        volt_gada.append({"t": int(pc.t(0)),
                                     "x": n.x,
                                     "y": n.y,
                                     "z": n.z,
                                     "v": n.somaV[-1],
                                     "id": n.id,
                                     "num": n.number,
                                     "name": n.name})


        pc.psolve(pc.t(0) + h.dt)



    logging.info('Simulation complete.')
    pc.barrier()
    if pcid == 0:
        for j in cell:
            for n in j:
                plot_spike_html(n,time, n.number)





        csv_writer(volt, os.path.join(outdir, 'volt.csv'), ["t",
                             "x",
                             "y",
                             "z",
                             "v",
                             "id",
                             "num",
                            "name"])
        logging.info("write to file - volt.csv")

        csv_writer(volt, os.path.join(outdir, 'volt_all.csv'), ["t",
                                                            "x",
                                                            "y",
                                                            "z",
                                                            "v",
                                                            "id",
                                                            "num",
                                                            "name"])
        logging.info("write to file - volt_all.csv")


        csv_writer(volt_gada, os.path.join(outdir, 'volt_gaba.csv'),["t",
                             "x",
                             "y",
                             "z",
                             "v",
                             "id",
                             "num",
                            "name"])
        logging.info("write to file - volt_gaba.csv")


        pc.runworker()
        pc.done()
        h.quit()


run(100)