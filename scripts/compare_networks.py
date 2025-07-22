import pickle
import matplotlib.pyplot as plt
import networkx as nx
from collections import namedtuple

import argparse
import pandas as pd

from scripts.data_loader import load_network_data

def network_comparison(imports_path, coordinates_path, century_1, century_2):
    """
    Compare two network graphs from different centuries.

    Args:
        fpath: Path to the pickle file containing the network data.
        century_1: First century to compare.
        century_2: Second century to compare.

    Returns:
        None
    """

    nodes, edges = load_network_data(coordinates_file=coordinates_path, imports_file=imports_path, century=century_1)
    G_1 = nx.from_pandas_edgelist(edges,
                                  source='source',
                                  target='target',
                                  edge_attr=True,
                                  create_using=nx.DiGraph())
    

    nodes, edges = load_network_data(coordinates_file=coordinates_path, imports_file=imports_path, century=century_2)
    G_2 = nx.from_pandas_edgelist(edges,
                                  source='source',
                                  target='target',
                                  edge_attr=True,
                                  create_using=nx.DiGraph())


    print(f"Graph Edit Distance between imports networks of centuries {century_1} and {century_2}: {nx.graph_edit_distance(G_1, G_2)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='comapre_networks',
                    description='Compare the network graphs of 2 different centuries',
                    epilog='made by Tsveta and Dimitar')

    parser.add_argument('-coordinates', type=str, default="data/Coordinates.csv")
    parser.add_argument('-imports', type=str, default="data/imports_percent_combined_version4.csv")
    parser.add_argument('-century_1', required=False, type=int, default='15')
    parser.add_argument('-century_2', required=False, type=int, default='16')

    args = parser.parse_args()

    network_comparison(imports_path = args.imports,
                       coordinates_path = args.coordinates,
                       century_1 = args.century_1,
                       century_2 = args.century_2)