import contextily as cx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import namedtuple
from matplotlib.colors import Normalize 
from dotenv import load_dotenv

import argparse
import pandas as pd
import os

from scripts.data_loader import load_network_data
from scripts.viz_utils import *

#visualize the map 
def visualize(nodes, edges):
    # instantiate the graph object modeling the network
    G = nx.from_pandas_edgelist(edges, 
                                    source='source',
                                    target='target',
                                    edge_attr=True,
                                    create_using=nx.DiGraph())
    
    # define plt figure - set the limits of the map before adding the basemap for best results
    xlim = nodes.min().lon - 5, nodes.max().lon + 5
    ylim = nodes.min().lat - 5, nodes.max().lat + 5
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_title("Trade in the Ottoman Empire")
    ax.axis("off")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # transform the nodes coordinates dataframe to a dictionary
    # ready to be ingested by the plotting function
    positions = nodesDF_to_positions(nodes)

    # generate color lists based on in-degrees and out-degrees
    node_colors = generate_node_color_list(G)

    nx.draw_networkx_nodes(G, positions,
                                ax = ax,
                                node_color=node_colors,
                                node_size=240,
                                alpha=0.8
                                )
    

    # generate colors based on their source
    edge_colors = generate_edge_colors(G)

    # generate edge alphas based on the weight metric 
    edge_alphas = generate_edge_alphas(edges)

    nx.draw_networkx_edges(G, positions,
                                ax=ax,
                                edge_color=edge_colors,
                                width=4,
                                alpha=edge_alphas,
                                arrows=True,
                                arrowsize=17
                            )
    
    # replace simplified labels with proper labels using special characters
    labels_to_draw = generate_proper_labels(G)

    # obtain positions for labels - tweak offsets to achieve visibility
    label_positions = nodesDF_to_positions(nodes, 
                                            x_offset=-2,
                                            y_offset=0.5,
                                            apply_x_offset_to=['Mytilini'],
                                            apply_y_offset_to='all')

    nx.draw_networkx_labels(G, label_positions,
                                labels=labels_to_draw,
                                ax=ax,
                                font_size=14,
                                font_color=('#202020'),
                                font_weight='bold',
                                horizontalalignment='left',
                                verticalalignment='bottom'
                            )
    # get the positions of nodes
    edge_label_positions = nodesDF_to_positions(nodes) #, x_offset= -42, y_offset = 2.2)
    # select the weight feature
    weight_feature = '% of imports for site per century'
    # get the actual labels
    edge_labels = nx.get_edge_attributes(G, weight_feature)
    nx.draw_networkx_edge_labels(G, 
                                    pos=edge_label_positions,
                                    ax=ax,
                                    edge_labels=edge_labels,
                                    font_size=9,
                                    font_color=('#202020'), 
                                    font_weight='bold',
                                    # horizontalalignment='left',
                                    # verticalalignment='center', 
                                    bbox={'facecolor': 'white', 'alpha': 0.9, 'pad': 2}
                                )

    provider = cx.providers.Stadia.StamenTerrainBackground(api_key=os.environ['STAMEN_API_KEY'])
    provider["url"] = provider["url"] + "?api_key={api_key}"
    cx.add_basemap(ax, crs='WGS84', source=provider, zoom='auto', alpha=0.6)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-coordinates', type=str, default="data/Coordinates.csv")
    parser.add_argument('-imports', type=str, default="data/imports_percent_combined_version4.csv")
    parser.add_argument('-century', required=False, type=int, default='15')
    parser.add_argument('-query', required=False, type=str, default='Mytilini')
    
    args = parser.parse_args()

    load_dotenv()
    # print(os.getenv('STAMEN_API_KEY'))
    nodes, edges = load_network_data(coordinates_file=args.coordinates, imports_file=args.imports, century=args.century, query_node=args.query)

    visualize(nodes, edges)
