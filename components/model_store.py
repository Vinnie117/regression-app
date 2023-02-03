from dash import dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash_app import dash_app
import statsmodels.api as sm
import pandas as pd
import numpy as np
import sys

model_store = dcc.Store(id='regression_results')

# callback to calculate regression
@dash_app.callback(
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

    # check which component_id was triggered
    input_id = callback_context.triggered_id
    # print(input_id) 
    # print(type(input_id))

    #### remove experiment from model store
    if all(key in input_id for key in ["index", "type"]):
        #input_id = ast.literal_eval(input_id)
        delete_chart = input_id["index"]

        # remove html child div from list
        children = [chart for chart in children if "'index': " + str(delete_chart) not in str(chart)]

        # update dict in Store that experiment was deleted:
        delete = 'experiment_' + str(delete_chart)
        print(delete)
        if delete not in children:
            del regression_dict[delete]
        
        return regression_dict

    # the case when new models are to be submitted
    else:
        df = pd.DataFrame(data)

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

        return regression_dict