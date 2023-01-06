from dash import Dash, dcc, html, dash_table, Output, Input
import plotly.graph_objects as go

app = Dash()

data = [
        {'x': 0, 'y': 0},
        {'x': 1, 'y': 1},
        {'x': 2, 'y': 2},
        {'x': 3, 'y': 3},
        {'x': 4, 'y': 4},
        {'x': 2, 'y': 5},
        {'x': 3, 'y': 4}
]

app.layout = html.Div([
    
    # a header for the webpage
    html.H1('My Dash App'),

    # create the data table
    dash_table.DataTable(
        id='table',
        columns=[{'name': 'x', 'id': 'x'}, {'name': 'y', 'id': 'y'}],
        data=data,
        editable=True,
        fill_width=False,
        style_cell={'width': '10%'}
    ),

    # a submit button
    html.Button('Submit', id='submit-val', n_clicks=0),

    # create the scatter plot
    dcc.Graph(id='scatterplot'),

     # create the div that will display the sum of all numbers in the table
    html.Div(id='sum')
    ])

@app.callback(
    Output(component_id = 'scatterplot', component_property = 'figure'),
    [Input(component_id = 'table', component_property = 'data')])
def update_scatterplot(data):
    x = [d['x'] for d in data]
    y = [d['y'] for d in data]

    # create the scatter plot
    figure = go.Figure(data=[go.Scatter(x=x, y=y, mode='markers')])

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)






