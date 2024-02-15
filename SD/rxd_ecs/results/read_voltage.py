
import h5py
import matplotlib.pyplot as plt
import sys
import os
import fnmatch
import random
# path = "C://Users/Алина/IdeaProjects/spreading-depression/SD/rxd_ecs/testRes/results/voltage_L4 spiny stellate.hdf5"
sys.path.append('../')
my_path = os.path.abspath('')


volt_data = []

for file in fnmatch.filter(os.listdir('.'), '*.hdf5'):

    with h5py.File(file) as f:
        id = str(file).rsplit('_')[1]
        vol_group = list(f.keys())[0]
        data = list(f[vol_group])
        volt_data.append((id, data))


fig = plt.figure()
ls = [[13, 10, 2], [13, 6, 2], [12, 6, 2], [12, 6, 3], [12, 10, 3], [12, 10, 2]]
for i, j in enumerate(ls):
    for k in j:
        for id_v in volt_data:
            if id_v[0] == k.__str__():
                plt.plot(id_v[1])
                break
    fig.savefig(os.path.join(my_path, i.__str__() + 'motif.png'))
    fig = plt.figure()

plt.show()
