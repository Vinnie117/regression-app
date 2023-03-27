from dash import dcc, html

formatting = html.Div(
    className="formatting",
    children=[
        dcc.Checklist(
            id = 'decimal_separator', 
            options = ['Punkt als Dezimaltrennzeichen'], 
            value = [''], 
            inline=True
    )]
)