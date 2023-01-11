from dash import Dash, dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash.dash_table.Format import Format
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import json



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

    html.Div(children = [

        # left column
        html.Div([
            
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
            'width': '15%',  # percentage of screen width taken by div
            'border': '1px dashed black',  # border (for debugging)          
            }
        ),

        # middle column
        html.Div(children = [

            html.Div(

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
                    style_cell={'width': '100px'} # width of columns
                    
                ), style={
                    'text-align': 'center', 
                    'width': '50%', 
                    'margin-left': 'auto', 
                    'margin-right': 'auto'
                }
            ),
            # create the data table


            # create the scatter plot
            dcc.Graph(id='scatterplot')
        ], style={
            'display': 'inline-block', 
            'width': '55%', 
            'border': '1px dashed black'
            }
        ),

        # right column
        # create the div that will display the regression results
        html.Div(
            id='results',
            children = [],
            style={
            
            'width': '25%', 
            'border': '1px dashed black',
            }
        )

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
    Output(component_id = 'results', component_property = 'children'),
    State(component_id = 'table', component_property = 'data'),
    State(component_id = 'target', component_property = 'value'),
    State(component_id = 'predictors', component_property = 'value'),
    State(component_id='results', component_property='children'),
    [
        Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
        Input({"type": "dynamic-delete", "index": ALL}, "n_clicks")       
    ],
    prevent_initial_call=True
    )
def calculate_regression(data, target_var, predictor_vars, children, n_clicks, _): # order of arguments in order of classes after 'Output'

    df = pd.DataFrame(data)

    # print(df)
    # print(target_var)
    # print(predictor_vars)

    lm = sm.OLS(data = df, endog=df[target_var], exog=df[predictor_vars])
    lm_results = lm.fit()

    # df_results_regression = lm_results.summary().tables[0].as_html()
    # df_results_distribution = lm_results.summary().tables[2].as_html()
    df_results_parameters = lm_results.summary().tables[1].as_html()
    df_results_parameters = pd.read_html(df_results_parameters, header=0, index_col=0)[0]

    print(df_results_parameters)

    #### Extracting the results from df
    list_coefs = df_results_parameters['coef'].tolist()

    result = 'Experiment {number}: Regression '.format(number = n_clicks)
    list_results = []
    for var, coef in zip(predictor_vars, list_coefs):
        list_results.append('coef of {var} is {coef}'. format(var=var, coef=coef))
    
    # print(list_results)

    results_string = result + ', '.join(list_results)


    #### appending / removing divs to results html
    input_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    print(input_id)

    # if block is triggered by clicking on X
    if "index" in input_id:
        delete_chart = json.loads(input_id)["index"]
        children = [
            chart
            for chart in children
            if "'index': " + str(delete_chart) not in str(chart)
        ]

    # otherwise, new experiment results can be appended
    else:
        new_element = html.Div(
            children=[
                html.Button(
                    "X",
                    id={"type": "dynamic-delete", "index": n_clicks},
                    n_clicks=0,
                    style={"display": "block"},
                ),
                html.Div(
                    results_string,
                    id = {"type": "dynamic-output", "index": n_clicks}
                )
            ]
        )
        children.append(new_element)


    return children


if __name__ == '__main__':
    app.run_server(debug=True)






