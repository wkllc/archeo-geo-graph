import pickle
import matplotlib.pyplot as plt
import networkx as nx
from collections import namedtuple

import argparse
import pandas as pd

with open("directed_combined_15.pkl", "rb") as f:
    G_15 = pickle.load(f)

with open("directed_combined_16.pkl", "rb") as f:
    G_16 = pickle.load(f)

with open("directed_combined_17.pkl", "rb") as f:
    G_17 = pickle.load(f)

with open("directed_combined_18.pkl", "rb") as f:
    G_18 = pickle.load(f)

with open("directed_combined_19.pkl", "rb") as f:
    G_19 = pickle.load(f)

with open("directed_combined_20.pkl", "rb") as f:
    G_20 = pickle.load(f)

#isomorphic = nx.is_isomorphic(G_19, G_20)
#print("Graphs are isomorphic:", isomorphic)

#print('Graph Edit Distance between 15 and 16 centuries',nx.graph_edit_distance(G_15,G_16))
#print('Graph Edit Distance between 16 and 17 centuries',nx.graph_edit_distance(G_16,G_17))
#print('Graph Edit Distance between 17 and 18 centuries',nx.graph_edit_distance(G_17,G_18))
#print('Graph Edit Distance between 18 and 19 centuries',nx.graph_edit_distance(G_18,G_19))
#print('Graph Edit Distance between 19 and 20 centuries',nx.graph_edit_distance(G_19,G_20))


#print(nx.simrank_similarity(G_18, source='Mytilini'))