import matplotlib.pyplot as plt
import networkx as nx
from collections import namedtuple


import argparse
import pandas as pd
import pprint

from visualize import parse_coordinates, parse_imports

def analyse(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes.keys())
    ebunch = list(map(lambda e: (e.source, e.target, {"quantity": e.quantity, "percent_imports": e.percent_imports, "percent_of_all_for_site": e.percent_of_all_for_site}), edges))
    G.add_edges_from(ebunch)

    positions = nodes

    print(nx.average_neighbor_degree(G, source="out", target="in", weight="percent_imports"))




 
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
