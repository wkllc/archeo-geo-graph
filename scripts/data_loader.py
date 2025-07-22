import pandas as pd
from pathlib import Path

currentDirectory = Path.cwd()
while currentDirectory.name != 'archeo-geo-graph':
    currentDirectory = currentDirectory.parent
data = currentDirectory / 'data'
default_imports_file = data /"imports_percent_combined_version4.csv"
default_coordinates_file = data / "Coordinates.csv"

def load_extract_imports(fpath: str = default_imports_file, 
                        century: int = 15, one_hot: bool = True, imports_sep: str = ';') -> pd.DataFrame:
    """
    Extract archeological imports data for a specific century.
    
    Args:
        fpath: Path to the CSV file containing imports data.
        century: Century to extract data for (default: 18)
        one_hot: If True, assumes centuries are one-hot encoded, if false it assumes a single 'century' feature/column.
        imports_sep: CSV separator for imports file.
        
    Returns:
        DataFrame with imports data for the specified century.
    """
    df = pd.read_csv(fpath, sep=imports_sep)
    if one_hot:
        # Filter columns for the specified century
        df_for_century = df.dropna(subset=[str(century)])
        cols_to_drop = [str(cent) for cent in range(10, 21) if str(cent) in df_for_century.columns]
        importsDataFrame = df_for_century.drop(columns=cols_to_drop)
        return importsDataFrame
    else:
        df_for_century = df[df['century'] == century]
        importsDataFrame = df_for_century.drop(columns=['century'])
        return importsDataFrame

def load_network_data(coordinates_file: str = default_coordinates_file, 
                      imports_file: str = default_imports_file, 
                      century: int = 15,
                      query_node: str = None,
                      coordinates_sep: str = ';',
                      imports_sep: str = ';') -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load nodes and edges of archeological imports data for a given century.
    
    Args:
        coordinates_file: Path to coordinates CSV file
        imports_file: Path to imports CSV file
        century: Century to extract data for
        coordinates_sep: CSV separator for coordinates file
        imports_sep: CSV separator for imports file
        
    Returns:
        Tuple of DataFrames (nodes, edges):
            - nodes: DataFrame with node coordinates (columns: 'Node', 'lat', 'lon')
                - 'lat' referse to latitude, 'lon' to longitude
            - edges: DataFrame with imports data (columns: 'source', 'target', 'quantity', '% of imports for site per century', '% of all pottery for site per century')
    """

    # Load archeological imports data, rename features
    importsDF = load_extract_imports(imports_file, century, one_hot=True, imports_sep=imports_sep)
    edges_df = importsDF.rename(columns={'Source node': 'source', 'Target node': 'target'})
    if query_node:
        edges_df = edges_df[(edges_df['source'] == query_node) | (edges_df['target'] == query_node) ]
    # Load coordinates data and drop irrelevant 'Z' coordinate feature, rename features
    coordinatesDF = pd.read_csv(coordinates_file, sep=coordinates_sep)
    if 'Z' in coordinatesDF.columns:
        coordinatesDF = coordinatesDF.drop(columns=['Z'])
    nodes_df = coordinatesDF.rename(columns={'N': 'lat', 'E': 'lon'})

    # find out nodes relevant to the quieried imports data
    relevant_nodes = edges_df[['source', 'target']].melt().drop_duplicates() # get all nodes from both source and target columns
    relevant_nodes = relevant_nodes.drop(columns=['variable']).rename(columns={'value': 'Node'}) # drop duplicates, rename column to 'Node'

    # Obtain only the coordinates of relevant nodes
    nodes_df = pd.merge(relevant_nodes, nodes_df, left_on='Node', right_on='Node', how='left')

    return nodes_df, edges_df


if __name__ == '__main__':
    nodes, edges = load_network_data(century=17)
    print("Nodes dataframe:\n")
    print(nodes.head())
    print("Edges dataframe:\n")
    print(edges.head())
