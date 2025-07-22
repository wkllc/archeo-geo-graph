import matplotlib.pyplot as plt
import networkx as nx
from collections import namedtuple
from collections import Counter
from networkx.algorithms import bipartite


import argparse
import pandas as pd
import pprint

from scripts.data_utils import load_network_data


def graph_analysis(nodes, edges, plot_graph=True):
    G = nx.from_pandas_edgelist(edges, 
                             source='source', 
                             target='target',
                             create_using=nx.DiGraph())

    print('Indegree centrality', nx.in_degree_centrality(G))
    print('Outdegree centrality', nx.out_degree_centrality(G))
    print('Katz centrality',nx.katz_centrality(G))
    print('Page rank', nx.pagerank(G))
    print('HITS', nx.hits(G))


    print('Average neighbor indegree',nx.average_neighbor_degree(G, source="in+out"))
    print('Average neighbor indegree',nx.average_neighbor_degree(G, source="in"))

    if plot_graph:
        plt.figure(figsize=(12, 8))
        plt.title('Network Graph')
        plt.axis('off')
        positions = nx.spring_layout(G, k=3, iterations=200)
        nx.draw(G, pos=positions, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black', edge_color='gray')
        plt.show()


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Run graph theory analysis on the trade networks',
                    description='Evaluates average neighbor indegree of trade networks',
                    epilog='Made by Tsveta and Dimitar')

    parser.add_argument('-coordinates', type=str, default="data/coordinates.csv")
    parser.add_argument('-imports', type=str, default="data/imports_combined.csv")
    parser.add_argument('-century', type=int, default='18')

    args = parser.parse_args()

    nodes, edges = load_network_data(
        coordinates_file=args.coordinates,
        imports_file=args.imports,
        century=args.century
        )
    
    graph_analysis(nodes, edges)
    