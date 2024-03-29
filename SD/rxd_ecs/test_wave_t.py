import random
import os
import sys
import csv
from cells import *
import json
import logging
import neuron.rxd as rxd
from neuron.units import ms, mV

h.nrnmpi_init()
pc = h.ParallelContext()

pcid = pc.id()
nhost = pc.nhost()
root = 0
#pc.set_maxstep(0.5)


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
outdir = os.path.abspath('tests/989_100_tW')
value=0#100 #% epilepsy 

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

num=0

count_cells = 0
count_syn = 0

#0-400

data={}
data['cells']=[]



rec_neurons12=[]
logging.info('Create neurons')


epi=int(value*NsyppyrFRB/100)
for i in range(0,NsyppyrFRB-epi):
    rec_neurons12.append(SyppyrFRB(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform( -850+somaR,-450),
    i+num))
    data['cells'].append({
        'name': rec_neurons12[i].name,
        'id': rec_neurons12[i].id,
        'num': rec_neurons12[i].number,
        'x': rec_neurons12[i].x,
        'y' : rec_neurons12[i].y,
        'z' : rec_neurons12[i].z
    })

if value!=0:
    for i in range(0, epi):
        rec_neurons12.append(EpilepsySyppyrFRB(
            random.uniform(somaR, Lx - somaR),
            random.uniform(somaR, Ly - somaR),
            random.uniform(-850 + somaR, -450),
            i + num))
        data['cells'].append({
            'name': rec_neurons12[i].name,
            'id': rec_neurons12[i].id,
            'num': rec_neurons12[i].number,
            'x': rec_neurons12[i].x,
            'y': rec_neurons12[i].y,
            'z': rec_neurons12[i].z
        })

num+=50

rec_neurons13 = []
epi=int(value*NsyppyrRS/100)
for i in range(0,NsyppyrRS-epi):
    rec_neurons13.append(SyppyrRS(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(-850+somaR,-450),
    i+num))
    data['cells'].append({
        'name': rec_neurons13[i].name,
        'id': rec_neurons13[i].id,
        'num': rec_neurons13[i].number,
        'x': rec_neurons13[i].x,
        'y': rec_neurons13[i].y,
        'z': rec_neurons13[i].z
    })

if value!=0:
    for i in range(0, epi):
        rec_neurons13.append(EpilepsySyppyrRS(
            random.uniform(somaR, Lx - somaR),
            random.uniform(somaR, Ly - somaR),
            random.uniform(-850 + somaR, -450),
            i + num))
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
    random.uniform(-850+somaR,-450),
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
    random.uniform(-850+somaR,-450),
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
    random.uniform(-850+somaR,-450),
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
epi=int(value*Nspinstel4/100)
for i in range(0,Nspinstel4-epi):
    rec_neurons4.append(Spinstel4(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(-450,-150), i+num))
    data['cells'].append({
        'name': rec_neurons4[i].name,
        'id': rec_neurons4[i].id,
        'num': rec_neurons4[i].number,
        'x': rec_neurons4[i].x,
        'y': rec_neurons4[i].y,
        'z': rec_neurons4[i].z
    })

if value!=0:
    for i in range(0, epi):
        rec_neurons4.append(EpilepsySpinstel4(
            random.uniform(somaR, Lx - somaR),
            random.uniform(somaR, Ly - somaR),
            random.uniform(-450, -150), i + num))
        data['cells'].append({
            'name': rec_neurons4[i].name,
            'id': rec_neurons4[i].id,
            'num': rec_neurons4[i].number,
            'x': rec_neurons4[i].x,
            'y': rec_neurons4[i].y,
            'z': rec_neurons4[i].z
        })

num+=Nspinstel4

rec_neurons16=[]
for i in range(0,Nbask4):
    rec_neurons16.append(Bask4(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(-450,-150), i+num))
    data['cells'].append({
        'name': rec_neurons16[i].name,
        'id': rec_neurons16[i].id,
        'num': rec_neurons16[i].number,
        'x': rec_neurons16[i].x,
        'y': rec_neurons16[i].y,
        'z': rec_neurons16[i].z
    })

num+=Nbask4
rec_neurons5=[]
epi=int(value*NtuftIB5/100)
for i in range(0,NtuftIB5 -epi):
    rec_neurons5.append(TuftIB5(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(-150,50), i+num))
    data['cells'].append({
        'name': rec_neurons5[i].name,
        'id': rec_neurons5[i].id,
        'num': rec_neurons5[i].number,
        'x': rec_neurons5[i].x,
        'y': rec_neurons5[i].y,
        'z': rec_neurons5[i].z
    })


