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

def generate_edge_alphas(edges, weight_feature='% of imports for site per century', min_alpha=0.3, max_alpha=0.8):
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