import matplotlib.pyplot as plt
import networkx as nx
from collections import namedtuple
from collections import Counter
from networkx.algorithms import bipartite


import argparse
import pandas as pd
import pprint

from visualize import parse_coordinates, parse_imports


def analyse(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)

    ebunch = list(map(lambda e: (e.source, e.target, {
        "source": e.source,
        "target": e.target,
        "quantity": e.quantity,
        "percent_imports": e.percent_imports,
        "percent_of_all_for_site": e.percent_of_all_for_site}), edges))

    G.add_edges_from(ebunch)

    positions = nx.spring_layout(G, k=3, iterations=200)

    #nx.draw_networkx(G, positions)
    #plt.show()

    print('Average neighbor indegree',nx.average_neighbor_degree(G, source="in", weight='percent_import'))
    print('Indegree centrality', nx.in_degree_centrality(G))
    print('Outdegree centrality', nx.out_degree_centrality(G))
    print('Is this network weedly connected',nx.is_weakly_connected(G))
    print('Karz centrality',nx.katz_centrality(G, weight='percent_imports"'))
    print('Page rank', nx.pagerank(G, weight='percent_import'))
    print('HITS', nx.hits(G))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-coordinates', type=str, default="Coordinates_version3.csv")
    parser.add_argument('-imports', type=str, default="imports_percent_combined_version4.csv")
    parser.add_argument('-century', type=int, default='16')

    args = parser.parse_args()
    node_coordinates = parse_coordinates(args.coordinates)
    nodes, edges = parse_imports(node_coordinates, args.imports, args.century)
    analyse(nodes, edges)