if value!=0:
    for i in range(0, epi):
        rec_neurons5.append(EpilepsyTuftIB5(
            random.uniform(somaR, Lx - somaR),
            random.uniform(somaR, Ly - somaR),
            random.uniform(-150, 50), i + num))
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
epi=int(value*NtuftRS5/100)
for i in range(0,NtuftRS5-epi):
    rec_neurons6.append(TuftRS5(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(-150,350), i+num))
    data['cells'].append({
        'name': rec_neurons6[i].name,
        'id': rec_neurons6[i].id,
        'num': rec_neurons6[i].number,
        'x': rec_neurons6[i].x,
        'y': rec_neurons6[i].y,
        'z': rec_neurons6[i].z
    })

if value!=0:
    for i in range(0, epi):
        rec_neurons6.append(EpilepsyTuftRS5(
            random.uniform(somaR, Lx - somaR),
            random.uniform(somaR, Ly - somaR),
            random.uniform(-150, 350), i + num))
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
    random.uniform(-150,350), i+num))
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
    random.uniform(-150,850), i+num))
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
    random.uniform(-150,850), i+num))
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
epi=int(value*NnontuftRS6/100)
for i in range(0,NnontuftRS6-epi):
    rec_neurons10.append(NontuftRS6(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(350,850-somaR), i+num))
    data['cells'].append({
        'name': rec_neurons10[i].name,
        'id': rec_neurons10[i].id,
        'num': rec_neurons10[i].number,
        'x': rec_neurons10[i].x,
        'y': rec_neurons10[i].y,
        'z': rec_neurons10[i].z
    })
if value!=0:
    for i in range(0, epi):
        rec_neurons10.append(EpilepsyNontuftRS6(
            random.uniform(somaR, Lx - somaR),
            random.uniform(somaR, Ly - somaR),
            random.uniform(350, 850 - somaR), i + num))
        data['cells'].append({
            'name': rec_neurons10[i].name,
            'id': rec_neurons10[i].id,
            'num': rec_neurons10[i].number,
            'x': rec_neurons10[i].x,
            'y': rec_neurons10[i].y,
            'z': rec_neurons10[i].z
        })

num += NnontuftRS6





rec_neurons14=[]
for i in range(0,NTCR):
    rec_neurons14.append(TCR(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(1000,1300-somaR), i+num))
    data['cells'].append({
        'name': rec_neurons14[i].name,
        'id': rec_neurons14[i].id,
        'num': rec_neurons14[i].number,
        'x': rec_neurons14[i].x,
        'y': rec_neurons14[i].y,
        'z': rec_neurons14[i].z
    })
num +=NTCR

rec_neurons15=[]
for i in range(0,NTCR):
    rec_neurons15.append(nRT(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(1100,1300-somaR), i+num))
    data['cells'].append({
        'name': rec_neurons15[i].name,
        'id': rec_neurons15[i].id,
        'num': rec_neurons15[i].number,
        'x': rec_neurons15[i].x,
        'y': rec_neurons15[i].y,
        'z': rec_neurons15[i].z
    })
num +=NnRT
#2710
cell=[rec_neurons12, rec_neurons13, rec_neurons1, rec_neurons2, rec_neurons3, rec_neurons4, rec_neurons5, rec_neurons6, rec_neurons7, rec_neurons8, rec_neurons9, rec_neurons10, rec_neurons14, rec_neurons15, rec_neurons16 ]
#for i in range(0,Nspinstel4):
#    rec_neurons4.append(Spinstel4(
#    random.uniform(somaR,Lx-somaR),
#    random.uniform(somaR,Ly-somaR),
#    random.uniform(350,50), i+num))
#    data['cells'].append({
#        'name': rec_neurons4[i].name,
#        'id': rec_neurons4[i].id,
#        'num': rec_neurons4[i].number,
#        'x': rec_neurons4[i].x,
#        'y': rec_neurons4[i].y,
#        'z': rec_neurons4[i].z
#    })
#------for test----------
#i4 = random.randint(0, Nspinstel4)
#i5=random.randint(0, NtuftIB5)
#i6 = random.randint(0, NtuftRS5)
#print('start connect_cells.')
logging.info('start connect_cells')
#---------------------- 2/3 (0-400) ---------------------
count_cells_23=Nbask23+Naxax23+NsyppyrFRB+NsyppyrRS+NLTS23
count_links_23=0
count_in_23=0
#count_out_23=0

