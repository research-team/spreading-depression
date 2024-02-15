import csv
import os
import random
import sys

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

sys.path.append('../')
my_path = os.path.abspath('')

nodelist = [("TCR", "#ffccd5"), ("TuftRS5", "#bfef45"), ("TuftIB5", "#3cb44b"),
            ("Spinstel4", "#ffba00"), ("NontuftRS6", "#18502b"), ("SyppyrFRB", "#f58231"),
            ("SyppyrRS", "#e6194B"),
            ("nRT", "#9d4edd"), ("Bask56", "#c8b6ff"), ("Axax56", "#f032e6"),
            ("Bask23", "#1a7ef2"), ("Axax23", "#42d4f4"), ("LTS4", "#a6e1fa"), ("LTS56", "#911eb4"),
            ("LTS23", "#3a0ca3")]


def read_csv():
    color_dict = {'0': '#fb6107', '1': 'r', '-1': 'b'}
    color = []
    from_cell = []
    to_cell = []
    weight = []

    with open('connections.csv') as File:
        reader = csv.reader(File, delimiter='\t')
        for i, row in enumerate(reader):
            if i < 3:
                continue
            color.append(row[0])
            from_cell.append(row[1])
            to_cell.append(row[2])
            weight.append(row[5])

    for i, v in enumerate(color):
        color[i] = color_dict[v]

    for i, v in enumerate(weight):
        weight[i] = float(v)

    return from_cell, to_cell, color, weight


def add_n(nodelist, G):
    """----adding nodes parameters"""
    for node in enumerate(nodelist):
        G.add_node(node[1][0], color=node[1][1],
                   bbox=dict(facecolor=node[1][1], edgecolor='black', boxstyle='round,pad=0.2'))


def add_e(from_cell, to_cell, color, weight, G, color_edge):
    """ ------adding all connections----- """
    for i in range(len(from_cell)):
        if color_edge == color[i]:
            G.add_edge(from_cell[i],
                       to_cell[i],
                       color=color[i],
                       weight=weight[i] / np.mean(weight))
        else:
            continue


def add_e_if(from_cell, to_cell, color, weight, G, edgelist, type):
    """ ------adding single cycle connections----- """
    for i in range(len(from_cell)):
        for j in enumerate(edgelist):
            if j[1][0] == from_cell[i] and j[1][1] == to_cell[i]:
                if color[i] == '#fb6107':
                    continue
                if type == 1:
                    w = weight[i]
                else:
                    w = weight[i] / np.mean(weight)
                G.add_edge(from_cell[i],
                           to_cell[i],
                           color=color[i],
                           weight=w)


def add_pos(G):
    """----adding nodes positions"""
    G.nodes["TCR"]['pos'] = (-10, 0)
    G.nodes["nRT"]['pos'] = (10, 0)
    G.nodes["NontuftRS6"]['pos'] = (0, 20)
    G.nodes["LTS56"]['pos'] = (20, 40)
    G.nodes["Bask56"]['pos'] = (-20, 40)
    G.nodes["Axax56"]['pos'] = (0, 40)
    G.nodes["TuftRS5"]['pos'] = (-10, 60)
    G.nodes["TuftIB5"]['pos'] = (10, 60)
    G.nodes["Spinstel4"]['pos'] = (-15, 80)
    G.nodes["LTS4"]['pos'] = (20, 80)
    G.nodes["SyppyrRS"]['pos'] = (-40, 100)
    G.nodes["SyppyrFRB"]['pos'] = (-20, 100)
    G.nodes["Axax23"]['pos'] = (0, 100)
    G.nodes["Bask23"]['pos'] = (20, 100)
    G.nodes["LTS23"]['pos'] = (40, 100)


def g_draw(A, G, N, alpha_A, alpha_G, alpha_N, alpha_motif, G1, new_graph, id, name):
    if alpha_motif == 1:
        alpha_A = 0.1
        alpha_G = 0.1
        alpha_N = 0.1

    if new_graph == 1:
        alpha_A = 0.05
        alpha_G = 0.05
        alpha_N = 0.05

    graphs = [A, G, N]
    ar_st = "->"
    alpha_graphs = [alpha_A, alpha_G, alpha_N]
    con_style = ['arc3, rad=0.3', 'arc3, rad=0.5', 'arc3, rad=-0.3']

    fig = plt.figure(figsize=(10, 10))
    draw_elements()
    if name is None:
        for graph, con_st, alpha in zip(graphs, con_style, alpha_graphs):
            graph_draw(graph, con_st, alpha, ar_st, 0)
    else:
        if name == 'AMPA':
            graph_draw(A, con_style[0], alpha_A, ar_st, 0)
        elif name == 'GABA':
            graph_draw(G, con_style[1], alpha_G, ar_st, 0)
        elif name == 'NMDA':
            graph_draw(N, con_style[2], alpha_N, ar_st, 0)
        fig.savefig(os.path.join(my_path, f'connects_{name}.svg'))
        fig.savefig(os.path.join(my_path, f'connects_{name}.png'))

    if alpha_motif == 1:
        motif_draw(N, 2, 5)
        fig.savefig(os.path.join(my_path, 'connects_with_motif_3.svg'))
        fig.savefig(os.path.join(my_path, 'connects_with_motif_3.png'))
    elif G1 is not None:
        graph_draw(G1, 'arc3, rad=-0.1', 1, ar_st, 2)
        fig.savefig(os.path.join(my_path, f'connects_{id}.svg'))
        fig.savefig(os.path.join(my_path, f'connects_{id}.png'))
    else:
        fig.savefig(os.path.join(my_path, 'connects_new.svg'))
        fig.savefig(os.path.join(my_path, 'connects_new.png'))
    plt.show()


