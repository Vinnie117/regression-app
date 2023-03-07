import sys
from dash import html, dash_table, callback_context
from assets.data_table import data_table
from dash_app import dash_app
from dash.dependencies import Input, Output, State
from utils.data_prep import numeric_converter
import pandas as pd
import json


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
                        'deletable': True,
                        'renamable': True
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
                        'deletable': True,
                        'renamable': True
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
                        'deletable': True,
                        'renamable': True
                    }

                ],
                data=data_table,
                editable=True,
                fill_width=False,
                virtualization=True,  # make datatable scrollable
                style_cell={'width': '100px'}, # width of columns
                fixed_rows={'headers': True},  #  fix headers for scrolling
                style_table={'height': '200px', 'overflowY': 'auto'}
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
    Output('table', 'data'),
    Input('decimal_separator', 'value'),
    Input('table', 'columns'),
    Input('table', 'data'),
    State('table', 'selected_cells'),
    Input('table_store', 'data'),   
    Input('upload-data', 'contents')
)
def data_prep(value, columns, data, selected_cells, table_store, contents):

    if 'Punkt als Dezimaltrennzeichen' in value:
        decimal = '.'
    else:
        decimal = ','

    # fetch which input triggered the callback
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if table_store != None and triggered_id == 'upload-data':
        
        df = pd.DataFrame(table_store.get(contents)['props']['data'])
        json_data = df.to_dict(orient='records')

        # print(json_data)
        # print(json.loads(json_data))  # check if json

        external_columns = table_store.get(contents)['props']['columns']
        

        table_columns = [
            {
                **col,
                'type': 'numeric',
                'format': {
                    **col.get('format', {}),
                    'locale': {'decimal': decimal}
                },
                'on_change':{
                    'action': 'coerce',
                    'failure': 'accept'
                },
                'deletable': True,
                'renamable': True
            }
            for col_index, col in enumerate(external_columns) if col_index <= 4  # default is 5 cols!
        ]

        # print(table_columns)




    else:
        df = pd.DataFrame(data)

        # try to convert string representation of numerics to numeric for edited cell
        if selected_cells != None:
            for i in selected_cells:
                # print(df.iloc[i['row']-1, i['column']])
                df.iloc[i['row']-1, i['column']] = numeric_converter(df.iloc[i['row']-1, i['column']])
        
        json_data = df.to_dict(orient='records')  # json Serialisierung, weil df nicht übertragen wird
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


    return table_columns, json_data