for i in rec_neurons13:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:10]:
        j.connect_cells(i, 1, 0.000025,random.randint(1,2))
        j.connect_cells(i, 0, 0.000025, random.randint(1,2))
        count_links_23=count_links_23+2*50
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:15]:
        j.connect_cells(i, 1, 0.000025, random.randint(1,2))
        j.connect_cells(i, 0, 0.000025, random.randint(1,2))
        count_links_23=count_links_23+2*15
    #random.shuffle(rec_neurons13)

    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:20]:
        j.connect_cells(i, -1, 0.9, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons2)
    for j in rec_neurons2[0:20]:
        j.connect_cells(i, -1,0.9, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1, 0.9, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:5]:
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        #j.connect_cells(i, 0,0.25, random.randint(1,2))
        count_in_23 = count_in_23 + 2*100
    #random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:50]:
    #    j.connect_cells(i, 0, 0.25, random.randint(6,8))
    #    j.connect_cells(i, 1, 0.025, random.randint(6,8))
    #    count_in_23 = count_in_23 + 2*50
    #random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:50]:
    #    j.connect_cells(i, 1, 0.025, random.randint(1,2))
    #    count_in_23 = count_in_23 + 1*50
    #random.shuffle(rec_neurons8)
    #for j in rec_neurons8[0:5]:
    #    j.connect_cells(i, -1, 0.25, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*5
    #random.shuffle(rec_neurons9)
    #for j in rec_neurons9[0:10]:
    #    j.connect_cells(i, -1, 0.25, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*10
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:10]:
    #    j.connect_cells(i, 1, 0.00025)
    #    j.connect_cells(i, 0, 0.0000025)
    #    count_in_23 = count_in_23 + 2*10
    #for j in rec_neurons14[0:10]:
    #    j.connect_cells(i, 1, 0.000025, random.randint(10,15))
#

for i in rec_neurons12:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:10]:
        j.connect_cells(i, 1, 0.15, random.randint(1,2))
        j.connect_cells(i, 0, 0.000025, random.randint(1,2))
        count_links_23=count_links_23+2*50
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1, 0.15, random.randint(1,2))
        j.connect_cells(i, 0, 0.00025, random.randint(1,2))
        count_links_23=count_links_23+2*20
    #random.shuffle(rec_neurons13)
    #for j in rec_neurons13[0:10]:
    #    j.connect_cells(i, 1, 0.25, random.randint(1, 2))
    #    j.connect_cells(i, 0, 0.25, random.randint(1, 2))
    #    count_links_23 = count_links_23 + 2 * 50
    #random.shuffle(rec_neurons12)
    #for j in rec_neurons12[0:20]:
    #    j.connect_cells(i, 1, 0.25, random.randint(1, 2))
    #    j.connect_cells(i, 0, 0.25, random.randint(1, 2))
    #    count_links_23 = count_links_23 + 2 * 20
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:10]:
        j.connect_cells(i, -1, 0.9, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons2)
    for j in rec_neurons2[0:10]:
        j.connect_cells(i, -1, 0.9, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:10]:
        j.connect_cells(i, -1, 0.9, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:5]:
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        #j.connect_cells(i, 0, 0.25, random.randint(2,3))
        count_in_23 = count_in_23 + 2*20
    #random.shuffle(rec_neurons5)
    #for j in rec_neurons5[0:50]:
    #    j.connect_cells(i, 0, 0.25, random.randint(6,8))
    #    j.connect_cells(i, 1, 0.25, random.randint(6,8))
    #    count_in_23 = count_in_23 + 2*50
    #random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:50]:
    #    j.connect_cells(i, 1, 0.025, random.randint(6,8))
    #    count_in_23 = count_in_23 + 1*50
    #random.shuffle(rec_neurons8)
    #for j in rec_neurons8[0:5]:
    #    j.connect_cells(i, -1, 0.25, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*5
    #random.shuffle(rec_neurons9)
    #for j in rec_neurons9[0:10]:
    #    j.connect_cells(i, -1, 0.25, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*5
   #random.shuffle(rec_neurons10)
   #for j in rec_neurons10[0:10]:
   #    j.connect_cells(i, 1, 0.0025, random.randint(6,8))
   #    j.connect_cells(i, 0, 0.25, random.randint(6,8))
   #    count_in_23 = count_in_23 + 2*10
    #for j in rec_neurons14[0:10]:
    #    j.connect_cells(i, 1, 0.25, random.randint(10,15))


for i in rec_neurons1:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:10]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_links_23=count_links_23+1*90
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_links_23=count_links_23+1*5
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:10]:
        j.connect_cells(i, -1, 0.00025, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1, 0.00025, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:10]:
        j.connect_cells(i, 1, 0.025, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 1*20
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:10]:
        #j.connect_cells(i, 0)
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        count_in_23 = count_in_23 + 1*20
    random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:20]:
    #    j.connect_cells(i, 1, 0.025, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*20
    #random.shuffle(rec_neurons9)
    #for j in rec_neurons9[0:10]:
    #    j.connect_cells(i, -1, 0.25, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*10
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:10]:
    #    j.connect_cells(i, 1, 0.025, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*10
    #for j in rec_neurons14[0:10]:
    #    j.connect_cells(i, 1, 0.25, random.randint(10,15))






