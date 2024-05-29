import matplotlib.pyplot as plt
import networkx as nx
from collections import namedtuple


import argparse
import pandas as pd
import pprint
import pickle


from visualize import parse_coordinates, parse_imports

def analyse(nodes, edges):
    G_directed = nx.DiGraph()
    G_directed.add_nodes_from(nodes.keys())

    G_undirected = nx.Graph()
    G_undirected.add_nodes_from(nodes.keys())


    ebunch = list(map(lambda e: (e.source, e.target, {"quantity": e.quantity, "percent_imports": e.percent_imports, "percent_of_all_for_site": e.percent_of_all_for_site}), edges))
    G_directed.add_edges_from(ebunch)
    G_undirected.add_edges_from(ebunch)

    positions = nodes

    # print('Average neighbor degree',nx.average_neighbor_degree(G_directed, source="in", weight="percent_of_all_for_site")) #useufl
    # print('Indegree centrality', nx.in_degree_centrality(G_directed)) #useful
    # print(nx.sigma(G_undirected)) #not useful
    # print(nx.omega(G_undirected)) #not useful
    # print('Is this network weedly connected',nx.is_weakly_connected(G_directed))
    # print('Karz centrality',nx.katz_centrality(G_directed, weight='percent_of_all_for_site"')) # useful
    # print(nx.trophic_levels(G_directed, weight='percent_of_all_for_site')) #not useful - visible without this
    # print('Clustering',nx.clustering(G_directed)) #not useful
    # print('Page rank', nx.pagerank(G_directed)) #useful
    # reciprocity - not useful for our network but perhaps in another one
    # comparing two or more network's similarity 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-coordinates', type=str, default="Coordinates_version3.csv")
    parser.add_argument('-imports', type=str, default="imports_percent_combined_version4.csv")
    parser.add_argument('-century', required=True, type=int)

    args = parser.parse_args()
    node_coordinates = parse_coordinates(args.coordinates)
    nodes, edges = parse_imports(node_coordinates, args.imports, args.century)
    analyse(nodes, edges)
