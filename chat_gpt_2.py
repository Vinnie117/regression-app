from dash import Dash, dcc, html, dash_table, Output, Input
import plotly.graph_objects as go

# initialize Dash app and set up layout
app = Dash()

app.layout = html.Div([
    # create the data table
    dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'X', 'id': 'x'},
            {'name': 'Y', 'id': 'y'},
        ],
        data=[
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 1},
            {'x': 2, 'y': 2},
            {'x': 3, 'y': 3},
            {'x': 4, 'y': 4},
        ],
        editable=True,
    ),
    # create the scatter plot
    dcc.Graph(id='scatterplot'),
    # create the div that will display the sum of all numbers in the table
    html.Div(id='sum')
])

# callback to update the scatter plot when the table data changes
@app.callback(
    Output('scatterplot', 'figure'),
    [Input('table', 'data')])
def update_scatterplot(data):
    # extract the x and y values from the table data
    x = [row['x'] for row in data]
    y = [row['y'] for row in data]

    # create the scatter plot
    figure = go.Figure(data=[go.Scatter(x=x, y=y, mode='markers')])

    return figure

# callback to update the sum div when the table data changes
@app.callback(
    Output('sum', 'children'),
    [Input('table', 'data')])
def update_sum(data):
    # calculate the sum of all numbers in the table
    total = sum([row['x'] + row['y'] for row in data])

    return f'Sum: {total}'

if __name__ == '__main__':
    app.run_server(debug=True)