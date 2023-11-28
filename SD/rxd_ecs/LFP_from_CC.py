import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import csv
import  math

hdf5_files='D:/results1'
coordinates_file='D:/results1/cord.csv'


def load_voltages(path):
    vol_group = {}
    voltages = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.endswith(".hdf5") and entry.is_file():
                with h5py.File(entry.path, 'r') as f:
                    vol_group[entry.name] = np.array(f[list(f.keys())[0][:]])
    return vol_group

def load_coordinates(path):
    coordinates = []
    with open(path, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            coordinates.append(row)
    coordinates.sort()
    return coordinates


def calc_lfp(voltages, coords):
    '''Допустим электрод находится на x = 100, y = 100, z = 100'''
    Xe = 100
    Ye = 100
    Ze = 100
    result = []
    fraction_dict = {}
    for data in coords:
        dkey = data[0]
        x = float(data[1])
        y = float(data[2])
        z = float(data[3])
        res = 0
        for key, values in voltages.items():
            vkey = key[0:30]
            fraction_dict[vkey] = np.array(result)
            if (21 <= len(key) < 27) and (dkey[0:21] == key[0:21]) :
                square_of_distace = math.sqrt((Xe - x) ** 2 + (Ye - y) ** 2 + (Ze - z) ** 2)
                for i in values:
                    fraction = i / square_of_distace
                    res += fraction
                    result.append(res)
                    result.append(fraction)
            if (len(key) > 27) and (dkey[0:30] == vkey):
                square_of_distace = math.sqrt((Xe - x) ** 2 + (Ye - y) ** 2 + (Ze - z) ** 2)
                for i in values:
                    fraction = i / square_of_distace
                    res += fraction
                    result.append(res)
                    result.append(fraction)
    return fraction_dict


def calculation_simple_LFP(fraction):
    result = {}
    const = 1 / (4 * math.pi)
    for key, value in fraction.items():
        lfp = const * value
        result[key] = np.array(lfp)
    return result


def main():
    voltages = load_voltages(hdf5_files)
    coordinates = load_coordinates(coordinates_file)
    fraction = calc_lfp(voltages, coordinates)
    lfp = calculation_simple_LFP(fraction)

    with h5py.File('D:/lfps/lfp3.hdf5', 'w') as hf:
        group = hf.create_group('values')
        for key, value in lfp.items():
            group[key] = value


if __name__ == "__main__":
    main()