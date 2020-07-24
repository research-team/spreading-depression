import random
import os
import sys
import csv
from cells import *
import json
import logging
import neuron.rxd as rxd
h.nrnmpi_init()
pc = h.ParallelContext()
pcid = pc.id()
nhost = pc.nhost()
root = 0
pc.set_maxstep(10)

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
outdir = os.path.abspath('tests/887_tW')


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
NsyppyrFRB = 50
NsyppyrRS = 1000
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

data={}
data['cells']=[]
rec_neurons12=[]
logging.info('Create neurons')
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
#print('start connect_cells.')
logging.info('start connect_cells')
#---------------------- 2/3 (0-400) ---------------------
count_cells_23=Nbask23+Naxax23+NsyppyrFRB+NsyppyrRS+NLTS23
count_links_23=0
count_in_23=0
#count_out_23=0

for i in rec_neurons13:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:50]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    #print('cc13')
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1
    random.shuffle(rec_neurons2)
    for j in rec_neurons2[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1

    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:2]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:2]:
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons8)
    for j in rec_neurons8[0:5]:
        j.connect_cells(i, -1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:10]:
        j.connect_cells(i, -1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 2


for i in rec_neurons12:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:50]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1
    random.shuffle(rec_neurons2)
    for j in rec_neurons2[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1

    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:2]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:2]:
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons8)
    for j in rec_neurons8[0:5]:
        j.connect_cells(i, -1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:10]:
        j.connect_cells(i, -1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 2


for i in rec_neurons1:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:90]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1

    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:20]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:20]:
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:10]:
        j.connect_cells(i, -1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 1






for i in rec_neurons2:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:90]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1

    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:20]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:20]:
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:10]:
        j.connect_cells(i, -1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 1




for i in rec_neurons3:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:90]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23=count_links_23+2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:5]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_23 = count_links_23 + 2
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_links_23 = count_links_23 + 1

    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:20]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:20]:
        j.connect_cells(i, 1)
        count_in_23 = count_in_23 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:10]:
        j.connect_cells(i, -1)
        count_in_23 = count_in_23 + 1


dg={}
dg['2-3'] = []
dg['2-3'].append({
    'count_cells' : [count_cells_23],
    'count_links' : [count_links_23],
    'count_in' : [count_in_23]
    })
logging.info('level 2-3')
#_________________________ 4 (400-700)______________________________
count_cells_4=Nspinstel4+NtuftIB5
count_links_4=0
count_in_4=0

for i in rec_neurons4:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:3]:
        j.connect_cells(i, 0)
        count_in_4=count_in_4+1
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:20]:
        j.connect_cells(i, 1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_4 = count_in_4 + 2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:1]:
        j.connect_cells(i, 0)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons1)
    for j in rec_neurons1[0:20]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons2)
    for j in rec_neurons2[0:5]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:30]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_4 = count_links_4 + 2
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:3]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_links_4 = count_links_4 + 2



for i in rec_neurons5:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:60]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_4=count_in_4+2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:20]:
        j.connect_cells(i, 1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_4 = count_in_4 + 2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:3]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_4 = count_in_4 + 2
    random.shuffle(rec_neurons2)
    for j in rec_neurons2[0:5]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons8)
    for j in rec_neurons8[0:20]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1)
        count_in_4 = count_in_4 + 1
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:50]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_links_4 = count_links_4 + 2
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 0)
        count_links_4 = count_links_4 + 1




dg['4'] = {
    'count_cells' : [count_cells_4],
    'count_links' : [count_links_4],
    'count_in' : [count_in_4]
    }
logging.info('level 4')
#_____________________5 (700-1200)___________________________________
count_cells_5=NtuftRS5 + Nbask56
count_links_5=0
count_in_5=0


for i in rec_neurons6:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:60]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_5=count_in_5+2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:10]:
        j.connect_cells(i, 1)
        count_links_5 = count_links_5 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_5 = count_in_5 + 2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:3]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_5 = count_in_5 + 2
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, -1)
        count_links_5 = count_links_5 + 1
    random.shuffle(rec_neurons8)
    for j in rec_neurons8[0:5]:
        j.connect_cells(i, -1)
        count_links_5 = count_links_5 + 1
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_in_5 = count_in_5 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1)
        count_in_5 = count_in_5 + 1
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:20]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_5 = count_in_5 + 2
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:20]:
        j.connect_cells(i, 0)
        count_in_5 = count_in_5 + 1