for i in rec_neurons2:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:10]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_links_23=count_links_23+1*90
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_links_23=count_links_23+1*5
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:10]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:10]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:10]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 1*20
    #random.shuffle(rec_neurons5)
    #for j in rec_neurons5[0:20]:
    #    #j.connect_cells(i, 0)
    #    j.connect_cells(i, 1, 0.025, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*20
    #random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:20]:
    #    j.connect_cells(i, 1, 0.025, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*20
    #random.shuffle(rec_neurons9)
    #for j in rec_neurons9[0:10]:
    #    j.connect_cells(i, -1, 0.25, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*10
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:10]:
    #    j.connect_cells(i, 1, 0.00025, random.randint(2,3))
    #    count_in_23 = count_in_23 + 1*10
    #for j in rec_neurons14[0:10]:
    #    j.connect_cells(i, 1, 0.0025, random.randint(15, 19))




for i in rec_neurons3:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:0]:
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_links_23=count_links_23+ 1*90
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_links_23 = count_links_23 + 1*5
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:10]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:10]:
        j.connect_cells(i, -1, 0.0025, random.randint(1,2))
        count_links_23 = count_links_23 + 1*20
    #random.shuffle(rec_neurons4)
    #for j in rec_neurons4[0:20]:
    #    j.connect_cells(i, 1, 0.00025, random.randint(1,2))
    #    #j.connect_cells(i, 0)
    #    count_in_23 = count_in_23 + 1*20
    #random.shuffle(rec_neurons5)
    #for j in rec_neurons5[0:20]:
    #    #j.connect_cells(i, 0)
    #    j.connect_cells(i, 1, 0.00025, random.randint(1,2))
    #    count_in_23 = count_in_23 + 1*20
    #random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:20]:
    #    j.connect_cells(i, 1, 0.00025, random.randint(1,2))
    #    count_in_23 = count_in_23 + 1*20
    #random.shuffle(rec_neurons9)
    #for j in rec_neurons9[0:10]:
    #    j.connect_cells(i, -1, 0.25, random.randint(1,2))
    #    count_in_23 = count_in_23 + 1*10


dg={}
dg['2-3'] = []
dg['2-3'].append({
    'count_cells' : [count_cells_23],
    'count_links' : [count_links_23],
    'count_in' : [count_in_23]
    })
logging.info('level 2-3')
#_________________________ 4 (400-700)______________________________
count_cells_4=Nspinstel4+Nbask4
count_links_4=0
count_in_4=0

for i in rec_neurons4:
    #random.shuffle(rec_neurons13)
    #for j in rec_neurons13[0:3]:
    #    j.connect_cells(i, 0, 0.25, random.randint(6,8))
    #    j.connect_cells(i, 1, 0.0025, random.randint(6,8))
    #    count_in_4=count_in_4+2*3
    #random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:20]:
    #    j.connect_cells(i, 1, 0.00025)
    #    count_in_4 = count_in_4 + 1*20
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:30]:
    #    j.connect_cells(i, 1, 0.025, random.randint(6,8))
    #    j.connect_cells(i, 0, 0.25, random.randint(6,8))
    #    count_in_4 = count_in_4 + 2*30
    #random.shuffle(rec_neurons12)
    #for j in rec_neurons12[0:2]:
    #    j.connect_cells(i, 0, 0.25, random.randint(6,8))
    #    j.connect_cells(i, 1, 0.00025, random.randint(6,8))
    #    count_in_4 = count_in_4 + 1*2
    #random.shuffle(rec_neurons1)
    #for j in rec_neurons1[0:20]:
    #    j.connect_cells(i, -1, 0.25, random.randint(11,15))
    #    count_in_4 = count_in_4 + 1*20
    #random.shuffle(rec_neurons2)
    #for j in rec_neurons2[0:5]:
    #    j.connect_cells(i, -1, 0.05, random.randint(11,15))
    #    count_in_4 = count_in_4 + 1*5
    #random.shuffle(rec_neurons3)
    #for j in rec_neurons3[0:20]:
    #    j.connect_cells(i, -1, 0.25, random.randint(11,15))
    #    count_in_4 = count_in_4 + 1*20
    #random.shuffle(rec_neurons7)
   #for j in rec_neurons7[0:20]:
   #    j.connect_cells(i, -1, 0.25, random.randint(13,15))
   #    count_in_4 = count_in_4 + 1*20
   #random.shuffle(rec_neurons9)
   #for j in rec_neurons9[0:20]:
   #    j.connect_cells(i, -1, 0.25, random.randint(14,17))
   #    count_in_4 = count_in_4 + 1*20
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:5]:
        j.connect_cells(i, 1, 0.3, random.randint(1,2))
        j.connect_cells(i, 0, 0.5, random.randint(1,2))
        count_links_4 = count_links_4 + 2*10
    #random.shuffle(rec_neurons4)
    #for j in rec_neurons4[0:50]:
    #    j.connect_cells(i, 1, 0.3, random.randint(1, 2))
    #    j.connect_cells(i, 0, 0.25, random.randint(1, 2))
    #    count_links_4 = count_links_4 + 2 * 50
    #for j in rec_neurons4[0:10]:
    #    j.connect_cells(i, 1, 0.3, random.randint(2,3))
    #    j.connect_cells(i, 0, 0.25, random.randint(2,3))
    #for j in rec_neurons4[0:10]:
    #    j.connect_cells(i, 1, 0.3, random.randint(2,3))
    #    j.connect_cells(i, 0, 0.25, random.randint(2,3))
    random.shuffle(rec_neurons16)
    for j in rec_neurons16[0:20]:
        j.connect_cells(i, -1, 0.00009, random.randint(1,2))
        count_in_4 = count_in_4 + 1 * 100
    for j in rec_neurons14[0:10]:
        j.connect_cells(i, 1, 0.5, random.randint(2, 3))
    #for j in rec_neurons14[0:50]:
    #    j.connect_cells(i, 1, 1, random.randint(10, 15))

    #random.shuffle(rec_neurons5)
    #for j in rec_neurons5[0:3]:
    #    j.connect_cells(i, 0)
    #    j.connect_cells(i, 1)
    #    count_links_4 = count_links_4 + 2



