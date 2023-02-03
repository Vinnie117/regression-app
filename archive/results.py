
from dash import html, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash_app import dash_app
import statsmodels.api as sm
import pandas as pd
import numpy as np
import json
import sys

results = html.Div(
            id='results',
            children = [],
            style={
            'width': '27%', 
            'border': '1px dashed black',
            }
        )

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
    x_range = np.linspace(df[predictor_var].min(), df[predictor_var].max(), 10)

    # for the model
    predictor_space = np.linspace(df[x_vars].min(), df[x_vars].max(), 10)
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
    regression_dict[experiment_runs]['target_var'] = target_var
    regression_dict[experiment_runs]['results'] = df_results_parameters.to_dict('index')
    
    print(regression_dict)
    print("The size of the regression_dictionary is {} bytes".format(sys.getsizeof(regression_dict)))  # 232 Bytes

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
    print(input_id)

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