from dash import Dash, html, dcc
from dash import dash_table
import plotly.express as px
import pandas as pd

app = Dash(__name__)

####
# some variables

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})


params = ['XXX', 'YYY', 'ZZZ']
####

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# Layout describes the look of the app
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    # dcc = dash core component
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            [{'id': 'Model', 'name': 'Row'}] +
            [{'id': p, 'name': p} for p in params]
        ),
        data=[
            dict(Model=i, **{param: 0 for param in params})
            for i in range(1, 5)
        ],
        editable=True,
        fill_width=False,


    ),
    dcc.Graph(
        id='table-editing-simple-output', 
        style={'width': '100%', 'height': '100%'}    # size of the
        )
    

    
])




# Dash uses Flask as web server
if __name__ == '__main__':

    print(app.layout)    # Google: python select elements from html div
    print(type(app.layout))

    app.run_server(debug=True)