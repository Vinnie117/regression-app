from dash import Dash, dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash.dash_table.Format import Format
import plotly.express as px
import statsmodels.api as sm
import pandas as pd
import json
from components.data_table import data_table



dash_app = Dash()

dash_app.layout = html.Div([
        
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

            html.Div([

                html.P('Target variable'),

                dcc.Dropdown(
                    id = 'target',
                    options=[],
                    value = '',
                ),

            ], style={
                #'display': 'inline-block',
                'margin-top': '30px',
                'border': '1px dashed black'
                }
            ),

            html.Div([
        
                html.P('Predictor variable'),

                dcc.Dropdown(
                    id = 'predictors',
                    options=[],
                    value = ''            
                )
            ], style={
                #'display': 'inline-block',
                'border': '1px dashed black',
                'margin-top': '30px',
                #'margin-left': '20px'
                }
            ),
            
            html.Div([

                html.P('Control variables'),
                
                dcc.Checklist(
                    id = 'controls',
                    options=[],
                    value=[''],
                    labelStyle= {
                        'display': 'block'
                    }               
                )

            ])
            
            ,          
        ], style={
            'display': 'inline-block',  # display elements (children) side by side
            'width': '10%',  # percentage of screen width taken by div
            'border': '1px dashed black',  # border (for debugging)          
            }
        ),

        # middle column
        html.Div(children = [

            # create the data table
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
                        },
                        {
                             'name': 'a', 
                            'id': 'a', 
                            'type': 'numeric',
                            'format': Format(nully='N/A'),
                            'on_change': {'action': 'coerce', 'failure': 'default'},
                            'deletable': True,
                            'renamable': True
                        }                       
                        ],
                    data=data_table,
                    editable=True,
                    fill_width=False,
                    virtualization=True,  # make datatable scrollable
                    style_cell={'width': '100px'} # width of columns
                    
                ), style={
                    'text-align': 'center', 
                    'width': '77%', 
                    'margin-left': 'auto', 
                    'margin-right': 'auto',
                    'border': '1px solid black'
                }
            ),

            # visualization
            html.Div(children = [

                html.Div([

                    dcc.Dropdown(
                        options = list(pd.DataFrame(data_table)),
                        value='y',
                        placeholder="Y-Achse",
                        id='yaxis-column'
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        options = [],
                        value = 'x',
                        placeholder="X-Achse",
                        id='xaxis-column'
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),
            
                # create the scatter plot
                dcc.Graph(id='scatterplot')
            ], style={
                'margin-top': '50px'
            }
        )

        ], style={
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
            
            'width': '27%', 
            'border': '1px dashed black',
            }
        )

    ], style={'display': 'flex', 'align-items': 'top'}),  # vertically align the children
    

])


###########################################################################################

def create_plot(df, x, y):
    
    plot = px.scatter(df, x=x, y=y)
    plot.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    return plot

###########################################################################################


# callback to update the scatter plot given changes
@dash_app.callback(
    Output(component_id = 'scatterplot', component_property = 'figure'),
    Input(component_id = 'table', component_property = 'data'),
    Input(component_id = 'xaxis-column', component_property = 'value'),
    Input(component_id = 'yaxis-column', component_property = 'value'))
def update_scatterplot(data, x_axis, y_axis):
    x = [d['x'] for d in data]
    y = [d['y'] for d in data]

    print("X is: ", x, '\n', "Y is: ", y)

    data = pd.DataFrame(data)
    fig = create_plot(data, x_axis, y_axis)

    return fig

# callbacks for scatterplot axis selection
@dash_app.callback(
    Output('xaxis-column', 'options'),
    Output('yaxis-column', 'options'),
    Input('table', 'columns'))
def update_radio_items(columns):
    column_names = [i['name'] for i in columns]
    return column_names, column_names


# callback for target variable selection
@dash_app.callback(
    Output('target', 'options'),
    Input('table', 'columns'),
    Input('predictors', 'value'),
    Input('controls', 'value')
    )
def update_target(columns, predictor_var, control_vars):
    control_vars = ",".join(string for string in control_vars if len(string) > 0)
    column_names = [i['name'] for i in columns if i['name'] not in [control_vars, predictor_var]]
    return column_names

# callback for predictor variable selection
@dash_app.callback(
    Output('predictors', 'options'),
    Input('table', 'columns'),
    Input('target', 'value'),
    Input('controls', 'value')
    )
def update_predictor(columns, target_var, control_vars):
    control_vars = ",".join(string for string in control_vars if len(string) > 0)
    column_names = [i['name'] for i in columns if i['name'] not in [control_vars, target_var]]
    return column_names


# callback for control variable selection
@dash_app.callback(
    Output('controls', 'options'),
    Input('table', 'columns'),
    Input('predictors', 'value'),
    Input('target', 'value')
    )
def update_controls(columns, predictor_var, target_var):
    column_names = [i['name'] for i in columns if i['name'] not in [predictor_var, target_var]]
    return column_names


# callback to calculate regression
@dash_app.callback(
    Output(component_id = 'results', component_property = 'children'),
    State(component_id = 'table', component_property = 'data'),
    State(component_id = 'target', component_property = 'value'),
    State(component_id = 'predictors', component_property = 'value'),
    State(component_id = 'controls', component_property = 'value'),
    State(component_id='results', component_property='children'),
    [
        Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
        Input({"type": "dynamic-delete", "index": ALL}, "n_clicks")       
    ],
    prevent_initial_call=True
    )
def calculate_regression(data, target_var, predictor_var, control_vars,children, n_clicks, _): # order of arguments in order of classes after 'Output'

    df = pd.DataFrame(data)

    # print(df)
    # print(target_var)
    # print(predictor_var)
    # print(control_vars)

    control_vars = [item for item in control_vars if len(item)>0]
    x_vars = [predictor_var] + control_vars

    X = sm.add_constant(df[x_vars])  # intercept must be added manually
    lm = sm.OLS(data = df, endog=df[target_var], exog=X)
    lm_results = lm.fit()

    #### Prediction
    #import numpy as np
    
    # df_results_regression = lm_results.summary().tables[0].as_html()
    # df_results_regression = pd.read_html(df_results_regression, header=0, index_col=0)[0]
    # print(df_results_regression)
    # df_results_distribution = lm_results.summary().tables[2].as_html()

    df_results_parameters = lm_results.summary().tables[1].as_html()
    df_results_parameters = pd.read_html(df_results_parameters, header=0, index_col=0)[0]
    print(df_results_parameters)


    #### Extracting the results from df
    list_coefs = df_results_parameters['coef'].tolist()
    result = 'Experiment {number}: Regression '.format(number = n_clicks)

    x_vars = list(x_vars)
    x_vars.insert(0, 'const')
        
    list_results = []
    for var, coef in zip(x_vars, list_coefs):
        list_results.append('coef of {var} is {coef}'. format(var=var, coef=coef))
    
    print(list_results)

    results_string = result + ', '.join(list_results)


    #### appending / removing divs to results html
    input_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    # print(input_id)

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
    dash_app.run_server(debug=True)





