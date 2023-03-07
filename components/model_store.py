from dash import dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash_app import dash_app
import statsmodels.api as sm
import pandas as pd
import numpy as np
import sys
from utils.data_prep import dummy_vars, numeric_converter, cat_inference, drop_minority_type


model_store = dcc.Store(id='regression_results')

# callback to calculate regression
@dash_app.callback(
    Output(component_id = 'regression_results', component_property = 'data'),  # dcc.Store
    Output(component_id = 'counter', component_property = 'data'),  # dcc.Store
    State(component_id = 'table', component_property = 'data'),
    State(component_id = 'target', component_property = 'value'),
    State(component_id = 'predictors', component_property = 'value'),
    State(component_id = 'controls', component_property = 'value'),
    State(component_id = 'encoding', component_property = 'value'),
    State(component_id='results', component_property='children'),
    State(component_id = 'regression_results', component_property = 'data'),  # dcc.Store
    State(component_id = 'counter', component_property = 'data'),  # dcc.Store
    Input('warning_msg', 'cancel_n_clicks'),
    [
        Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
        Input({"type": "dynamic-delete", "index": ALL}, "n_clicks")   
    ],
    prevent_initial_call=True
    )
def calculate_regression(data, target_var, predictor_var, control_vars, encoding,
                        children, regression_dict, counter ,cancel, n_clicks, _): # order of arguments in order of classes after 'Output'

    # check which component_id was triggered
    input_id = callback_context.triggered_id

    # Create / append dict for storing multiple runs
    if regression_dict == None:
        regression_dict = {}

    # to track experiments
    if counter == None:
        counter = 0
    
    #### remove experiment from model store
    if all(key in input_id for key in ["index", "type"]):
        delete_chart = input_id["index"]

        # remove html child div from list
        children = [chart for chart in children if "'index': " + str(delete_chart) not in str(chart)]

        # update dict in Store that experiment was deleted:
        delete = 'experiment_' + str(delete_chart)
        print(delete)
        if delete not in children:
            del regression_dict[delete]
        
        return regression_dict, counter

    # cancel button was clicked
    if cancel:
        return regression_dict, counter
    

    # the case when new models are to be submitted and no warning message appeared
    else:

        df = pd.DataFrame(data)

        print(df)

        control_vars = [item for item in control_vars if len(item)>0]
        x_vars = [predictor_var] + control_vars

##########################################################################

        # check NaNs and drop rows if necessary
        if df[[target_var] + x_vars].isnull().values.any():   
            df=df.dropna()


        df = drop_minority_type(df, [target_var] + x_vars)


        # for the plot
        if df[predictor_var].dtypes == 'object':
            x_range = df[predictor_var].unique().tolist()
        else:
            x_range = np.linspace(df[predictor_var].min(), df[predictor_var].max(), 10)

        print(x_range)
        
        cat_cols = []
        for i in df.select_dtypes(include=['object']).columns:
            if i in x_vars:
                cat_cols.append(i)

        num_cols = [col for col in x_vars if col not in cat_cols]  # numeric predictor vars


        # dummy encoding for categorical variables
        # By default, pandas sorts the categories in ascending order 
        # (based on the alphabetical order of the category labels), and the 
        # first category in the sorted list is dropped.
        if encoding == 'Dummy Codierung':
            df = pd.get_dummies(df, columns=cat_cols, prefix=cat_cols, prefix_sep='!_dummy_!', drop_first=True)

            # extract all dummy columns that are part of predictor variables
            x_vars = dummy_vars(df, cat_cols, num_cols, '!_dummy_!')


        elif encoding == 'One-Hot Codierung':
            
            df = pd.get_dummies(df, columns=cat_cols, prefix=cat_cols, prefix_sep='!_onehot_!', drop_first=False)
            x_vars = dummy_vars(df, cat_cols, num_cols, '!_onehot_!')

        # print(x_vars)
        print(df)
        print(df.dtypes)


        X = sm.add_constant(df[x_vars])  # intercept must be added manually
        lm = sm.OLS(data = df, endog=df[target_var], exog=X)
        lm_results = lm.fit()

        #### Prediction for the model

        # hacky way of saying that predictor is numeric (bc non-numeric predictors are dropped after encoding)
        if predictor_var in list(df.columns):
            predictor_space = np.linspace(df[x_vars].min(), df[x_vars].max(), 10)
            print(predictor_space)
            predictor_space_with_const = sm.add_constant(predictor_space)
            print(predictor_space_with_const)

            # Partial regression plot: Set all controls to value 0 -> see multivariate regression equation
            if predictor_space_with_const.shape[1] >= 2:
                predictor_space_with_const[:,2:] = 0

            y_range = lm_results.predict(predictor_space_with_const)

        # predictor is categorical
        else:
            print('it is object!!')
            print(x_range)

            if encoding == 'Dummy Codierung':
                predictor_space_with_const = cat_inference(x_range, control_vars, True)

            elif encoding == 'One-Hot Codierung':
                predictor_space_with_const = cat_inference(x_range, control_vars, False)

            y_range = lm_results.predict(predictor_space_with_const).tolist()


        # df_results_regression = lm_results.summary().tables[0].as_html()
        # df_results_regression = pd.read_html(df_results_regression, header=0, index_col=0)[0]
        # print(df_results_regression)
        # df_results_distribution = lm_results.summary().tables[2].as_html()
        df_results_parameters = lm_results.summary().tables[1].as_html()       

        df_results_parameters = pd.read_html(df_results_parameters, header=0, index_col=0)[0]
        print(df_results_parameters)


        # passing regression results to store
        # Create / append dict for storing multiple runs
        counter = counter + 1
        experiment_runs = 'experiment_' + str(counter)
        regression_dict[experiment_runs] = {'x_range': x_range, 'y_range': y_range}

        regression_dict[experiment_runs]['predictor_var'] = predictor_var
        regression_dict[experiment_runs]['target_var'] = target_var
        regression_dict[experiment_runs]['results'] = df_results_parameters.to_dict('index')
        
        print(regression_dict)
        print("The size of the regression_dictionary is {} bytes".format(sys.getsizeof(regression_dict)))  # 232 Bytes

        return regression_dict, counter