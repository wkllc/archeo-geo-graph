import contextily as cx
import matplotlib.pyplot as plt
import networkx as nx
from collections import namedtuple

import geopandas

import argparse
import pandas as pd
import pprint

def parse_coordinates(file_name):
    df = pd.read_csv(file_name, sep=';', index_col='Node')
    return df.T.to_dict()

def parse_imports(node_coordinates, file_name, century):
    df = pd.read_csv(file_name, sep=';')
    df_for_century = df.dropna(subset=[str(century)])

    # collect all nodes in a set
    node_names = set(df_for_century['Source node']).union(df_for_century['Target node'])
    nodes = {}
    for node_name in node_names:
        coordinates = node_coordinates.get(node_name)
        if not coordinates:
            raise RuntimeError(f"Node name {node_name} not found in coordinates file")
        nodes[node_name] = float(coordinates['E']), float(coordinates['N'])

    edges = df_for_century.loc[:, ['Source node', 'Target node', 'Quantity', '% of imports for site per century', '% of all pottery for site per century']]
    Edge = namedtuple('Edge', ['source', 'target', 'quantity', 'percent_imports', 'percent_of_all_for_site'])
    edges = [Edge(source=r[0], target=r[1], quantity=int(r[2]), percent_imports=float(r[3]), percent_of_all_for_site=float(r[4])) for r in edges.to_numpy()]

    return nodes, edges

def visualize(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes.keys())
    ebunch = list(map(lambda e: (e.source, e.target, {"edge":e}), edges))
    G.add_edges_from(ebunch)

    positions = nodes

    from shapely.geometry import Point
    cities, geometry = zip(*list(nodes.items()))
    d = {'city': cities, 'geometry': list(map(Point, geometry))}
    gdf = geopandas.GeoDataFrame(d, crs="WGS84")

    # plot with a nice basemap
    ax = gdf.plot(marker=".", color="orangered", figsize=(9,9))
    try:  # For issues with downloading/parsing basemaps in CI
        cx.add_basemap(ax, crs=gdf.crs, source=cx.providers.CartoDB.VoyagerNoLabels, zoom=6)
    except:
        print("Could not add basemap")
        pass
    ax.set_title("Map")
    ax.axis("off")
    ax.set_xlim(-20, 50)
    ax.set_ylim(-20, 60)

    node_colors = {'Sofia': 'blue', 'Belgrade':'blue', 'Varna':'blue', 'Izmir':'blue', 'Mytilini':'blue',}
    node_color_list = [node_colors.get(node, 'black') for node in G.nodes()]

    nx.draw(G, positions, ax=ax, node_size=60, edge_color='black', alpha=0.5, arrows=True, arrowsize=15)
    nx.draw_networkx_nodes(G, positions, node_color=node_color_list, 
            node_size=60, alpha=0.5, linewidths=0,)

    nx.draw_networkx_labels(G, positions, font_size=10, verticalalignment='top')

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-coordinates', type=str, default="Coordinates_version3.csv")
    parser.add_argument('-imports', type=str, default="imports_percent_detailed_version4.csv")
    parser.add_argument('-century', required=True, type=int)

    args = parser.parse_args()
    node_coordinates = parse_coordinates(args.coordinates)
    nodes, edges = parse_imports(node_coordinates, args.imports, args.century)

    visualize(nodes, edges)

