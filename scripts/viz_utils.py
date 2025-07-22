import pandas as pd

def generate_proper_labels(G):
    """
    Generate a dictionary of proper labels for nodes in the graph.
    
    Args:
        G: NetworkX graph object.
        
    Returns:
        Dictionary mapping node names to their proper labels.
    """

    # proper location names
    labels_new = {'Kutahya':'Kütahya','Abisola_Italy':'Abisola', 'Central_Europe':'Central Europe', 'Valencia_Spain':'Valencia','Florence_Italy':'Florence',
            'Faenza_Italy':'Faenza', 'Iznik/Kutahya':'Iznik/Kütahya', 'Orvieto_Italy':'Orvieto', 'Tuscany_Italy':'Tuscany', 'West_Europe':'West Europe', 
            'South_Italy':'South Italy','Italian_States':'Italian States', 'Northwest_Anatolia':'Northwest Anatolia', 'German_States':'German States'}

    nodes = {str(node): node for node in G.nodes()}
    for key in nodes.keys():
        if key in labels_new:
            nodes[key] = labels_new[key]

    return nodes

def generate_node_color_list(G):
    """
    Generate a list of node colors based on predefined node colors.

    Args:
        G: NetworkX graph object.

    Returns:
        List of colors for each node in the graph.
    """
    node_color_list = [("#6D4A25")] * len(G.nodes())  # Default color for nodes
    # Create a mapping from nodes for the colouring
    for i, node in enumerate(G.nodes()):
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)

        if in_degree > 0 and out_degree > 0:
            node_color_list[i] = "#FF9100" # both incoming and outgoing edges
        elif in_degree > 0:
            node_color_list[i] = "#D61331" # only incoming edges
        elif out_degree > 0:
            node_color_list[i] = "#1565BB" # only outgoing edges

    return node_color_list

def generate_edge_alphas(edges, weight_feature='percent_imports', min_alpha=0.3, max_alpha=0.8):
    """
    Generate edge alphas based on the weight feature.

    Args:
        edges: DataFrame containing edge data.
        weight_feature: Column name for the weight feature.
        min_alpha: Minimum alpha value for edges.
        max_alpha: Maximum alpha value for edges.

    Returns:
        List of alpha values for each edge.
    """
    X = edges[weight_feature].to_numpy().squeeze()  # Preparing the percent_import data to be normalized
    X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    edge_alphas = X_std * (max_alpha - min_alpha) + min_alpha
    return edge_alphas

def generate_edge_colors(G,colors= ['#3D5064', "#6B2424"], source_nodes = {'Northwest_Anatolia', 'Chanakkale', 'Didymoteicho', 'Levantt', 'Ephesus'}):
    """
    Generate edge colors based on the source node.

    Args:
        G: NetworkX graph object.
        colors: List of colors for edges.

    Returns:
        List of colors for each edge in the graph.
    """
    edge_colors = []
    for edge in G.edges():
        source, target = edge
        if source in source_nodes:
            edge_colors.append(colors[0])  # Special color for specific nodes
        else:
            edge_colors.append(colors[1])  # Default color for other edges
    return edge_colors

# LONG = X
# LAT = Y
def nodesDF_to_positions(nodes: pd.DataFrame, x_offset: int = 0, y_offset: int = 0, apply_x_offset_to: list | str = 'all', apply_y_offset_to: list | str = 'all') -> dict:
    """
    Convert a DataFrame of nodes to a dictionary of positions.
    """
    # apply x and y offsets to all nodes
    if apply_x_offset_to == 'all' and apply_y_offset_to == 'all':
        return {row['Node']: (row.lon + x_offset, row.lat + y_offset) for _, row in nodes.iterrows()}
    
    # apply x to all, y to specified only
    elif apply_x_offset_to == 'all' and isinstance(apply_y_offset_to, list):
        return {row['Node']: (row.lon + x_offset, # X TO ALL
                              row.lat + y_offset if row['Node'] in apply_y_offset_to else row.lat)
                              for _, row in nodes.iterrows()}
    
    # apply y to all, x to specified only
    elif apply_y_offset_to == 'all' and isinstance(apply_x_offset_to, list):
        return {row['Node']: (row.lon + x_offset if row['Node'] in apply_x_offset_to else row.lon,
                              row.lat + y_offset) # Y TO ALL 
                for _, row in nodes.iterrows()}
    else:
        # if isinstance(apply_x_offset_to, str) and apply_x_offset_to in nodes['Node'].values:
        #     return nodesDF_to_positions(nodes, x_offset=x_offset, y_offset=y_offset, apply_x_offset_to=[apply_x_offset_to], apply_y_offset_to=apply_y_offset_to)
        # if isinstance(apply_y_offset_to, str) and apply_y_offset_to in nodes['Node'].values:
        #     return nodesDF_to_positions(nodes, x_offset=x_offset, y_offset=y_offset, apply_x_offset_to=apply_x_offset_to, apply_y_offset_to=[apply_y_offset_to])
        # else:
        raise ValueError("apply_x_offset_to and apply_y_offset_to should be either 'all' or a list of node names.")
    