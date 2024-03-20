import argparse
import pandas as pd
from collections import namedtuple
import re

# https://stackoverflow.com/a/69079951
def to_snake_case(string):
    string = re.sub(r'(?<=[a-z])(?=[A-Z])|[^a-zA-Z]', ' ', string).strip().replace(' ', '_')
    return ''.join(string.lower())

def parse_excel_to_cytoscape(file_name, century):
    file = pd.ExcelFile(file_name)
    df = file.parse()
    df_for_century = df.dropna(subset=[century])

    source_nodes = set()
    target_nodes = set()
    source_nodes = source_nodes.union(df_for_century['Source node'])
    target_nodes = target_nodes.union(df_for_century['Target node'])

    edges = df_for_century.loc[:, ['Source node', 'Target node', 'Quantity', '% of imports for site per century', '% of imports and local for site per century']]
    Edge = namedtuple('Edge', ['source', 'target', 'quantity', 'percent_imports', 'percent_imports_and_local'])
    edges = [Edge(*r) for r in edges.to_numpy()]

    cytoscape_nodes = []
    for node in source_nodes:
        cytoscape_nodes.append(
            {
                'data': {'id': to_snake_case(node), 'label': node},
            }
        )
    for node in target_nodes:
        cytoscape_nodes.append(
            {
                'data': {'id': to_snake_case(node), 'label': node},
            }
        )

    cytoscape_edges = []
    for edge in edges:
        cytoscape_edges.append(
            {
                'data': {'source': to_snake_case(edge.source), 'target': to_snake_case(edge.target)},
            }
        )

    return cytoscape_nodes, cytoscape_edges

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('file_name', type=str)
    parser.add_argument('century', type=int)

    args = parser.parse_args()

    print(parse_excel_to_cytoscape(args.file_name, args.century))

