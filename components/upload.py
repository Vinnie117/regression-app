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


upload = dcc.Upload(
            id='upload-data',
            className="upload",
            children=html.Div([
                'Drag and Drop oder ',
                html.A('Datei auswählen')
            ]),
            multiple=False,
            contents= None,
            filename=''
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

        table_store = {contents: children[0][0]}

        # Check for warning message of parse_contents()
        if children[0][1]:  # a dict containing warning messages
            warning_displayed = True

            warning_msg = ""

            # loop over all warnings
            for key, value in children[0][1].items():
                warning_msg += value

        else:
            warning_displayed = False
            warning_msg = None

    return table_store, warning_displayed, warning_msg
