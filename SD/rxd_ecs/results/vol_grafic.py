import os
import h5py
import numpy as np
import matplotlib.pyplot as plt


vol_group = {}
with os.scandir(r'...') as it:
    for entry in it:
        if entry.name.endswith(".hdf5") and entry.is_file():
            with h5py.File(entry.path, 'r') as f:
                vol_group[entry.name] = np.array(f[list(f.keys())[0][:]])
                list_keys = list(vol_group.keys())
                list_keys.sort()
                yx = 1
                y_ticks_list = []
                fig,ax=plt.subplots()
                for i in list_keys:
                    yx += 1
                    plt.plot(np.array(vol_group[i])+yx*(1e-8))
                    y_ticks_list.append(i[8:11])
                    ax.set_yticklabels(np.array(y_ticks_list))
                    #plt.yticks(np.array(y_ticks_list).item())
                plt.show()



