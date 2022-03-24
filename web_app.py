import base64
import datetime
import io

import dash
from dash import Input, Output, html, dcc, dash_table
import plotly.express as px

import pandas as pd
from helper_fuctions import process_single_file, filter_single_file


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
server = app.server
app.title = "Quantum dropjump filecruncher"

app.layout = html.Div([ # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
    html.P('1) Eins oder mehrere .csv files (quantum Rohdaten) hochladen'),
    html.P('2) Via \'Export\' Button oben an der Tabelle die berechneten Messgrössen exportieren'),
    html.P('Anmerkungen: Nur Exzentrik, nur Teil der Bewegung nach Landung (v_max) wird benutzt. Ausser für \'max speed of concentric motion\''),
    # html.P('Graph nur zu illustrativen Zwecken.'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    # html.Div(id='graph-div'),
    html.Div(id='output-datatable'),
])


def parse_contents(contents_list):
    result_df = pd.DataFrame()
    for contents in contents_list:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=";")
            result_df = pd.concat([result_df, process_single_file(df)])
            # result_df.append(process_single_file(df))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

    return html.Div([
        html.Hr(),

        dash_table.DataTable(
            data=result_df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in result_df.columns],
            page_size=20,
            export_format="xlsx",
            style_data={'whiteSpace': 'normal','height': 'auto'},
            style_cell={'maxWidth': '100px'},
            style_header= {'whiteSpace': 'normal'},
        ),
        dcc.Store(id='stored-data', data=result_df.to_dict('records')),
    ])

def parse_full_df(contents_list):
    df_full = pd.DataFrame()
    for contents in contents_list:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=";")
            df_full = pd.concat([df_full, filter_single_file(df)])
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
    return df_full

def create_graph(df):
    fig = px.line(df, x='time', y='Speed [m/s]', color='unique_key')
    fig.update_layout(showlegend=False) 
    return dcc.Graph(id='graph', figure=fig)

@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
)
def update_output(list_of_contents):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents)]
        return children

# @app.callback(Output('graph-div', 'children'),
#               Input('upload-data', 'contents'),
# )
# def update_graph(list_of_contents):
#     if list_of_contents is not None:
#         full_df = parse_full_df(list_of_contents)
#         fig = create_graph(full_df)
#         return fig

if __name__ == '__main__':
    app.run_server(debug=True)