for i in rec_neurons16:
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:30]:
        j.connect_cells(i, 1, 0.7, random.randint(1,2))
        #j.connect_cells(i, 1, 0.00025)
        count_in_4=count_in_4+1*100


dg['4'] = {
    'count_cells' : [count_cells_4],
    'count_links' : [count_links_4],
    'count_in' : [count_in_4]
    }
logging.info('level 4')
#_____________________5 (700-1200)___________________________________
count_cells_5=NtuftRS5 + Nbask56+NtuftIB5
count_links_5=0
count_in_5=0

for i in rec_neurons5:

    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:1]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        j.connect_cells(i, 0, 0.1, random.randint(1,2))
        count_in_5=count_in_5+2*60
    random.shuffle(rec_neurons6)
    #for j in rec_neurons6[0:1]:
    #    j.connect_cells(i, 1, 0.05, random.randint(1,2))
    #    count_links_5 = count_links_5 + 1*200
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:10]:
    #    j.connect_cells(i, 1, 0.025, random.randint(6,8))
    #    j.connect_cells(i, 0, 0.25, random.randint(6,8))
    #    count_in_5 = count_in_5 + 2*10
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:2]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        j.connect_cells(i, 0, 0.05, random.randint(1,2))
        count_in_5 = count_in_5 + 2*3
    random.shuffle(rec_neurons2)
    for j in rec_neurons2[0:5]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_in_5 = count_in_5 + 1*5
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_in_5 = count_in_5 + 1*20
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:10]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_links_5 = count_links_5 + 1*20
    random.shuffle(rec_neurons8)
    for j in rec_neurons8[0:5]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_in_5 = count_in_5 + 1*20
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:5]:
        j.connect_cells(i, -1, 0.00025, random.randint(1,2))
        count_in_5 = count_in_5 + 1*20
    random.shuffle(rec_neurons5)
    #for j in rec_neurons5[0:5]:
    #    j.connect_cells(i, 0, 0.05, random.randint(1,2))
    #    #j.connect_cells(i, 1, 0.25, random.randint(1,2))
    #    count_links_5 = count_links_5 + 2*5
    #random.shuffle(rec_neurons4)
    #for j in rec_neurons4[0:20]:
    #    j.connect_cells(i, 1, 0.00025, random.randint(6,8))
    #    count_in_5 = count_in_5 + 1*20
    #random.shuffle(rec_neurons14)
    #for j in rec_neurons14[0:30]:
    #    j.connect_cells(i, 1, 0.25, random.randint(15, 17))


