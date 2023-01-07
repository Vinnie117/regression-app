from dash import Dash, dcc, html, dash_table, Output, Input, State
from dash.dash_table.Format import Format
import plotly.graph_objects as go

app = Dash()

data = [
        {'x': 0, 'y': 0, 'z': 7},
        {'x': 1, 'y': 1, 'z': 2},
        {'x': 2, 'y': 2, 'z': 0},
        {'x': 3, 'y': 3, 'z': 4},
        {'x': 4, 'y': 4, 'z': 5},
        {'x': 2, 'y': 5, 'z': 9},
        {'x': 3, 'y': 4, 'z': 6}
]

app.layout = html.Div([
        
    # a header for the webpage
    html.H1('My Dash App'),

    # a submit button
    #html.Button(id='submit-button-state', children='Submit', type='button'),


    html.Div(children = [

        # create the data table
        html.Div([

            html.Button(id='submit-button-state', children='Submit', type='button'), 
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
                    },
                    {
                        'name': 'z', 
                        'id': 'z', 
                        'type': 'numeric',
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'}
                    }
                    ],
                data=data,
                editable=True,
                fill_width=False,
                style_cell={'width': '10%'}
                )
            
        ], style={
            'display': 'inline-block',  # display elements (children) side by side
            'width': '19%',  # percentage of screen width taken by div
            'border': '1px solid black',  # border (for debugging)
            
            }
        ),

        # create the scatter plot
        html.Div([
            dcc.Graph(id='scatterplot', style={'width': '100%', 'height': '100%'})
        ], style={
            'display': 'inline-block', 
            'width': '49%', 
            'border': '1px solid black',
            }
        )
    ], style={'display': 'flex', 'align-items': 'center'}),  # vertically align the children
    
     # create the div that will display the sum of all numbers in the table
    html.Div(id='sum-state')
])

# Child divs müssen beide inline-blocks haben

###########################################################################################



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

# callback for logic with data - here to calculate the sum of all values
@app.callback(
    Output(component_id = 'sum-state', component_property = 'children'),
    State(component_id = 'table', component_property = 'data'),
    Input(component_id = 'submit-button-state', component_property = 'n_clicks'))
def update_sum(data, n_clicks):

    # data is a list of dicts: [{'x': 0, 'y': 0, 'z': 7}, {'x': 1, 'y': 1, 'z': 2}, ....]
    x = [d['x'] for d in data]
    y = [d['y'] for d in data]
    z = [d['z'] for d in data]

    total = sum(x) + sum(y) + sum(z)
    print('The total sum is: ', total)

    return f'The total sum is: {total}'


if __name__ == '__main__':
    app.run_server(debug=True)






