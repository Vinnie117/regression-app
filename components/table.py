from dash.dash_table.Format import Format
from dash import html, dash_table, dcc
from assets.data_table import data_table
from dash_app import dash_app
from dash.dependencies import Input, Output, State
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
    
    Output('table', 'data'),
    # Output('table_store', 'data'),

    Input('decimal_separator', 'value'),
    Input('table', 'columns'),

    Input('table', 'data'),
    # Input('table', 'data'),

    prevent_initial_call=True
)
def decimal_separator(value, columns,data):

    df = pd.DataFrame(data)
    # print(df)
    # print(df.dtypes)
    df = df.applymap(numeric_converter)
    json_data = df.to_dict(orient='records')

    if 'Punkt als Dezimaltrennzeichen' in value:
        decimal = '.'
    else:
        decimal = ','


    return [
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

    ], json_data



# @dash_app.callback(
#     Output('table', 'data'),
#     Input('table_store', 'data')
# )
# def clean_data(clean_df):
#     return clean_df

