from dash import dcc, html
from dash_app import dash_app
from dash.dependencies import Input, Output, State
import pandas as pd
import base64, io, sys
from utils.table_upload import parse_contents

validation_upload =dcc.ConfirmDialog(
                id='warning_upload_msg',
                message='',
                )

# @dash_app.callback(
#     Output('warning_upload_msg', 'displayed'),
#     Output('warning_upload_msg', 'message'),
#     Output('warning_upload_msg', 'cancel_n_clicks'),
#     State(component_id = 'table', component_property = 'data'),
#     State(component_id = 'target', component_property = 'value'),
#     State(component_id = 'predictors', component_property = 'value'),
#     State(component_id = 'controls', component_property = 'value'),               
#     Input('submit-button-state', 'n_clicks'),
#     prevent_initial_call=True)
# def validate(data, target_var, predictor_var, control_vars, n_clicks):
#     pass


upload = dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop oder ',
                html.A('Datei auswählen')
            ]),
            multiple=False,
            contents= None,
            filename='',
            style={
                'width': '77%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin-left': 'auto', 
                'margin-right': 'auto',
                }
                )


@dash_app.callback(
    Output('table_store', 'data'),
    Output('warning_upload_msg', 'displayed'),
    Output('warning_upload_msg', 'message'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
)
def store_external_data(contents, filename, date):

    if contents is not None:

        children = [parse_contents(c, n, d) for c, n, d in zip([contents], [filename], [date])]
        
        # this triggers if parse_contents() detects more than 100 rows
        if children[0][1]:
            warning_displayed = True
            warning_msg = children[0][1]
        else:
            warning_displayed = None
            warning_msg = None

        # retrieve 'data' property of data table
        # json_data = children[0].data
        print("The size of df in data_store is {} bytes".format(sys.getsizeof(children)))  # 232 Bytes

        # table_columns = children[0].columns # columns # [{'name': i, 'id': i} for i in df.columns]
        # print(table_columns)

        table_store = {contents: children[0][0]}

    return table_store, warning_displayed, warning_msg
