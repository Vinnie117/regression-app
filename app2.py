from dash import Dash, dcc, html, dash_table, Output, Input, State
from dash.dash_table.Format import Format
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd


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

        # left column
        html.Div([

            # create the data table
            dash_table.DataTable(
                id='table',
                columns=[
                    {
                        'name': 'x', 
                        'id': 'x', 
                        'type': 'numeric',
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'renamable': False
                    }, 
                    {
                        'name': 'y', 
                        'id': 'y', 
                        'type': 'numeric',
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'renamable': False
                    },
                    {
                        'name': 'z', 
                        'id': 'z', 
                        'type': 'numeric',
                        'format': Format(nully='N/A'),
                        'on_change': {'action': 'coerce', 'failure': 'default'},
                        'deletable': True,
                        'renamable': True
                    }
                    ],
                data=data,
                editable=True,
                fill_width=False,
                virtualization=True,  # make datatable scrollable
                style_cell={'width': '100px'}  # width of columns
                ),
            
            html.Button(
                id='submit-button-state', 
                children='Submit', 
                type='button', 
                style={'margin-top': '20px'}  # space between the button and the table below
                ), 

            html.Div(children = [

                html.Div([

                    html.P('Target variable'),

                    dcc.RadioItems(
                    id = 'target',
                    options=[],  # will be filled by callback
                    value = '',
                    labelStyle={
                        'display': 'block', 
                        'margin-top': '20px'
                    } # display gives a vertical list of radio items, margin top increases spacing between items
                    )
                ], style={
                    'display': 'inline-block',
                    'border': '1px dashed black'
                    }
                ), 

                html.Div([
            
                    html.P('Predictor variables'),

                    dcc.Checklist(
                        id = 'predictors',
                        options=[],  # will be filled by callback
                        labelStyle={
                            'display': 'block', 
                            'margin-top': '20px'
                            
                        } # display gives a vertical list of radio items, margin top increases spacing between items
                    )
                ], style={
                    'display': 'inline-block',
                    'border': '1px dashed black',
                    'margin-top': '20px',
                    'margin-left': '20px'
                    }
                )
            ])
        ], style={
            'display': 'inline-block',  # display elements (children) side by side
            'width': '25%',  # percentage of screen width taken by div
            'border': '1px dashed black',  # border (for debugging)          
            }
        ),

        # middle column
        html.Div([

            # create the scatter plot
            dcc.Graph(id='scatterplot', style={'width': '100%', 'height': '100%'})
        ], style={
            'display': 'inline-block', 
            'width': '49%', 
            'border': '1px dashed black'
            }
        ),

        # create the div that will display the sum of all numbers in the table
        html.Div(
            id='sum-state',
            style={
            'display': 'inline-block', 
            'width': '20%', 
            'border': '1px dashed black',
            }
        ),

    ], style={'display': 'flex', 'align-items': 'top'}),  # vertically align the children
    

])



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
    figure.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    return figure


# dynamically adjust list of radio items for target given table vars
@app.callback(
    Output('target', 'options'),
    Input('table', 'columns'))
def update_radio_items(columns):
    column_names = [i['name'] for i in columns]
    return column_names

# dynamically adjust list of radio items for predictors given table vars
@app.callback(
    Output('predictors', 'options'),
    Input('table', 'columns'))
def update_radio_items(columns):
    column_names = [i['name'] for i in columns]
    return column_names


# callback for logic with data - here to calculate the sum of all values
@app.callback(
    Output(component_id = 'sum-state', component_property = 'children'),
    State(component_id = 'table', component_property = 'data'),
    State(component_id = 'target', component_property = 'value'),
    State(component_id = 'predictors', component_property = 'value'),
    Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
    prevent_initial_call=True
    )
def update_sum(data, target_var, predictor_vars, n_clicks,): # order of arguments in order of classes after 'Output'

    # data is a list of dicts: [{'x': 0, 'y': 0, 'z': 7}, {'x': 1, 'y': 1, 'z': 2}, ....]
    x = [d['x'] for d in data]
    y = [d['y'] for d in data]
    z = [d['z'] for d in data]

    total = sum(x) + sum(y) + sum(z)
    #print('The total sum is: ', total)

    result = 'The total sum is:\n{total}'.format(total = total) 

    #### regression
    #print(data)
    df = pd.DataFrame(data)

    # print(df)
    print(target_var)
    print(predictor_vars)

    lm = sm.OLS(data = df, endog=df[target_var], exog=df[predictor_vars])
    lm_results = lm.fit()

    # lm_results_regression = lm_results.summary().tables[0]
    lm_results_parameters = lm_results.summary().tables[1]
    # lm_results_distribution = lm_results.summary().tables[2]
    df_results_parameters = pd.DataFrame(lm_results_parameters)

    print(df_results_parameters)
    # print(test.iloc[0,1]) # coef
    coef = str(df_results_parameters.iloc[1,1]) # coef value

    return result + 'Regression coef is: {}'.format(coef) 


if __name__ == '__main__':
    app.run_server(debug=True)






