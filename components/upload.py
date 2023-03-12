from dash import dcc, html, dash_table
from dash_app import dash_app
from dash.dependencies import Input, Output, State
import pandas as pd
import base64, io, sys
from utils.table_upload import parse_contents


upload = dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop oder ',
                html.A('Datei auswählen')
            ]),
            multiple=False,
            contents= None,
            filename='',
            style={
                'width': '77%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin-left': 'auto', 
                'margin-right': 'auto',
                }
                )


@dash_app.callback(
    Output('table_store', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
)
def store_external_data(contents, filename, date):

    if contents is not None:
  
        children = [parse_contents(c, n, d) for c, n, d in zip([contents], [filename], [date])]

        # retrieve 'data' property of data table
        # json_data = children[0].data
        print("The size of df in data_store is {} bytes".format(sys.getsizeof(children)))  # 232 Bytes

        # table_columns = children[0].columns # columns # [{'name': i, 'id': i} for i in df.columns]
        # print(table_columns)

        table_store = {contents: children[0]}

    return table_store
