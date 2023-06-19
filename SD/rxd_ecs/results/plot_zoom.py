import fnmatch
import os

import sys

import bokeh

import h5py

bokeh.sampledata.download()

from bokeh.plotting import figure, output_file, show

sys.path.append('../')
my_path = os.path.abspath('')

themes = 'light_minimal'


def read():
    volt_data = []
    lab_line = []

    for file in fnmatch.filter(os.listdir('.'), 'voltage' + '*.hdf5'):
        with h5py.File(file) as f:
            id = str(file).rsplit('_')[1]
            if id[-1] == 'e':
                id = int(id.rsplit('e')[0])
                lab_line.append((id, 1))
            else:
                id = int(id)
                lab_line.append((id, 0))

            vol_group = list(f.keys())[0]
            data_y = list(f[vol_group])
            volt_data.append((id, data_y))

    data_time = []

    with open('time_e.txt', 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.rstrip('\n\r')
            data_time.append(float(line))
    return volt_data, lab_line, data_time


def draw_motifs(data_x, volt_data, par, lab_line, name, type):
    # ls = [[13, 10, 2], [13, 6, 2], [12, 6, 2], [12, 6, 3], [12, 10, 3], [12, 10, 2]]
    # ls = [[14], [14, 4, 10], [4, 12], [12, 10], [10, 15]]
    # ls = [[14], [14, 4, 10], [4],
    # [4, 16], [4, 16, 12], [4, 16, 12 ],[4, 12, 10, 14]]

    # ls = [[14, 4, 16, 12, 10]]  # seque
    ls = [[13, 2, 10], [12, 2, 6], [13, 2, 6], [12, 3, 6], [12, 10, 3], [12, 10, 2]]  # motifs
    for i, j in enumerate(ls):
        fig = figure(x_axis_label='time (ms)', y_axis_label='V (mV)')
        for id, k in enumerate(j):
            for id_y, lab in zip(volt_data, lab_line):
                if id_y[0] == k:
                    y = id_y[1]
                    if type == 0:
                        if lab[1] == 0:
                            output_file(i.__str__() + f'{name}.html')
                            fig.line(data_x, y, line_width=2, color=par.get(id_y[0])[1],
                                     legend_label=par.get(id_y[0])[0])
                            break
                    elif type == 1:
                        if lab[1] == 1:
                            output_file(i.__str__() + f'{name}_e.html')
                            fig.line(data_x, y, line_width=2, color=par.get(id_y[0])[1],
                                     legend_label=par.get(id_y[0])[0] + '_e')
                        break
                    else:
                        output_file(par.get(id_y[0])[0] + '_with_e.html')
                        if lab[1] == 0:
                            fig.line(data_time, y, line_width=2, color=par.get(id_y[0])[1],
                                     legend_label=par.get(id_y[0])[0])
                        if lab[1] == 1:
                            fig.line(data_time, y, line_width=2, color='red',
                                     legend_label=par.get(id_y[0])[0] + '_e')
        show(fig)


def draw(volt_data, par, lab_line, data_time, type):
    # ls1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16]
    #ls1 = [4, 10]
    ls1 = [12, 16]
    for i, j in enumerate(ls1):
        figur = figure(x_axis_label='time (ms)', y_axis_label='V (mV)')
        for id_y, lab in zip(volt_data, lab_line):
            if id_y[0] == j:
                if type == 0:
                    if lab[1] == 0:
                        output_file(par.get(id_y[0])[0] + '.html')
                        figur.line(data_time, id_y[1], line_width=2, color=par.get(id_y[0])[1],
                                   legend_label=par.get(id_y[0])[0])
                elif type == 1:
                    if lab[1] == 1:
                        output_file(par.get(id_y[0])[0] + '_e.html')
                        figur.line(data_time, id_y[1], line_width=2, color=par.get(id_y[0])[1],
                                   legend_label=par.get(id_y[0])[0] + '_e')
                else:
                    output_file(par.get(id_y[0])[0] + '_with_e.html')
                    if lab[1] == 0:
                        figur.line(data_time, id_y[1], line_width=2, color=par.get(id_y[0])[1],
                                   legend_label=par.get(id_y[0])[0])
                    if lab[1] == 1:
                        figur.line(data_time, id_y[1], line_width=2, color='red',
                                   legend_label=par.get(id_y[0])[0] + '_e')

        show(figur)


if __name__ == '__main__':
    volt_data, lab_line, data_time = read()
    par = {1: ["Bask23", "#1a7ef2"],
           2: ["Axax23", "#42d4f4"],
           3: ["LTS23", "#3a0ca3"],
           4: ["Spinstel4", "#ffba00"],
           5: ["TuftIB5", "#3cb44b"],
           6: ["TuftRS5", "#bfef45"],
           7: ["Bask56", "#c8b6ff"],
           8: ["Axax56", "#f032e6"],
           9: ["LTS56", "#911eb4"],
           10: ["NontuftRS6", "#18502b"],
           12: ["SyppyrFRB", "#f58231"],
           13: ["SyppyrRS", "#e6194B"],
           14: ["TCR", "#ffccd5"],
           15: ["nRT", "#9d4edd"],
           16: ["LTS4", "#a6e1fa"],
           }

    # draw(volt_data, par, lab_line, data_time, 0)
    # draw(volt_data, par, lab_line, data_time, 1)

    # draw_motifs(data_time, volt_data, par, lab_line, 'motifs', 0)
    # draw_motifs(data_time, volt_data, par, lab_line, 'motifs', 1)