for i in rec_neurons6:
    random.shuffle(rec_neurons14)
    for j in rec_neurons14[0:1]:
        j.connect_cells(i, 1, 0.2, random.randint(2, 3))
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:1]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
        j.connect_cells(i, 0, 0.025, random.randint(1,2))
        count_in_5=count_in_5+2*300
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:3]:
        j.connect_cells(i, 1, 0.025, random.randint(1,2))
        j.connect_cells(i, 0, 0.025, random.randint(1,2))
        count_links_5 = count_links_5 + 1*10
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:4]:
    #    j.connect_cells(i, 1, 0.025, random.randint(2,3))
    #    j.connect_cells(i, 0, 0.25, random.randint(2,3))
    #    count_in_5 = count_in_5 + 2*10
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:2]:
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        j.connect_cells(i, 0, 0.25, random.randint(1,2))
        count_in_5 = count_in_5 + 2*30
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:10]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_links_5 = count_links_5 + 1*20
    random.shuffle(rec_neurons8)
    for j in rec_neurons8[0:5]:
        j.connect_cells(i, -1, 0.5, random.randint(1,2))
        count_links_5 = count_links_5 + 1*5
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_in_5 = count_in_5 + 1*20
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_in_5 = count_in_5 + 1*20
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:1]:
        j.connect_cells(i, 0, 0.25, random.randint(1,2))
        j.connect_cells(i, 1, 0.025, random.randint(1,2))
        count_in_5 = count_in_5 + 2*20
    #random.shuffle(rec_neurons14)
    #for j in rec_neurons14[0:30]:
    #    j.connect_cells(i, 1, 0.25, random.randint(15, 18))




for i in rec_neurons7:
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:3]:
        j.connect_cells(i, -1, 0.0025, random.randint(1,2))
    #    #j.connect_cells(i, 0)
        count_in_5=count_in_5+1*30
        random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:3]:
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        count_links_5 = count_links_5 + 1*20
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:3]:
    #    j.connect_cells(i, 1, 0.00025, random.randint(1,2))
    #    #j.connect_cells(i, 0)
    #    count_in_5 = count_in_5 + 1*10
    #random.shuffle(rec_neurons12)
    #for j in rec_neurons12[0:3]:
    #    j.connect_cells(i, -1, 0.0000025)
    #    #j.connect_cells(i, 0)
    #    count_in_5 = count_in_5 + 1*3
    #random.shuffle(rec_neurons3)
    #for j in rec_neurons3[0:20]:
    #    j.connect_cells(i, -1, 0.0000025)
    #    count_in_5 = count_in_5 + 1*20
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:3]:
        j.connect_cells(i, -1, 0.0025, random.randint(1,2))
        count_links_5 = count_links_5 + 1*20
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:3]:
        j.connect_cells(i, -1, 0.0025, random.randint(1,2))
        count_in_5 = count_in_5 + 1*20
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:3]:
        #j.connect_cells(i, 0)
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        count_in_5 = count_in_5 + 1*20
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:3]:
        j.connect_cells(i, 1, 0.0025, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_in_5 = count_in_5 + 1*20
    #random.shuffle(rec_neurons14)
    #for j in rec_neurons14[0:10]:
    #    j.connect_cells(i, 1, 0.25, random.randint(15, 18))

dg['5 (700-1200)'] = {
    'count_cells' : [count_cells_5],
    'count_links' : [count_links_5],
    'count_in' : [count_in_5]
    }
logging.info('level 5')
#______________________5-6 (700-1700)__________________________________
count_cells_56=Naxax56+NLTS56
count_links_56=0
count_in_56=0


for i in rec_neurons8:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:3]:
        j.connect_cells(i, 1, 0.0025, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_in_56=count_in_56+1*30
    #random.shuffle(rec_neurons7)
    #for j in rec_neurons7[0:20]:
    #    j.connect_cells(i, -1, 0.0000025)
    #    count_in_56 = count_in_56 + 1*20
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:10]:
    #    j.connect_cells(i, 1, 0.025, random.randint(6,8))
    #    #j.connect_cells(i, 0)
    #    count_in_56 = count_in_56 + 1*10
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:3]:
        j.connect_cells(i, 1, 0.0025, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_in_56 = count_in_56 + 1*3
    #random.shuffle(rec_neurons4)
    #for j in rec_neurons4[0:20]:
    #    j.connect_cells(i, -1, 0.0000025)
    #    #j.connect_cells(i, 0)
    #    count_in_56 = count_in_56 + 1*20
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:2]:
        #j.connect_cells(i, 0)
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        count_in_56 = count_in_56 + 2*20
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:2]:
        j.connect_cells(i, 1, 0.25, random.randint(1,2))
        count_in_56 = count_in_56 + 1*20
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:2]:
        j.connect_cells(i, -1, 0.00025, random.randint(1,2))
        count_links_56 = count_links_56 + 1*20
    #random.shuffle(rec_neurons14)
    #for j in rec_neurons14[0:10]:
    #    j.connect_cells(i, 1, 0.25, random.randint(15, 18))





