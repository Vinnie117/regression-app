from dash.dash_table.Format import Format
from dash import html, dash_table, dcc
from assets.data_table import data_table

table = html.Div([

            html.Div(
                dcc.Checklist(
                id = 'decimal_separator', 
                options = ['Punkt als Dezimaltrennzeichen'], 
                value = [''], inline=True),
                style={}
            ),

            # html.Div(
            #     html.P("EMPTY"), 
            #     style={         
            #         'display': 'inline-block',
            #         'border': '1px dashed blue'
            #     }
            # ),

            html.Div(
            dash_table.DataTable(
                id='table',
                columns=[
                    {
                        'name': 'x', 
                        'id': 'x', 
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'renamable': False
                    }, 
                    {
                        'name': 'y', 
                        'id': 'y', 
                        'format': dict(locale=dict(decimal='.'), nully='N/A'),
                        
                        
                            #  Format(
                            #     nully='N/A',
                            #     ),
                        #'on_change': {'action': 'coerce', 'failure': 'default'},
                        'renamable': False
                    },
                    {
                        'name': 'z', 
                        'id': 'z', 
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'deletable': True,
                        'renamable': True
                    },
                    {
                        'name': 'a', 
                        'id': 'a', 
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'deletable': True,
                        'renamable': True
                    },
                    {
                        'name': 'b', 
                        'id': 'b', 
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
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