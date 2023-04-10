from dash import dcc, html

formatting = html.Div(
    className="formatting",
    children=[
        html.Button(
            id='clear_data',
            className= "formatter",
            children="Tabelle leeren"
        ),

        html.Button(
            id='col_names',
            className= "formatter",
            children="1. Zeile als Spaltennamen"
        ),
        dcc.Checklist(
            id = 'decimal_separator', 
            className="formatter",
            options = ['Punkt als Dezimaltrennzeichen'], 
            value = [''], 
            inline=True
        )
    ]
)