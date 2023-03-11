from dash import dcc, html

formatting = html.Div(
                dcc.Checklist(
                id = 'decimal_separator', 
                options = ['Punkt als Dezimaltrennzeichen'], 
                value = [''], inline=True),
                style={
                    'width': '77%',
                    'margin-left': 'auto', 
                    'margin-right': 'auto',
                }
            )
