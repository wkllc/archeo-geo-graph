import argparse

from dash import Dash, html
import dash_cytoscape as cyto
from parse import parse_excel_to_cytoscape

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-file', type=str, default='Final_Database_Aoristic.xlsx')
    parser.add_argument('-century', type=int, required=True)

    args = parser.parse_args()

    nodes, edges = parse_excel_to_cytoscape(args.file, args.century)

    app = Dash(__name__)

    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape-compound',
            layout={'name': 'random'},
            elements=nodes + edges,
        )
    ])

    app.run(debug=True)