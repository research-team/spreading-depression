import h5py
import matplotlib.pyplot as plt
import sys
import os
import fnmatch
# path = "C://Users/Алина/IdeaProjects/spreading-depression/SD/rxd_ecs/testRes/results/voltage_L4 spiny stellate.hdf5"
sys.path.append('../')
my_path = os.path.abspath('')
from bokeh.plotting import figure, output_file, show


output_file('Vol.html')
fig = figure()
for file in fnmatch.filter(os.listdir('.'), '*.hdf5'):
    with h5py.File(file) as f:
        #data = [v[:] for v in file.values()]
        id = str(file).rsplit('_')[1]
        name = str(file).rsplit('_')[2]
        vol_group=list(f.keys())[0]
        data=list(f[vol_group])
        fig.line(data)
        # fig.savefig(os.path.join(my_path, id + '_' + name + '.png'))
show(fig)