for i in rec_neurons9:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:3]:
        j.connect_cells(i, 1, 0.0025, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_in_56=count_in_56+1*30
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:2]:
        j.connect_cells(i, -1, 0.0025, random.randint(1,2))
        count_in_56 = count_in_56 + 1*20
    #random.shuffle(rec_neurons10)
    #for j in rec_neurons10[0:10]:
    #    j.connect_cells(i, 1, 0.025, random.randint(3,6))
    #    #j.connect_cells(i, 0)
    #    count_in_56 = count_in_56 + 1*10
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:3]:
        j.connect_cells(i, 1, 0.0025, random.randint(1,2))
        #j.connect_cells(i, 0)
        count_in_56 = count_in_56 + 1*3
    #random.shuffle(rec_neurons4)
    #for j in rec_neurons4[0:20]:
    #    j.connect_cells(i, 1, 0.0025, random.randint(6,8))
    #    #j.connect_cells(i, 0)
    #    count_in_56 = count_in_56 + 1*20
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:2]:
        #j.connect_cells(i, 0)
        j.connect_cells(i, 1, 0.15, random.randint(1,2))
        count_in_56 = count_in_56 + 1*20
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:2]:
        j.connect_cells(i, -1, 0.0025, random.randint(1,2))
        count_in_56 = count_in_56 + 1*20
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:2]:
        j.connect_cells(i, -1, 0.0025, random.randint(1,2))
        count_links_56 = count_links_56 + 1*20


dg['5-6 (700-1700)'] = {
    'count_cells' : [count_cells_56],
    'count_links' : [count_links_56],
    'count_in' : [count_in_56]
    }
logging.info('level 5-6')
#_________________________ 6 (1200-1700)___________________________________________
count_cells_6=NnontuftRS6
count_links_6=0
count_in_6=0

for i in rec_neurons10:
    #random.shuffle(rec_neurons13)
    #for j in rec_neurons13[0:10]:
    #    j.connect_cells(i, 1, 0.05, random.randint(3,4))
    #    j.connect_cells(i, 0, 0.25, random.randint(3,4))
    #    count_in_6=count_in_6+2*3

    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:10]:
        j.connect_cells(i, 1, 0.2, random.randint(2,3))
        j.connect_cells(i, 0, 0.2, random.randint(2, 3))
        count_in_6 = count_in_6 + 1*10
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:6]:
        j.connect_cells(i, 1, 0.02, random.randint(1,2))
        j.connect_cells(i, 0, 0.025, random.randint(1,2))
        count_links_6 = count_links_6 + 2*6
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, -1, 0.0005, random.randint(1,2))
        count_in_6 = count_in_6 + 1*20
    random.shuffle(rec_neurons8)
    for j in rec_neurons8[0:5]:
        j.connect_cells(i, -1, 0.005, random.randint(1,2))
        count_in_6 = count_in_6 + 1*5
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1, 0.005, random.randint(1,2))
        count_in_6 = count_in_6 + 1*20
    #random.shuffle(rec_neurons12)
    #for j in rec_neurons12[0:1]:
    #    j.connect_cells(i, 1)
    #    j.connect_cells(i, 0)
    #    count_in_6 = count_in_6 + 2
    #random.shuffle(rec_neurons3)
    #for j in rec_neurons3[0:20]:
    #    j.connect_cells(i, -1, 0.05, random.randint(2,3))
    #    count_in_6 = count_in_6 + 1*20
    #random.shuffle(rec_neurons5)
    #for j in rec_neurons5[0:10]:
    #    j.connect_cells(i, 1, 0.7, random.randint(1,2))
    #    #j.connect_cells(i, 0, 0.025, random.randint(6,8))
    #    count_in_6 = count_in_6 + 2*20
    #random.shuffle(rec_neurons4)
    #for j in rec_neurons4[0:20]:
    #    j.connect_cells(i, 1, 0.025, random.randint(6,8))
    #    count_in_6 = count_in_6 + 1*20
    #random.shuffle(rec_neurons14)
    #for j in rec_neurons14[0:30]:
    #    j.connect_cells(i, 1, 0.025, random.randint(5,10))


dg['6 (1200-1700)'] = {
    'count_cells' : [count_cells_6],
    'count_links' : [count_links_6],
    'count_in' : [count_in_6]
    }
logging.info('level 6')

#_____________________________thalamus___________________________________

for i in rec_neurons14:
    #random.shuffle(rec_neurons14)
    #for j in rec_neurons14[0:20]:
        #j.connect_cells(i, 0, 0.3, random.randint(1, 2))
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1, 0.5, random.randint(1,2))
    random.shuffle(rec_neurons15)
    for j in rec_neurons15[0:10]:
        j.connect_cells(i, -1, 0.005, random.randint(1,2))

for i in rec_neurons15:
    random.shuffle(rec_neurons14)
    for j in rec_neurons14[0:10]:
        j.connect_cells(i, 1, 0.7, random.randint(1,2))
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:3]:
        j.connect_cells(i, 1, 0.25, random.randint(1,2))

logging.info('done')


alpha = alpha1
tort = tort1



