from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
from dash_app import dash_app
import dash_bootstrap_components as dbc
from assets.data_table import empty_data_table
import pandas as pd
import numpy as np

variable_selection = html.Div(
    
    className="left-column",
    children=[

        html.Button(
            id='submit-button-state',
            className="submit-button-state",
            children='Berechnen', 
            type='button', 
            ), 

        html.Div(
            className = "variable_selection",
            children=[

                html.P('Zielvariable'),

                dcc.Dropdown(
                    id = 'target',
                    options=[],
                    value = '',
                    placeholder='Auswählen' 
                )
            ]
        ),

        html.Div(
            className = "variable_selection",
            children=[

                html.P('Erklärende Variable'),

                dcc.Dropdown(
                    id = 'predictors',
                    options=[],
                    value = '',
                    placeholder='Auswählen'            
                )
            ]
        ),
        
        html.Div(
            className = "variable_selection",
            children=[

                html.P('Kontrollvariablen'),
                
                dcc.Checklist(
                    id = 'controls',
                    options=[],
                    value=[''],
                    labelStyle= {'display': 'block'}               
                )
            ]
        ),

        html.Div(
            className = "variable_selection",
            children=[

                html.P(
                    'Codierung für Kategorien',
                    id = "encoding_title"
                ),
                
                dcc.Dropdown(
                    id = 'encoding',
                    options=['Dummy Codierung', 'One-Hot Codierung'],
                    value='Dummy Codierung',             
                ),
                dbc.Tooltip(
                    "Dummy: ... One-Hot: ...",
                    target= 'encoding', #"encoding", # "Codierung für Kategorien"
                    placement="bottom"
                )
            ]
        )

    ]
)


# callback for target variable selection
@dash_app.callback(
    Output('target', 'options'),
    Input('table', 'columns'),
    Input('predictors', 'value'),
    Input('controls', 'value'),
    Input('table', 'data'))
def update_target(columns, predictor_var, control_vars, data):

    df = pd.DataFrame(data)

    categorical = df.columns[(df.dtypes.values == np.dtype('object'))]
    control_vars = ",".join(string for string in control_vars if len(string) > 0)
    column_names = [i['name'] for i in columns if i['name'] not in [control_vars, predictor_var]]

    # only numeric targets for (linear) regression
    column_names = [i for i in column_names if i not in categorical]

    # if user clear data in table
    if df.isna().all().all() and list(df.columns) == ['Variable 1', 'Variable 2', 'Variable 3', 'Variable 4', 'Variable 5']:
        column_names = df.columns

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


# reset selection when data is uploaded
@dash_app.callback(
    Output('target', 'value'),
    Output('predictors', 'value'),
    Input('upload-data', 'contents'),
    prevent_initial_call=True
)
def clear_selection(upload):
    if callback_context.triggered_id == 'upload-data':
        return '', ''