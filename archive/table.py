from dash.dash_table.Format import Format
from dash import html, dash_table
from assets.data_table import data_table

table = html.Div(
            dash_table.DataTable(
                id='table',
                columns=[
                    {
                        'name': 'x', 
                        'id': 'x', 
                        'type': 'numeric',
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'renamable': False
                    }, 
                    {
                        'name': 'y', 
                        'id': 'y', 
                        'type': 'numeric',
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'renamable': False
                    },
                    {
                        'name': 'z', 
                        'id': 'z', 
                        'type': 'numeric',
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'deletable': True,
                        'renamable': True
                    },
                    {
                        'name': 'a', 
                        'id': 'a', 
                        'type': 'numeric',
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'deletable': True,
                        'renamable': True
                    },
                    {
                        'name': 'b', 
                        'id': 'b', 
                        #'type': 'numeric',
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
                'border': '1px solid black'
            }
        )