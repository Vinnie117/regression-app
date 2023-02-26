import sys
from dash import html, dash_table, dcc
from assets.data_table import data_table
from dash_app import dash_app
from dash.dependencies import Input, Output
from utils.data_prep import numeric_converter
import pandas as pd

table = html.Div([

            html.Div(
                dcc.Checklist(
                id = 'decimal_separator', 
                options = ['Punkt als Dezimaltrennzeichen'], 
                value = [''], inline=True),
                style={}
            ),


            html.Div(
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
])

@dash_app.callback(
    Output('table', 'columns'),
    Output('table_store', 'data'),
    Output('table', 'data'),
    Input('decimal_separator', 'value'),
    Input('table', 'columns'),
    Input('table', 'data'),
    # prevent_initial_call=True
)
def data_prep(value, columns, data):

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

    return table_columns, json_data, json_data




