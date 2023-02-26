from dash import dcc, html
from dash.dependencies import Input, Output
from dash_app import dash_app
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from utils.data_prep import numeric_converter

variable_selection = html.Div([

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
    ], style={
        'border': '1px dashed black',
        'margin-top': '30px',
    }),

    html.Div([

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
    ], style={
        'border': '1px dashed black',
        'margin-top': '30px',
    })

], style={
    'display': 'inline-block',  # display elements (children) side by side
    'width': '10%',  # percentage of screen width taken by div
    'border': '1px dashed black',  # border (for debugging)          
    }
)


# callback for target variable selection
@dash_app.callback(
    Output('target', 'options'),
    Input('table', 'columns'),
    Input('predictors', 'value'),
    Input('controls', 'value'),
    # Input(component_id = 'table', component_property = 'data'),
    Input(component_id = 'table_store', component_property = 'data'),
    Input(component_id='decimal_separator', component_property = 'value')
    )
def update_target(columns, predictor_var, control_vars, data, decimal_separator):

    df = pd.DataFrame(data)

    categorical = df.columns[(df.dtypes.values == np.dtype('object'))]
    control_vars = ",".join(string for string in control_vars if len(string) > 0)
    column_names = [i['name'] for i in columns if i['name'] not in [control_vars, predictor_var]]

    # only numeric targets for (linear) regression
    column_names = [i for i in column_names if i not in categorical]

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