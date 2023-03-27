
from dash import html, callback_context, dash_table
from dash.dependencies import Input, Output, State, ALL
from dash_app import dash_app
import pandas as pd

    
# Extract html results!
results = html.Div(
            id='results',
            className="results",
            children = [],
        )

@dash_app.callback(
    Output(component_id = 'results', component_property = 'children'),
    State(component_id='results', component_property='children'),
    Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
    Input(component_id = 'regression_results', component_property = 'data'),
    Input({"type": "dynamic-delete", "index": ALL}, "n_clicks"),
    Input('warning_msg', 'cancel_n_clicks'),
    Input('warning_msg', 'submit_n_clicks'),
    prevent_initial_call=True
)
def show_results(children, n_clicks, regression_dict, _, cancel, submit):

    # fetch which input triggered the callback
    input_id = callback_context.triggered_id

    # if block is triggered by clicking on X
    if all(key in input_id for key in ["index", "type"]):
        delete_chart = input_id["index"]

        # remove html child div from list
        children = [chart for chart in children if "'index': " + str(delete_chart) not in str(chart)]
        return children

    # cancel button was clicked
    if cancel:
        return children


    # Construct results to display
    experiment_runs = str(list(regression_dict)[-1])
    run_number = experiment_runs.split("experiment_")[1:]
    run_name = "Modell " + run_number[0]

    df_results_parameters = pd.DataFrame.from_dict(regression_dict[experiment_runs]['results'], orient='index')

    df_results_parameters.index = df_results_parameters.index.astype(str).str.replace('!_dummy_!', ': ')
    df_results_parameters.index = df_results_parameters.index.astype(str).str.replace('!_onehot_!', ': ')

    result_table = df_results_parameters.reset_index(names='')


    #### appending divs to results html
    new_element = html.Div(
        children=[html.Details(open=True, children=[
            html.Summary(children=[
                run_name,
                html.Button("X", 
                            id={"type": "dynamic-delete","index": n_clicks},
                            n_clicks=0,style={"float": "right"}
                            )
                        ]
                ),
            html.Div([
                dash_table.DataTable(result_table.to_dict('records'),
                                        [{"name": i, "id": i} for i in result_table.columns])
            ])
            ])
        ], 
        style={'margin-bottom': '5%'}
    )

    children.append(new_element)
    return children