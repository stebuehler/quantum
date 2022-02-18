import base64
import datetime
import io

import dash
from dash import Input, Output, html, dcc, dash_table
import plotly.express as px

import pandas as pd
from helper_fuctions import process_single_file


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
server = app.server
app.title = "Quantum dropjump filecruncher"

app.layout = html.Div([ # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
    html.P('1) Eins oder mehrere .csv files (quantum Rohdaten) hochladen'),
    html.P('2) Via \'Export\' Button oben an der Tabelle die berechneten Messgrössen exportieren'),
    html.P('Anmerkung: Nur Exzentrik, nur Teil der Bewegung nach Landung (v_max) wird benutzt.'),
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
    html.Div(id='output-div'),
    html.Div(id='output-datatable'),
])


def parse_contents(contents_list):
    full_df = pd.DataFrame()
    for contents in contents_list:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=";")
            df_result = process_single_file(df)
            full_df = pd.concat([full_df, df_result])
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

    return html.Div([
        html.Hr(),

        dash_table.DataTable(
            data=full_df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in full_df.columns],
            page_size=20,
            export_format="xlsx",
            style_data={'whiteSpace': 'normal','height': 'auto'},
            style_cell={'maxWidth': '100px'},
            style_header= {'whiteSpace': 'normal'},
        ),
        dcc.Store(id='stored-data', data=full_df.to_dict('records')),
    ])


@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
)
def update_output(list_of_contents):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents)]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)