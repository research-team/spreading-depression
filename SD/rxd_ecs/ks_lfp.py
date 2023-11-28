import h5py
import os
import numpy as np

file = 'D:/results1/lfp.hdf5'


def load_cc_lfp(filepath):
    lfp_cc = {}
    with h5py.File(filepath, 'r') as file:
        def traverse(group, prefix=""):
            for key in group.keys():
                item = group[key]
                path = f"{prefix}/{key}" if prefix else key
                if isinstance(item, h5py.Group):
                    traverse(item, path)
                elif isinstance(item, h5py.Dataset):
                    lfp_cc[path] = item[()]
        traverse(file)
    return lfp_cc

def main():
    lfp_cc = load_cc_lfp(file)
    print(lfp_cc)