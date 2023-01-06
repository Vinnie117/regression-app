from dash import Dash, dcc, html, dash_table, Output, Input, State
from dash.dash_table.Format import Format
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
        columns=[
            {
                'name': 'x', 
                'id': 'x', 
                'type': 'numeric',
                'format': Format(nully='N/A'),
                'on_change': {'action': 'coerce', 'failure': 'default'}
            }, 
            {
                'name': 'y', 
                'id': 'y', 
                'type': 'numeric',
                'format': Format(nully='N/A'),
                'on_change': {'action': 'coerce', 'failure': 'default'}
            }
            ],
        data=data,
        editable=True,
        fill_width=False,
        style_cell={'width': '10%'}
    ),

    # a submit button
    html.Button('Submit', id='submit-val', n_clicks=0),

    # create the scatter plot
    dcc.Graph(id='scatterplot', style={'width': '100%', 'height': '100%'} ),

    # another submit button
    html.Button(id='submit-button-state', children='Submit2', type='button'),

     # create the div that will display the sum of all numbers in the table
    html.Div(id='sum-state')
    ])

# callback to update the scatter plot when the table data changes
@app.callback(
    Output(component_id = 'scatterplot', component_property = 'figure'),
    Input(component_id = 'table', component_property = 'data'))
def update_scatterplot(data):
    x = [d['x'] for d in data]
    y = [d['y'] for d in data]

    print("X is: ", x, '\n', "Y is: ", y)

    # create the scatter plot
    figure = go.Figure(data=[go.Scatter(x=x, y=y, mode='markers')])

    return figure

# # callback to calculate the sum
# @app.callback(
#     Output(component_id = 'sum-state', component_property = 'children'),
#     Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
#     State('table', 'data'))
# def update_sum(data):
#     # calculate the sum of all numbers in the table
#     print(data)
#     # total = sum([row['x'] + row['y'] for row in data])

#     return 'The total sum equals'
@app.callback(
    Output(component_id = 'sum-state', component_property = 'children'),
    Input(component_id = 'table', component_property = 'data'))
def update_scatterplot(data):
    x = [d['x'] for d in data]
    y = [d['y'] for d in data]

    total = sum(x) + sum(y)
    print('The total sum is: ', total)

    return total


if __name__ == '__main__':
    app.run_server(debug=True)






