import contextily as cx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import namedtuple
from matplotlib.colors import Normalize 

import geopandas

import argparse
import pandas as pd
import pprint

from scripts.data_loader import load_network_data
from scripts.viz_utils import *


#visualize the network
def visualize(nodes, edges):
    G = nx.from_pandas_edgelist(edges, 
                             source='source', 
                             target='target',
                             edge_attr = True,
                             create_using=nx.DiGraph())
    
    weight_feature = '% of imports for site per century'

    positions = nx.spring_layout(G, k=3,
                                iterations=200,
                                weight=weight_feature)
    
    # map nodes to colors according to their in-degree and out-degree
    node_color_list = generate_node_color_list(G)

    # draw network nodes
    nx.draw_networkx_nodes(G, positions,
                           node_color=node_color_list,
                           node_size=240,
                           alpha=0.7)

    
    # draw network edges
    edge_colors = generate_edge_colors(G) # according to source node
    edge_alphas = generate_edge_alphas(edges, weight_feature=weight_feature) # transparency according to weight feature
    nx.draw_networkx_edges(G, positions,
                           edge_color=edge_colors,
                           width=4,
                           alpha=edge_alphas,
                           arrows=True,
                           arrowsize=17
                           )
    
    # draw node labels
    labels_to_draw = generate_proper_labels(G)
    nx.draw_networkx_labels(G, positions,
                            labels=labels_to_draw,
                            font_size=13,
                            font_color=('#202020'),
                            font_weight='bold',
                            horizontalalignment='right',
                            verticalalignment='top'
                            )

    # draw edge labels according to desired feature
    edge_labels = nx.get_edge_attributes(G, weight_feature)
    nx.draw_networkx_edge_labels(G, positions,
                                edge_labels,
                                font_size=9,
                                font_color=('#202020'),
                                font_weight='bold',
                                bbox=None
                                )

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-coordinates', type=str, default="data/Coordinates.csv")
    parser.add_argument('-imports', type=str, default="data/imports_percent_combined_version4.csv")
    parser.add_argument('-century', required=False, type=int, default='15')

    args = parser.parse_args()
    nodes, edges = load_network_data(coordinates_file=args.coordinates, imports_file=args.imports, century=args.century)

    visualize(nodes, edges)