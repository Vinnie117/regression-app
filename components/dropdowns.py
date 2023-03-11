from dash import  dcc, html
import pandas as pd
from assets.data_table import data_table
from dash.dependencies import Input, Output, State
from dash_app import dash_app


dropdowns = html.Div([
    html.Div([
        dcc.Dropdown(
            options = list(pd.DataFrame(data_table)),
            value='y',
            placeholder="Y-Achse",
            id='yaxis-column'
        )], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Dropdown(
            options = list(pd.DataFrame(data_table)),
            value='x',
            placeholder="X-Achse",
            id='xaxis-column'
        )], style={'width': '48%', 'display': 'inline-block'}
    )
], style={
    'width': '77%',
    'margin-left': 'auto', 
    'margin-right': 'auto',
})


# callback for scatterplot axis selection
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
    Input(component_id = 'submit-button-state', component_property = 'n_clicks'),
    prevent_initial_call=True)
def update_axis_by_submit(predictor, target, n_clicks):
    return predictor, target