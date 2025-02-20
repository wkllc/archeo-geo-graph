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

#load the csv file 
def parse_coordinates(file_name):
    df = pd.read_csv(file_name, sep=';', index_col='Node')
    return df.T.to_dict()

#substract for each century
def parse_imports(node_coordinates, file_name, century):
    df = pd.read_csv(file_name, sep=';')
    df_for_century = df.dropna(subset=[str(century)])

    # collect all nodes in a set
    nodes = set(df_for_century['Source node']).union(df_for_century['Target node'])
    
    edges = df_for_century.loc[:, ['Source node', 'Target node', 'Quantity', '% of imports for site per century', '% of all pottery for site per century']]
    Edge = namedtuple('Edge', ['source', 'target', 'quantity', 'percent_imports', 'percent_of_all_for_site'])
    edges = [Edge(source=r[0], target=r[1], quantity=float(r[2]), percent_imports=float(r[3]), percent_of_all_for_site=float(r[4])) for r in edges.to_numpy()]

    return nodes, edges

#visualize the network
def visualize(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)

    ebunch = list(map(lambda e: (e.source, e.target, {
        "source": e.source,
        "target": e.target,
        "quantity": e.quantity,
        "percent_imports": e.percent_imports,
        "percent_of_all_for_site": e.percent_of_all_for_site}), edges))

    G.add_edges_from(ebunch)

    positions = nx.spring_layout(G, k=3, iterations=200, weight='percent_import')
    
    #change the colour of the nodes for only some nodes - blue for local source nodes, red for target nodes
    node_colors = {'Sofia': ('#AD5260'), 'Belgrade': ('#AD5260'), 'Varna': ('#AD5260'), 'Izmir': ('#AD5260'), 'Mytilini': ('#AD5260'), 'Northwest_Anatolia':('#607E9F'), 
    'Northwest_Anatolia':('#607E9F'), 'Chanakkale':('#607E9F'), 'Didymoteicho':('#607E9F'), 'Levantt':('#607E9F'), 'Ephesus':('#607E9F')}
    node_color_list = [('#64513D')] * len(G.nodes()) #colour for the rest of the nodes

    # Create a mapping from nodes for the colouring
    for i, node in enumerate(G.nodes()):
        if node in node_colors:
            node_color_list[i] = node_colors[node]  

    #draw network nodes
    nx.draw_networkx_nodes(G, positions, node_color=node_color_list, 
            node_size=240, alpha=0.7,)
    
    #change the colour of the edges
    edge_colors = []
    for edge in G.edges():
        source, target = edge
        if source in {'Northwest_Anatolia', 'Chanakkale', 'Didymoteicho', 'Levantt', 'Ephesus'}:
            edge_colors.append('#3D5064')  
        else:
            edge_colors.append('#202020')  

    #draw network edges
    min_alpha, max_alpha = 0.3, 0.8 #setting the min and max alpha for this attribute

    percent_import_values = np.array([data['percent_imports'] for _, _, data in G.edges(data=True)]) #preparing the percent_import data to be normalised
    norm = Normalize(vmin=percent_import_values.min(), vmax=percent_import_values.max())

    edge_alphas = [min_alpha + (max_alpha - min_alpha) * norm(data['percent_imports']) for _, _, data in G.edges(data=True)] # creating an array for the alpha

    nx.draw_networkx_edges(G, positions, edge_color=edge_colors, width=4, alpha=edge_alphas, arrows=True, arrowsize=17)

    #change the labels for the nodes
    labels_new = {'Kutahya':'Kütahya','Abisola_Italy':'Abisola', 'Central_Europe':'Central Europe', 'Valencia_Spain':'Valencia','Florence_Italy':'Florence',
               'Faenza_Italy':'Faenza', 'Iznik/Kutahya':'Iznik/Kütahya', 'Orvieto_Italy':'Orvieto', 'Tuscany_Italy':'Tuscany', 'West_Europe':'West Europe', 
               'South_Italy':'South Italy','Italian_States':'Italian States', 'Northwest_Anatolia':'Northwest Anatolia', 'German_States':'German States'}
    
    current_nodes = {str(node): node for node in G.nodes()}

    labels_to_draw = {}
    for node in current_nodes:
        if node in labels_new:
            labels_to_draw[node] = labels_new[node]
        else:
            labels_to_draw[node] = node

    #draw network labels
    nx.draw_networkx_labels(G, positions, labels=labels_to_draw, font_size=13, font_color=('#202020'), font_weight='bold', horizontalalignment='right', verticalalignment='top') 


    edge_labels = nx.get_edge_attributes(G, 'percent_importss') #edge labels for the percent import
        
    nx.draw_networkx_edge_labels(G, positions, edge_labels, font_size=9, font_color=('#202020'), font_weight='bold',
                                  bbox=dict(facecolor='none', edgecolor='none')
                                  )

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-coordinates', type=str, default="Coordinates_version3.csv")
    parser.add_argument('-imports', type=str, default="imports_percent_combined_version4.csv")
    parser.add_argument('-century', required=False, type=int, default='15')

    args = parser.parse_args()
    node_coordinates = parse_coordinates(args.coordinates)
    nodes, edges = parse_imports(node_coordinates, args.imports, args.century)

    visualize(nodes, edges)