def graph_draw(graph, con_st, alpha, arrowstyle, type):
    nx.draw(graph,
            arrows=True,
            arrowstyle=arrowstyle,
            node_size=500,
            node_shape='s',
            pos=dict((n, graph.nodes[n]["pos"]) for n in graph.nodes()),
            node_color=nx.get_node_attributes(graph, 'color').values(),
            width=[float(v['weight']) for (r, c, v) in graph.edges(data=True)],
            edge_color=nx.get_edge_attributes(graph, 'color').values(),
            connectionstyle=con_st,
            alpha=alpha
            )
    labels = {node: f'{node}' for node in G.nodes()}
    for node, color in zip(G.nodes(), nx.get_node_attributes(graph, 'color').values()):
        bbox_props = dict(facecolor=color, edgecolor='black', boxstyle='round')
        font_color = 'black'
        if node == 'LTS23' or node == 'LTS56' or node == 'nRT' or node == 'NontuftRS6':
            font_color = 'white'
        if type != 1:
            alpha = None
        nx.draw_networkx_labels(G, dict((n, graph.nodes[n]["pos"]) for n in graph.nodes()),
                                {node: labels[node]}, font_color=font_color, font_size=11,
                                bbox=bbox_props, alpha=alpha)


def motif_draw(G, id_1, id_2):
    edgelist = [[("Axax23", "SyppyrRS"), ("Axax23", "NontuftRS6"), ("SyppyrRS", "NontuftRS6")],
                [("Axax23", "SyppyrRS"), ("Axax23", "TuftRS5"), ("SyppyrRS", "TuftRS5")],
                [("Axax23", "SyppyrFRB"), ("Axax23", "NontuftRS6"), ("SyppyrFRB", "NontuftRS6")],
                [("Axax23", "SyppyrFRB"), ("Axax23", "TuftRS5"), ("SyppyrFRB", "TuftRS5")],
                [("LTS23", "SyppyrFRB"), ("LTS23", "TuftRS5"), ("SyppyrFRB", "TuftRS5")],
                [("LTS23", "SyppyrFRB"), ("LTS23", "NontuftRS6"), ("SyppyrFRB", "NontuftRS6")]
                ]
    colors_1 = ['purple', 'purple', 'purple']
    weights = [5, 5, 5]
    colors_2 = ['green', 'green', 'green']
    from_cc = []
    to_cc = []
    for i, edge in enumerate(edgelist):
        if i == id_1 or i == id_2:
            for k in edge:
                from_cc.append(k[0])
                to_cc.append(k[1])
            if i < 3:
                M = create_graph(1, nodelist, from_cc, to_cc, colors_1, weights, 'purple', True, edge)
                con_st = 'arc3, rad=0.2'
            else:
                M = create_graph(1, nodelist, from_cc, to_cc, colors_2, weights, 'green', True, edge)
                con_st = 'arc3, rad=-0.1'
            graph_draw(M, con_st, 1, None, 1)
            from_cc.clear()
            to_cc.clear()

    # for i, edge in enumerate(edgelist):
    #     if i == 2:
    #         for ed in edge:
    #             nx.draw_networkx_edges(G,
    #                                    pos=dict((n, G.nodes[n]["pos"]) for n in G.nodes()),
    #                                    arrows=True,
    #                                    width=3,
    #                                    edgelist=[ed],
    #                                    edge_color='purple',
    #                                    connectionstyle='arc3, rad=0.2'
    #                                    )
    #     if i == 5:
    #         for ed in edge:
    #             nx.draw_networkx_edges(G,
    #                                    arrows=True,
    #                                    pos=dict((n, G.nodes[n]["pos"]) for n in G.nodes()),
    #                                    width=3,
    #                                    edgelist=[ed],
    #                                    edge_color='green',
    #                                    connectionstyle='arc3, rad=0.1'
    #                                    )


