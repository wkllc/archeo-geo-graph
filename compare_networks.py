import pickle
import matplotlib.pyplot as plt
import networkx as nx
from collections import namedtuple

import argparse
import pandas as pd

with open("15_combined.pickle", "rb") as f:
    G_15 = pickle.load(f)

with open("16_combined.pickle", "rb") as f:
    G_16 = pickle.load(f)

with open("17_combined.pickle", "rb") as f:
    G_17 = pickle.load(f)

with open("18_combined.pickle", "rb") as f:
    G_18 = pickle.load(f)

with open("19_combined.pickle", "rb") as f:
    G_19 = pickle.load(f)

with open("20_combined.pickle", "rb") as f:
    G_20 = pickle.load(f)

#print('Graph Edit Distance between 15 and 16 centuries',nx.graph_edit_distance(G_15,G_16))
#print('Graph Edit Distance between 16 and 17 centuries',nx.graph_edit_distance(G_16,G_17))
#print('Graph Edit Dissance between 17 and 18 centuries',nx.graph_edit_distance(G_17,G_18))
#print('Graph Edit Distance between 18 and 19 centuries',nx.graph_edit_distance(G_18,G_19))
#print('Graph Edit Distance between 19 and 20 centuries',nx.graph_edit_distance(G_19,G_20))