import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import csv
import  math

hdf5_files=''
coordinates_file=''


def load_voltages(path):
    vol_group = {}
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.endswith(".hdf5") and entry.is_file():
                file_name = os.path.splitext(entry.name)[0]
                with h5py.File(entry.path, 'r') as f:
                    vol_group[file_name] = np.array(f[list(f.keys())[0][:]])
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
    '''
    Сенсоры на L23: 1, 2, 3
    Сенсоры на L4: 4, 5, 6
    Сенсоры на L5: 7, 8, 9
    Сенсоры на L56: 10, 11
    Сенсоры на L6: 12, 13, 14
    Сенсоры на tf: 15, 16
    '''
    # sensors = {'1': [100, 100, -700], '2': [100, 100, -650], '3':[100, 100, -490], '4':[100, 100, -400], '5':[100, 100, -300], '6':[100, 100, -250],
    #            '7':[100, 100, -100], '8':[100, 100, 50], '9': [100, 100, 100], '10':[100, 100, 250], '11':[100, 100, 330], '12':[100, 100, 400],
    #            '13':[100, 100, 550], '14':[100, 100, 700], '15':[100, 100, 1120], '16':[100, 100, 1270]}
    sensors = [[1, 100, 100, -700], [2, 100, 100, -650], [3, 100, 100, -490], [4, 100, 100, -400],
               [5, 100, 100, -300], [6, 100, 100, -250], [7, 100, 100, -100], [8, 100, 100, 50],
               [9, 100, 100, 100], [10, 100, 100, 250], [11, 100, 100, 330], [12, 100, 100, 400],
               [13, 100, 100, 550], [14, 100, 100, 700], [15, 100, 100, 1120], [16, 100, 100, 1270]]
    fraction_dict = {}
    for sensor in sensors:
        sensor_number = sensor[0]
        sX = sensor[1]
        sY = sensor[2]
        sZ = sensor[3]
        result = []
        for data in coords:
            dkey = data[0]
            x = float(data[1])
            y = float(data[2])
            z = float(data[3])
            summ = 0
            for key, value in voltages.items():
                if key == dkey:
                    square_of_distance = math.sqrt((sX - x) ** 2 + (sY - y) ** 2 + (sZ - z) ** 2)
                    for i in value:
                        fraction = i / square_of_distance
                        summ+=fraction
                    result.append(summ)
        fraction_dict[str(sensor_number)] = np.array(result)
    return fraction_dict

def calculation_simple_LFP(fraction):
    result = {}
    res=[]
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

    with h5py.File('', 'w') as hf:
        group = hf.create_group('values')
        for key, value in lfp.items():
            group[key] = value


if __name__ == "__main__":
    main()