'''
ecs = rxd.Extracellular(0, 0,
                        -850, 100, 100, 1300, dx=(10, 10, 30),  # dx - скорость распространнения в разные стороны - различны по осям
                        volume_fraction=alpha, tortuosity=tort)
volt = rxd.Species(ecs, name='v', d=0, charge=0, initial=None)

k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial= 3.5,
                ecs_boundary_conditions=3.5)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=142,
                 ecs_boundary_conditions=142)
'''


logging.info('add stims')
stims=[]
for i in range(0,100):
    j=0#random.randint(0,4)
    #for j in range(0,5):
    random.shuffle(rec_neurons14)
    stim = h.NetStim()
    stim.number = 2
    stim.start = 1
    ncstim = h.NetCon(stim, rec_neurons14[i].synlistexE[j])
    ncstim.delay = random.gauss(1, 1 / 4)
    ncstim.weight[0] = random.gauss(0.5, 0.5 / 6)
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
pc.set_maxstep(0.5 * ms)
#pc.set_maxstep(0.3)
# initialize and set the intracellular concentrations
logging.info('initialize-start')
h.finitialize()
logging.info('initialize-go')

def write_to_csw(data, nameFile, type='a'):
    File = open(nameFile, type)
    with File:
        writer = csv.writer(File)
        writer.writerows(data)
    File.close()

def progress_bar(tstop, size=40):
    """ report progress of the simulation """
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()

h.dt = 0.1
time = h.Vector().record(h._ref_t)
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
    volt_extr=[]
    data_ex = []
    data_exAll=[]
    while pc.t(0) <= tstop:
        for j in cell:
            for n in j:
                data_exAll.append({"t": pc.t(0),
                                "x": n.x,
                                "y": n.y,
                                "z": n.z,
                                "v": n.v_vec[-1],
                                "id": n.id
                                })
                if n.Excitatory==1:
                    data_ex.append({"t": pc.t(0),
                                     "x": n.x,
                                     "y": n.y,
                                     "z": n.z,
                                     "v": n.v_vec[-1],
                                     "id": n.id
                                     })
        if int(pc.t(0) * 10) % 10 == 0 and pcid == 0:
            logging.info('time: '.join(str(int(pc.t(0)))))
            #volt_extr.append(volt[ecs].states3d.mean(2))
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
                    volt_extr.append({"t": int(pc.t(0)),
                                     "x": n.x,
                                     "y": n.y,
                                     "z": n.z,
                                     "v": n.v_vec[-1],
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
    l=len(time)
    if pcid == 0:
        for j in cell:
            for n in j:
                if n.Excitatory == 1:
                    dd = [n.x, n.y, n.z, n.id]
                    dd.extend(n.spike_times)
                    write_to_csw([dd], os.path.join(outdir, 'spikeE.csv'))
                elif n.Excitatory == -1:
                    dd = [n.x, n.y, n.z, n.id]
                    dd.extend(n.spike_times)
                    write_to_csw([dd], os.path.join(outdir, 'spikeI.csv'))


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

        #for j in cell:
        #    for n in j:
        #        for i in range(l):
        #            all.append({"v": n.somaV[i],
        #                              "id": n.id,
        #                              #"num": n.number,
        #                              "name": n.name,
        #                        "t": time[i]})
        #        csv_writer(all, os.path.join(k_na_dir, '%i.csv' %n.number), ["v",
        #                                  "id",
        #                                  #"num",
        #                                  "name", "t"])

        with open(os.path.join(outdir, 'info.json'), 'w') as outfile:
            json.dump(dg, outfile)
        logging.info('write to file -info.json')

        csv_writer(volt_extr, os.path.join(outdir, 'volt_extr.csv'), ["t",
                             "x",
                             "y",
                             "z",
                             "v",
                             "id",
                             "num",
                            "name"])
        logging.info("write to file - volt_extr.csv")

        #data_ex=[]
        #ata_ex.append(['id','x','y','z'].extend(time))
        #or j in cell:
        #   for n in j:
        #       data_ex.append([n.id, n.x, n.y, n.z ].extend(n.v_vec))
        #ith open(os.path.join(outdir, 'extr_all.csv'), "w") as csv_file:
        #   file_writer = csv.writer(csv_file)
        #   file_writer.writerows(data_ex)
        csv_writer(data_ex, os.path.join(outdir, 'extr.csv'), ["t",
                                                                      "x",
                                                                      "y",
                                                                      "z",
                                                                      "v",
                                                                      "id"
                                                                     ])

        csv_writer(data_exAll, os.path.join(outdir, 'extr_all.csv'), ["t",
                                                                   "x",
                                                                   "y",
                                                                   "z",
                                                                   "v",
                                                                   "id"
                                                                   ])


        #logging.info("write to file - extr_all.csv")
        logging.info('the end')
        pc.runworker()
        pc.done()
        h.quit()


run(30)