def sequence_draw(G):
    edgelist = [("TCR", "SyppyrRS"), ("SyppyrRS", "SyppyrRS"), ("SyppyrRS", "LTS56"),
                ("TCR", "Spinstel4"), ("Spinstel4", "Spinstel4"), ("Spinstel4", "LTS56"),
                ("TCR", "Spinstel4"), ("Spinstel4", "Spinstel4"), ("Spinstel4", "Bask23")
                ]

    n = 0

    for i, edge in enumerate(edgelist):
        edge_labels = {}
        if n == 0:
            fig = plt.figure(figsize=(7, 7))
            ax = plt.gca()
            ellipse = Ellipse(xy=(15, 1), width=14, height=8,
                              edgecolor='black', fc='None', lw=1, alpha=0.3)
            ax.add_patch(ellipse)
            nx.draw_networkx_nodes(G,
                                   pos=dict((n, G.nodes[n]["pos"]) for n in G.nodes()),
                                   node_color=nx.get_node_attributes(G, 'color').values())
            nx.draw_networkx_labels(G,
                                    pos=dict((n, G.nodes[n]["pos"]) for n in G.nodes()),
                                    )
        if n == 0 or n == 1:
            col = 'r'
        if n == 2:
            col = 'b'
        nx.draw_networkx_edges(G,
                               arrows=True,
                               arrowstyle="->",
                               pos=dict((n, G.nodes[n]["pos"]) for n in G.nodes()),
                               width=[float(v['weight']) for (r, c, v) in G.edges(data=True)],
                               edgelist=[edge],
                               edge_color=col,
                               connectionstyle='arc3, rad=0.2'
                               )
        n += 1
        if n == 3:
            n = 0
            fig.savefig(os.path.join(my_path, f'sequence_{i}.svg'))
            plt.show()


def create_graph(type, node_list, from_cell, to_cell, colors, weights, color_edge, sequence, edge_list):
    """
    type: 0 - creating graph without motifs
          1 - creating motives
    """
    A = nx.MultiDiGraph()
    if type == 1:
        A = nx.Graph()
    add_n(node_list, A)
    if sequence:
        add_e_if(from_cell, to_cell, colors, weights, A, edge_list, type)
    else:
        add_e(from_cell, to_cell, colors, weights, A, color_edge)
    add_pos(A)
    return A


def draw_elements():
    """------drawing an ellipse to highlight the thalamus and lines to separate layers-----"""
    ax = plt.gca()
    ellipse = Ellipse(xy=(0, 1), width=40, height=20,
                      edgecolor='black', fc='None', lw=1, alpha=0.3)
    ax.add_patch(ellipse)

    x = [-50, 50]
    y = [[90, 90], [70, 70], [13, 13]]
    for i in y:
        plt.plot(x, i, linestyle='dashed', color='#6a040f', alpha=0.5)


if __name__ == '__main__':
    '''
    nodelist - a list of nuclei, 
        where the first 7 are excitatory neurons, 
        and the subsequent inhibitory ones
    from_c - source cell
    to_c - target cell
    color_node - color node
    weight - the amount of conductivity
    edge_list_n - the cycle of operation of the thalamocortical column
    '''
    edge_list_1 = [('TCR', 'Spinstel4'), ('Spinstel4', 'SyppyrFRB'), ('Spinstel4', 'LTS4'),
                   ('LTS4', 'Spinstel4'), ('Spinstel4', 'Spinstel4'), ('SyppyrFRB', 'NontuftRS6'),
                   ('TCR', 'NontuftRS6'), ('NontuftRS6', 'TCR')]

    from_c, to_c, color_edge, weight = read_csv()

    A = create_graph(0, nodelist, from_c, to_c, color_edge, weight, 'r', False, None)
    N = create_graph(0, nodelist, from_c, to_c, color_edge, weight, '#fb6107', False, None)
    G = create_graph(0, nodelist, from_c, to_c, color_edge, weight, 'b', False, None)
    S1 = create_graph(0, nodelist, from_c, to_c, color_edge, weight, None, True, edge_list_1)

    # g_draw(A, G, N, 0.7, 0.65, 0.6, 0, None, 0, 0, 'AMPA')
    # g_draw(A, G, N, 0.7, 0.65, 0.6, 0, None, 0, 0, 'GABA')
    # g_draw(A, G, N, 0.7, 0.65, 0.6, 0, None, 0, 0, 'NMDA')
    # g_draw(A, G, N, 0.7, 0.65, 0.6, 0, None, 0, 0, None)
    # g_draw(A, G, N, 0.7, 0.65, 0.6, 0, S1, 1, 1, None)

    g_draw(A, G, N, 0.7, 0.65, 0.6, 1, None, 0, 0, None)
