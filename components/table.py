import sys
from dash import html, dash_table
from assets.data_table import data_table
from dash_app import dash_app
from dash.dependencies import Input, Output, State
from utils.data_prep import numeric_converter
import pandas as pd
import base64
import io

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return dash_table.DataTable(data = df.to_dict('records'),
                                columns = [{'name': i, 'id': i} for i in df.columns]
            )

table = html.Div(
            dash_table.DataTable(
                id='table',
                columns=[
                    {
                        'name': 'x', 
                        'id': 'x', 
                        'type': 'numeric',
                        'format': {
                            'locale': {'decimal': ','}, 
                            'nully': '', 
                            'prefix': None, 
                            'specifier': ''
                        },
                        'on_change':{
                            'action': 'coerce',
                            'failure': 'accept'
                        },
                        'renamable': False
                    }, 
                    {
                        'name': 'y', 
                        'id': 'y', 
                        'type': 'numeric',
                        'format': {
                            'locale': {'decimal': ','}, 
                            'nully': '', 
                            'prefix': None, 
                            'specifier': ''
                        },
                        'on_change':{
                            'action': 'coerce',
                            'failure': 'accept'
                        },
                        'renamable': False
                    },
                    {
                        'name': 'z', 
                        'id': 'z', 
                        'type': 'numeric',
                        'format': {
                            'locale': {'decimal': ','}, 
                            'nully': '', 
                            'prefix': None, 
                            'specifier': ''
                        },
                        'on_change':{
                            'action': 'coerce',
                            'failure': 'accept'
                        },
                        'deletable': True,
                        'renamable': True
                    },
                    {
                        'name': 'a', 
                        'id': 'a', 
                        'type': 'numeric',
                        'format': {
                            'locale': {'decimal': ','}, 
                            'nully': '', 
                            'prefix': None, 
                            'specifier': ''
                        },
                        'on_change':{
                            'action': 'coerce',
                            'failure': 'accept'
                        },
                        'deletable': True,
                        'renamable': True
                    },
                    {
                        'name': 'b', 
                        'id': 'b', 
                        'type': 'numeric',
                        'format': {
                            'locale': {'decimal': ','}, 
                            'nully': '', 
                            'prefix': None, 
                            'specifier': ''
                        },
                        'on_change':{
                            'action': 'coerce',
                            'failure': 'accept'
                        },
                        #'deletable': True,
                        #'renamable': True
                    }

                ],
                data=data_table,
                editable=True,
                fill_width=False,
                virtualization=True,  # make datatable scrollable
                style_cell={'width': '100px'} # width of columns
                
            ), style={
                'text-align': 'center', 
                'width': '77%', 
                'margin-left': 'auto', 
                'margin-right': 'auto',
                'border': '1px solid black',
                # 'display': 'inline-block'
            }
        )


@dash_app.callback(
    Output('table', 'columns'),
    Output('table_store', 'data'),
    Output('table', 'data'),
    Input('decimal_separator', 'value'),
    Input('table', 'columns'),
    Input('table', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def data_prep(value, columns, data, contents, filename, date):

    if contents is not None:

        print(contents)
        print(filename)
        print(date)
  
        children = [parse_contents(c, n, d) for c, n, d in zip([contents], [filename], [date])]

        # retrieve 'data' property of data table
        json_data = children[0].data


        table_columns = columns # [{'name': i, 'id': i} for i in df.columns]
        # print(table_columns)

        return table_columns, json_data, json_data

    else:

        # to adjust view dynamically
        df = pd.DataFrame(data)

        # try to convert string representation of numerics to numeric
        # applymap applies function to each cell
        df = df.applymap(numeric_converter)

        json_data = df.to_dict(orient='records')  # json Serialisierung, weil df nicht übertragen wird
        print("The size of df in data_store is {} bytes".format(sys.getsizeof(json_data)))  # 232 Bytes


        if 'Punkt als Dezimaltrennzeichen' in value:
            decimal = '.'
        else:
            decimal = ','

        table_columns = [
            {
                **col,
                'format': {
                    **col.get('format', {}),
                    'locale': {'decimal': decimal}
                },
                'on_change':{
                    'action': 'coerce',
                    'failure': 'accept'
                }
            }
            for col in columns

        ]

        print(json_data)

        return table_columns, json_data, json_data




