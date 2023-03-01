
from dash import dcc, html

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

