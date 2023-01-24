from dash import Dash, dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash.dash_table.Format import Format
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import json
from components.data_table import data_table
from traceinfo import TraceInfo



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
                dcc.Graph(
                    id='scatterplot',
                    # figure=dict(
                    #     data=[{'x': [],
                    #            'y': [],
                    #             'mode':'markers'
                    #         }]
                    # )
                )
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
    
    dcc.Store(id='regression_results')
])


###########################################################################################

# def create_plot(x, y):
    
#     # plot = px.scatter(df, x=x, y=y)
#     # plot.update_layout(margin=dict(l=20, r=20, t=20, b=20))

#     plot = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))
#     plot.update_layout(margin=dict(l=20, r=20, t=20, b=20))

#     return plot

###########################################################################################


# callback to update the scatter plot given changes
@dash_app.callback(
    Output(component_id = 'scatterplot', component_property = 'figure'),
    Input(component_id = 'table', component_property = 'data'),
    Input(component_id = 'xaxis-column', component_property = 'value'),
    Input(component_id = 'yaxis-column', component_property = 'value'),
    Input(component_id = 'regression_results', component_property = 'data'),
    Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
    State('scatterplot', 'figure'))
def update_scatterplot(data, x_axis_name, y_axis_name, model, n_clicks, current_figure):
    
    # Initial plot upon page load
    if not current_figure or len(current_figure.get('data')) == 0:
        trace_name = 'experiment_0'

        trace = go.Scatter(
            x=[d[x_axis_name] for d in data],
            y=[d[y_axis_name] for d in data],
            mode='markers',
            marker={'color': '#636EFA'},
            name=trace_name
        )

        plot = go.Figure(data=trace, layout={'showlegend': False})
        plot.update_layout(margin=dict(l=20, r=20, t=20, b=20))


        return plot

    # the following code is executed, if there is a current figure with at least one
    # trace in it.

    # set fixed color map for OLS lines
    color_map = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

    # get trace info
    t = TraceInfo(current_figure)
    current_traces = t.traces

    # differences between current selection and current figure. The trace names correspond
    # to the column names. This has to be guaranteed.
    existing = set(t.names)

    selected = list(model.keys())
    selected.insert(0, 'experiment_0')
    selected = set(selected)

    # decide what to do, which traces to keep, to delete and which to create
    keep = existing & selected
    delete = existing ^ keep
    new = keep ^ selected

    # get indices of traces to delete
    d_index = [t.names.index(d) for d in delete]

    # get the indices of the trace color which are kept
    # Trace names and colors have the same indices
    c_index = [t.names.index(k) for k in keep]

    # now that we have the index of the colors, we need to know the color name
    used_colors = {t.colors[i] for i in c_index}

    # usable colors are the colors of the initial color map
    # minus the colors which are already used by traces kept
    usable_colors = iter(
        sorted(
            list(used_colors ^ set(color_map)),
            key=color_map.index
        )
    )

    # delete traces to be deleted from current traces
    # sort the indices in descending order
    for i in sorted(d_index, reverse=True):
        current_traces.pop(i)

    # create new traces
    new_traces = []
    for run in new:
        new_traces.append(
            go.Scatter(
                x=model[run]['x_range'],
                y=model[run]['y_range'],
                mode='lines',
                marker={'color': next(usable_colors)},
                name=run
            )
        )
    # create figure with current traces +  the new ones
    return go.Figure(data=current_traces + new_traces, layout={'showlegend': True})


# callback for scatterplot axis selection
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
    Output(component_id = 'regression_results', component_property = 'data'),  # dcc.Store
    State(component_id = 'table', component_property = 'data'),
    State(component_id = 'target', component_property = 'value'),
    State(component_id = 'predictors', component_property = 'value'),
    State(component_id = 'controls', component_property = 'value'),
    State(component_id='results', component_property='children'),
    State(component_id = 'regression_results', component_property = 'data'),  # dcc.Store
    [
        Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
        Input({"type": "dynamic-delete", "index": ALL}, "n_clicks")   
    ],
    prevent_initial_call=True
    )
def calculate_regression(data, target_var, predictor_var, control_vars,children, regression_dict,n_clicks, _): # order of arguments in order of classes after 'Output'

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

    # for the plot
    x_range = np.linspace(df[predictor_var].min(), df[predictor_var].max(), 100)

    # for the model
    predictor_space = np.linspace(df[x_vars].min(), df[x_vars].max(), 100)
    x_range_with_const = sm.add_constant(predictor_space)

    # Partial regression plot: Set all controls to value 0 -> see multivariate regression equation
    if x_range_with_const.shape[1] >= 2:
        x_range_with_const[:,2:] = 0

    y_range = lm_results.predict(x_range_with_const)

    # Create / append dict for storing multiple runs
    experiment_runs = 'experiment_' + str(n_clicks)
    if regression_dict == None:
        regression_dict = {}
    regression_dict[experiment_runs] = {'x_range': x_range, 'y_range': y_range}

    
    # df_results_regression = lm_results.summary().tables[0].as_html()
    # df_results_regression = pd.read_html(df_results_regression, header=0, index_col=0)[0]
    # print(df_results_regression)
    # df_results_distribution = lm_results.summary().tables[2].as_html()
    df_results_parameters = lm_results.summary().tables[1].as_html()

    # Replacing column names in HTML
    df_results_parameters = df_results_parameters.replace("coef", "BANANA")
    
    # formatting the HTML table -> BeautifulSoup
    df_results_parameters = df_results_parameters.replace(
        '<table class="simpletable">',
        '<table class="simpletable" border="1" style="border-collapse: collapse;">'
    )
    # print(df_results_parameters)

    df_results_parameters = pd.read_html(df_results_parameters, header=0, index_col=0)[0]
    print(df_results_parameters)

    # passing regression results to store
    regression_dict[experiment_runs]['predictor_var'] = predictor_var
    regression_dict[experiment_runs]['results'] = df_results_parameters.to_dict('index')
    
    print(regression_dict)

    ######################################################################################

    #### Extracting the results from df
    list_coefs = df_results_parameters.iloc[:,0].to_list()
    result = 'Experiment {number}: Regression '.format(number = n_clicks)

    x_vars = list(x_vars)
    x_vars.insert(0, 'const')
        
    list_results = []
    for var, coef_value in zip(x_vars, list_coefs):
        list_results.append('coef of {var} is {coef_value}'. format(var=var, coef_value=coef_value))
    
    print(list_results)

    results_string = result + ', '.join(list_results)


    #### appending / removing divs to results html

    input_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    # print(input_id)

    # if block is triggered by clicking on X
    if "index" in input_id:
        print(input_id)
        delete_chart = json.loads(input_id)["index"]
        print(delete_chart)
        print(children)

        # remove html child div from list
        children = [chart for chart in children if "'index': " + str(delete_chart) not in str(chart)]
        print(children)

        # update dict in Store that experiment was deleted:
        delete = 'experiment_' + str(delete_chart)
        print(delete)
        if delete not in children:
            del regression_dict[delete]

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
                    id = {"type": "dynamic-output", "index": n_clicks, "run":experiment_runs}
                )
            ]
        )
        children.append(new_element)

    return children, regression_dict


if __name__ == '__main__':
    dash_app.run_server(debug=True)





