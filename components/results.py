
from dash import html, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash_app import dash_app
import pandas as pd

# Extract html results!
results = html.Div(
            id='results',
            children = [],
            style={
            'width': '27%', 
            'border': '1px dashed black',
            }
        )

@dash_app.callback(
    Output(component_id = 'results', component_property = 'children'),
    State(component_id='results', component_property='children'),
    Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
    Input(component_id = 'regression_results', component_property = 'data'),
    Input({"type": "dynamic-delete", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def show_results(children, n_clicks, regression_dict, _):

    input_id = callback_context.triggered_id
    # print(input_id)
    # print(type(input_id))

    # if block is triggered by clicking on X
    if all(key in input_id for key in ["index", "type"]):
        delete_chart = input_id["index"]

        # remove html child div from list
        children = [chart for chart in children if "'index': " + str(delete_chart) not in str(chart)]
        return children

    else:
        experiment_runs = 'experiment_' + str(n_clicks)

        df_results_parameters = pd.DataFrame.from_dict(regression_dict[experiment_runs]['results'], orient='index')
        x_vars = list(df_results_parameters.index.values)
        list_coefs = df_results_parameters.iloc[:,0].to_list()

        print(df_results_parameters)

        list_results = []
        for var, coef_value in zip(x_vars, list_coefs):
            list_results.append('coef of {var} is {coef_value}'. format(var=var, coef_value=coef_value))

        result = 'Experiment {number}: Regression '.format(number = n_clicks)
        results_string = result + ', '.join(list_results)

        #### appending divs to results html

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

        return children