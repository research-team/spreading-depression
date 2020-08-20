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
outdir = os.path.abspath('tests/892_tW')


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

rec_neurons16=[]
for i in range(0,Nbask4):
    rec_neurons4.append(Bask4(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(400,700), i+num))
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
for i in range(0,NtuftIB5):
    rec_neurons5.append(TuftIB5(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(700,900), i+num))
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

NTCR = 100
NnRT = 100
num +=NTCR
num +=NnRT

rec_neurons14=[]
for i in range(0,NTCR):
    rec_neurons14.append(TCR(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(4900,5200-somaR), i+num))
    data['cells'].append({
        'name': rec_neurons14[i].name,
        'id': rec_neurons14[i].id,
        'num': rec_neurons14[i].number,
        'x': rec_neurons14[i].x,
        'y': rec_neurons14[i].y,
        'z': rec_neurons14[i].z
    })

rec_neurons15=[]
for i in range(0,NTCR):
    rec_neurons15.append(nRT(
    random.uniform(somaR,Lx-somaR),
    random.uniform(somaR,Ly-somaR),
    random.uniform(5000,5200-somaR), i+num))
    data['cells'].append({
        'name': rec_neurons15[i].name,
        'id': rec_neurons15[i].id,
        'num': rec_neurons15[i].number,
        'x': rec_neurons15[i].x,
        'y': rec_neurons15[i].y,
        'z': rec_neurons15[i].z
    })

#2710
cell=[rec_neurons12, rec_neurons13, rec_neurons1, rec_neurons2, rec_neurons3, rec_neurons4, rec_neurons5, rec_neurons6, rec_neurons7, rec_neurons8, rec_neurons9, rec_neurons10, rec_neurons14, rec_neurons15, rec_neurons16 ]
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
count_cells_4=Nspinstel4+Nbask4
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

def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = ["t",
                             "x",
                             "y",
                             "z",
                             "v",
                             "id",
                             "num",
                            "name"])
        for line in data:
            writer.writerow(line)


def run(tstop):
    volt = []
    
    while pc.t(0) <= tstop:
        if int(pc.t(0) * 10) % 10 == 0 and pcid == 0:
            print('time: ' , int(pc.t(0)))
            for j in cell:
                for n in j:
                    volt.append({"t" : int(pc.t(0)),
                                    "x" : n.x,
                                    "y" : n.y,
                                    "z" : n.z,
                                    "v" : n.somaV[-1],
                                    "id": n.id,
                                    "num": n.number,
                                    "name": n.name})


        pc.psolve(pc.t(0) + h.dt)
        


    logging.info('Simulation complete.')
    pc.barrier()
    if pcid == 0:
        logging.info('write to file -info.json')
        with open(os.path.join(outdir, 'info.json'), 'w') as outfile:
            json.dump(dg, outfile)

        logging.info("write to file - volt.csv")
        csv_writer(volt, os.path.join(outdir, 'volt.csv'))


        pc.runworker()
        pc.done()
        h.quit()


run(100)