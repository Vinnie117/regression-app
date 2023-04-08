import sys
from dash import html, dash_table, callback_context
from assets.data_table import data_table, empty_data_table
from dash_app import dash_app
from dash.dependencies import Input, Output, State
from utils.data_prep import numeric_converter
import pandas as pd
import json


table = html.Div(
            className="table",
            children=
                dash_table.DataTable(
                    id='table',
                    columns=[
                        {
                            'name': '', 
                            'id': 'x', 
                            'type': 'numeric',
                            'format': {
                                'locale': {'decimal': ','}, 
                                'nully': '', 
                                'prefix': None, 
                                'specifier': ''
                            },
                            'on_change':{  # behaviour if user edits data cells
                                'action': 'coerce',  # try to coerce to column type
                                'failure': 'accept'  # accept failed coercion
                            },
                            'deletable': True,
                            'renamable': True
                        }, 
                        {
                            'name': '', 
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
                            'name': '', 
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
                            'name': '', 
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
                            'name': '', 
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
                    # fill_width=True,
                    virtualization=True,  # make datatable scrollable
                    style_cell={'width': '20%'}, # width of columns (100% / 5 cols)
                    fixed_rows={'headers': True},  #  fix headers for scrolling
                    style_table={'height': '200px'}
                )
        )


@dash_app.callback(
    Output('table', 'columns'),
    Output('table', 'data'),
    Input('decimal_separator', 'value'),
    Input('clear_data', 'n_clicks'),
    Input('table', 'columns'),
    Input('table', 'data'),
    State('table', 'selected_cells'),
    Input('table_store', 'data'),   
    Input('upload-data', 'contents'),
    Input('warning_upload_msg', 'cancel_n_clicks')
)
def data_prep(value, clear, columns, data, selected_cells, table_store, contents, cancel):

    if 'Punkt als Dezimaltrennzeichen' in value:
        decimal = '.'
    else:
        decimal = ','

    # if user clicks button to clear table data
    if callback_context.triggered_id == 'clear_data':
        data = pd.DataFrame(empty_data_table)  

        # adjust column names to dummy names
        table_columns = [{**col,
                          'name': 'Variable ' + str(col_index + 1),
                          'id': 'Variable ' + str(col_index + 1),
                          } for col_index, col in enumerate(columns)]

        # empty data frame as table data
        json_data = data.to_dict(orient='records') 


    # if user uploads data from external file
    elif table_store != None and callback_context.triggered_id == 'upload-data' and cancel != True:

        df = pd.DataFrame(table_store.get(contents)['props']['data'])
        json_data = df.to_dict(orient='records')

        external_columns = table_store.get(contents)['props']['columns']
        
        table_columns = [{
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

    else:

        df = pd.DataFrame(data)
        
        table_columns = [
            {
                **col,
                # 'name': df.columns[col_index],
                'format': {
                    **col.get('format', {}),
                    'locale': {'decimal': decimal}
                },
                'on_change':{
                    'action': 'coerce',
                    'failure': 'accept'
                }
            } for col in columns
        ]
 

        # create list of col names (in case user edits column names in data table)
        col_list = [d['name'] for d in table_columns]

        # default column names for dashboard
        if all(element == '' for element in col_list):
            col_list = ['x', 'y', 'z', 'a', 'b']       

        # rename the columns of the dataframe using col list
        df.columns = col_list

        # map correct column names to table columns
        for i, d in enumerate(table_columns):
            d['name'] = col_list[i]
            d['id'] = col_list[i]

        # try to convert string representation of numerics to numeric for edited cell
        if selected_cells != None:
            for i in selected_cells:
                # print(df.iloc[i['row']-1, i['column']])
                df.iloc[i['row']-1, i['column']] = numeric_converter(df.iloc[i['row']-1, i['column']])

        json_data = df.to_dict(orient='records')  # json Serialisierung, weil df nicht übertragen wird

    return table_columns, json_data




