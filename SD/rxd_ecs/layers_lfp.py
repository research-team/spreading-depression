import matplotlib.pyplot as plt
import numpy as np
import scipy.io
from pylab import *
import seaborn as sns
from scipy.stats import norm, kstest

filepath = r'C:\Users\User\OneDrive\Рабочий стол\2011 may 03 P32 BCX rust\2011_05_03_0003.mat'
file=""

color = ['red', 'blue', 'yellow', 'black', 'gray', 'cyan', 'magenta']

def load_data(filepath):
    mat = scipy.io.loadmat(filepath)
    spks = mat['lfp']
    return spks

data = load_data(filepath)
data = np.moveaxis(data, [0, 1, 2], [2, 1,0])
data_0=[]
yx=0
for era, items in enumerate(data):
    if era<=4:
        for channel, varb in enumerate(items):
            plt.plot(np.array(items[0])+yx*850)
            yx+=1


plt.show()


























# import matplotlib.pyplot as plt
# import numpy as np
# import scipy.io
# from pylab import *
# import os
# import seaborn as sns
# from scipy.stats import norm, kstest, ks_2samp
#
# filepath = r'C:\Users\User\OneDrive\Рабочий стол\2011 may 03 P32 BCX rust\2011_05_03_0003.mat'
# file=""
#
# def load_data(filepath):
#     mat = scipy.io.loadmat(filepath)
#     spks = mat['spks']
#     return spks
# data = load_data(filepath)
# data = np.moveaxis(data, [0, 1], [1, 0])
# data_3= data[29]
# # print(data)
# layer_13=[]
# layer_12_14=[]
# layer_9_11=[]
# layer_8_10=[]
# layer_6_7=[]
# layer_3_4_5=[]
# layer_0_1_2=[]
#
# for b, items in enumerate(data_3):
#     if b==13:
#         layer_13.append(items[0])
#     if b==12 or b==14:
#         layer_12_14.append(items[0])
#     if b==9 or b==11:
#         layer_9_11.append(items[0])
#     if b==8 or b==10:
#         layer_8_10.append(items[0])
#     if b==6 or b==7:
#         layer_6_7.append(items[0])
#     if b==3 or b==4 or b==5:
#         layer_3_4_5.append(items[0])
#     if b==0 or b==1 or b==2:
#         layer_0_1_2.append(items[0])
#
#
# color = ['red', 'blue', 'yellow', 'black', 'green', 'cyan', 'magenta']
# fig, ax = plt.subplots()
# data_ = []
# layers=[]
# with os.scandir(r'C:\Users\User\OneDrive\Рабочий стол\последние результаты') as it:
#     for entry in it:
#         if entry.name.endswith(".txt") and entry.is_file():
#             with open(entry.path, 'r') as f:
#                 layer = str(str(entry.name).rsplit('_')[1])
#                 layers.append(layer)
#                 spiketime = []
#                 for line in f:
#                     line = line.rstrip('\n\r')
#                     spiketime.append(float(line))
#                 data_.append((layer,spiketime))
# all_layers=[]
# layer_23=[]
# layer_4=[]
# layer_5=[]
# layer_56=[]
# layer_6=[]
# for layer, spks in data_:
#     # print(layer)
#     '''L-23'''
#     if layer=="1" or layer=="2" or layer=="3" or layer=="12" or layer=="13":
#         layer_23.append(spks)
#     '''L-4'''
#     if layer=="4" or layer=="16":
#         layer_4.append(spks)
#     '''L-5'''
#     if layer=="5" or layer=="6":
#         layer_5.append(spks)
#     '''L-56'''
#     if layer=="7" or layer=="8" or layer=="9":
#         layer_56.append(spks)
#     '''L-6'''
#     if layer=="10":
#         layer_6.append(spks)
#
# time=[]
# with open(r'C:\Users\User\OneDrive\Рабочий стол\time.txt') as file:
#     for i in file:
#         time.append((float(i)))
#
#
# bio_data = np.concatenate(layer_0_1_2, axis=None)
# gen_data = np.concatenate(layer_23, axis=None)
# ks_test = ks_2samp(bio_data, gen_data)
# # print(ks_test)
# gen_data.sort()
# ISIs=np.diff(gen_data)
# ISIs_sort=set(ISIs)
# plt.plot(ISIs)
#
# plt.show()
#
#
#
#
# # time_xticks=[]
# # time_xticks_label=[]
# # for i in range(0, len(ISIs)):
# #     time_xticks.append(ISIs[i])
# #     time_xticks_label.append(round(time[i]))
# # plt.xticks(time_xticks, time_xticks_label)
# # def compare_spks(bio_layer, generated_layer):
# #     bio_data=np.concatenate(bio_layer, axis=None)
# #     gen_data=np.concatenate(generated_layer, axis=None)
# #     ISIs_bio=np.diff(bio_data)
# #     ISIs_gen=np.diff(gen_data)
# #     ks_test=ks_2samp(ISIs_bio, ISIs_gen)
# #     print(ks_test)
# #
# # def compare_voltage(bio_layer, generated_layer):
# #     pass
# # compare_voltage(layer_0_1_2, layer_23)
#
# # compare_spks(layer_0_1_2, layer_23)