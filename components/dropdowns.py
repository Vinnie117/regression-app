from dash import  dcc, html, callback_context
import pandas as pd
from assets.data_table import data_table, empty_data_table
from dash.dependencies import Input, Output, State
from dash_app import dash_app


dropdowns = html.Div(className="dropdowns",
    children=[
        html.Div(
        className="single_dropdown", 
        children=[
            dcc.Dropdown(
                options = [],
                value='',
                placeholder="X-Achse",
                id='xaxis-column'
            )]
        ),
        html.Div(
            className="single_dropdown", 
            children=[
                dcc.Dropdown(
                    options = [],
                    value='',
                    placeholder="Y-Achse",
                    id='yaxis-column'
            )]
        )

])


# callback for scatterplot axis selections
@dash_app.callback(
    Output('xaxis-column', 'options'),
    Output('yaxis-column', 'options'),
    Input('table', 'columns'))
def update_radio_items(columns):

    column_names = [i['name'] for i in columns]

    return column_names, column_names


# callback to adjust selected dropdown menu after submitting regression
@dash_app.callback(
    Output('xaxis-column', 'value'),
    Output('yaxis-column', 'value'),
    State('predictors', 'value'),
    State('target', 'value'),
    Input('submit-button-state', 'n_clicks'),
    Input('table', 'columns'),
    prevent_initial_call=True)
def update_axis_by_submit(predictor, target, n_clicks, columns):

    # if new external data uploaded
    if callback_context.triggered_id == 'table':
        column_names = [i['name'] for i in columns]
        predictor = column_names[0]
        target = column_names[1]
    # if regression, select its predictor and target
    elif callback_context.triggered_id == 'submit-button-state':
        pass
    # default case
    else:
        predictor = 'x'
        target = 'y'


    return predictor, target