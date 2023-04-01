from dash import dcc, html

formatting = html.Div(
    className="formatting",
    children=[
        html.Button(
            id='clear_data',
            className= "formatter",
            children="Tabelle leeren"
        ),
        dcc.Checklist(
            id = 'decimal_separator', 
            className="formatter",
            options = ['Punkt als Dezimaltrennzeichen'], 
            value = [''], 
            inline=True
    )]
)