for i in rec_neurons7:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:30]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_5=count_in_5+2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:20]:
        j.connect_cells(i, 1)
        count_links_5 = count_links_5 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_5 = count_in_5 + 2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:3]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_5 = count_in_5 + 2
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_in_5 = count_in_5 + 1
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, -1)
        count_links_5 = count_links_5 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1)
        count_in_5 = count_in_5 + 1
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:20]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_5 = count_in_5 + 2
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_5 = count_in_5 + 2

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
    for j in rec_neurons13[0:30]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_56=count_in_56+2
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, 1)
        count_in_56 = count_in_56 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_56 = count_in_56 + 2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:3]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_56 = count_in_56 + 2
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_56 = count_in_56 + 2
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:20]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_56 = count_in_56 + 2
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, -1)
        count_in_56 = count_in_56 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1)
        count_links_56 = count_links_56 + 1




for i in rec_neurons9:
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:30]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_56=count_in_56+2
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, 1)
        count_in_56 = count_in_56 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:10]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_56 = count_in_56 + 2
    random.shuffle(rec_neurons12)
    for j in rec_neurons12[0:3]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_56 = count_in_56 + 2
    random.shuffle(rec_neurons4)
    for j in rec_neurons4[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_56 = count_in_56 + 2
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:20]:
        j.connect_cells(i, 0)
        j.connect_cells(i, 1)
        count_in_56 = count_in_56 + 2
    random.shuffle(rec_neurons7)
    for j in rec_neurons7[0:20]:
        j.connect_cells(i, -1)
        count_in_56 = count_in_56 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1)
        count_links_56 = count_links_56 + 1


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
    random.shuffle(rec_neurons13)
    for j in rec_neurons13[0:3]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_6=count_in_6+2
    random.shuffle(rec_neurons6)
    for j in rec_neurons6[0:20]:
        j.connect_cells(i, 1)
        count_in_6 = count_in_6 + 1
    random.shuffle(rec_neurons10)
    for j in rec_neurons10[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_links_6 = count_links_6 + 2
    random.shuffle(rec_neurons7)
    for j in rec_neurons6[0:20]:
        j.connect_cells(i, -1)
        count_in_6 = count_in_6 + 1
    random.shuffle(rec_neurons8)
    for j in rec_neurons8[0:5]:
        j.connect_cells(i, -1)
        count_in_6 = count_in_6 + 1
    random.shuffle(rec_neurons9)
    for j in rec_neurons9[0:20]:
        j.connect_cells(i, -1)
        count_in_6 = count_in_6 + 1
    random.shuffle(rec_neurons12)
    for j in rec_neurons13[0:1]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_6 = count_in_6 + 2
    random.shuffle(rec_neurons3)
    for j in rec_neurons3[0:20]:
        j.connect_cells(i, -1)
        count_in_6 = count_in_6 + 1
    random.shuffle(rec_neurons5)
    for j in rec_neurons5[0:20]:
        j.connect_cells(i, 1)
        j.connect_cells(i, 0)
        count_in_6 = count_in_6 + 2

dg['6 (1200-1700)'] = {
    'count_cells' : [count_cells_6],
    'count_links' : [count_links_6],
    'count_in' : [count_in_6]
    }
logging.info('level 6')
logging.info('done')


alpha = alpha1
tort = tort1


time = h.Vector().record(h._ref_t)

ecs = rxd.Extracellular(-Lx / 2.0, -Ly / 2.0,
                        -Lz / 2.0, Lx / 2.0, Ly / 2.0, Lz / 2.0, dx=(20, 20, 20),  # dx - скорость распространнения в разные стороны - различны по осям
                        volume_fraction=alpha, tortuosity=tort)


k = rxd.Species(ecs, name='k', d=2.62, charge=1, initial= 3.5,
                ecs_boundary_conditions=3.5)

na = rxd.Species(ecs, name='na', d=1.78, charge=1, initial=142,
                 ecs_boundary_conditions=142)

logging.info('add stims')
stims=[]
for i in range(0,200):
    for j in range(0,30):
        stim = h.NetStim()
        stim.number = 1
        stim.start = 5#random.randint(5,15)
        ncstim = h.NetCon(stim, rec_neurons4[i].synlistexE[j])
        ncstim.delay = 1#random.randint(1,5)
        ncstim.weight[0] = 1
        stims.append(ncstim)
        stims.append(stim)

#kecs = h.Vector()
#kecs.record(k[ecs].node_by_location(0, 0, 0)._ref_value)


# initialize and set the intracellular concentrations
logging.info('initialize-start')
h.finitialize()
pc.psolve(100)
logging.info('initialize-go')
#print(len(stims))



'''
df = pd.DataFrame({
    'id' : [j.id for i in cell for j in i],
    'name' : [j.name for i in cell for j in i],
    'number' : [j.number for i in cell for j in i],
    'count' : [j.count for i in cell for j in i],
    'cells' : [j.cells for i in cell for j in i]
    })
df.to_csv(os.path.join(outdir,'data_cells.csv'))
'''



#dg.to_csv(os.path.join(outdir,'info.csv'))


def progress_bar(tstop, size=40):
    """ report progress of the simulation """
    prog = h.t / float(tstop)
    fill = int(size * prog)
    empt = size - fill
    progress = '#' * fill + '-' * empt
    sys.stdout.write('[%s] %2.1f%% %6.1fms of %6.1fms\r' % (progress, 100 * prog, pc.t(0), tstop))
    sys.stdout.flush()
'''
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
    fig.add_trace(go.Scatter(y=cell.dendV1, x=time, mode='lines', name='dendrite1'))
    fig.add_trace(go.Scatter(y=cell.dendV2, x=time, mode='lines', name='dendrite2'))
    fig.add_trace(go.Scatter(y=cell.dendV3, x=time, mode='lines', name='dendrite3'))
    fig.add_trace(go.Scatter(y=cell.dendV4, x=time, mode='lines', name='dendrite4'))
    fig.add_trace(go.Scatter(y=cell.v_vec, x=time, mode='lines', name='v'))
    fig.update_layout(title='Voltage of Neuron %i' % cell.id,
                   xaxis_title='ms',
                   yaxis_title='mV')
    fig.write_html(os.path.join(k_na_dir, 'spike%i.html' % i ))


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
'''
h.dt = 0.1

def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')
        for line in data:
            writer.writerow(line)


def run(tstop):
    volt = []
    
    while pc.t(0) <= tstop:
        if int(pc.t(0)*10) % 10 == 0 and pcid == 0:
            logging.info('time: '+ int(pc.t(0)))
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

            
        #if pcid == 0: progress_bar(tstop)
        pc.psolve(pc.t(0) + h.dt)
        
    if pcid == 0:
        logging.info('Simulation complete.')
        #progress_bar(tstop)
       # for i in [0, 108] :
            #plot_spike(rec_neurons[i], time , i)
        #print("\nSimulation complete. Plotting membrane potentials")
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
            #plot_spike(n, time, n.number)


    #pout = open(os.path.join(outdir, "membrane_potential_%i.pkl" % pcid), 'wb')
    #pickle.dump([soma, dend, pos, data], pout)
    #pout.close()
    #d3_data = pd.DataFrame(dict(x=x_pos, y=y_pos, z=z_pos, id=id_color, name=listname))
    pc.barrier()
    if pcid == 0:
        logging.info('write to file -info.json')
        with open(os.path.join(outdir, 'info.json'), 'w') as outfile:
            json.dump(dg, outfile)
        #plot_3D_data(d3_data)
        logging.info("write to file - volt.csv")
        csv_writer(volt, os.path.join(outdir, 'volt.csv'))
        #voltToCSV = pd.DataFrame(volt)
        #voltToCSV.to_csv(os.path.join(outdir, 'volt.csv'))
        #plot_volt(volt)
        #plot_rec_neurons()

    pc.done()
    h.quit()


run(100)