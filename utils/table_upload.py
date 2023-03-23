import pandas as pd
import base64, io
from dash import html, dash_table

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file - limit to 100 rows + header
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            
            if len(df.index) > 100:
                warning_upload_rows = "- Es werden nur die ersten 100 Zeilen hochgeladen \n"
            else:
                warning_upload_rows = None
            df = df.head(100)

            if len(df.columns) > 5:
                warning_upload_cols = "- Es werden nur die ersten 5 Spalten hochgeladen"
            else:
                warning_upload_cols = None

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file - limit to 100 rows + header
            df = pd.read_excel(io.BytesIO(decoded))

            if len(df.index) > 100:
                warning_upload_rows = "- Es werden nur die ersten 100 Zeilen hochgeladen \n"
            else:
                warning_upload_rows = None
            df = df.head(100)

            if len(df.columns) > 5:
                warning_upload_cols = "- Es werden nur die ersten 5 Spalten hochgeladen"
            else:
                warning_upload_cols = None


    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    # dict with warning messages
    warnings = {}
    if warning_upload_rows:
        warnings['warning_rows'] = warning_upload_rows
    if warning_upload_cols:
        warnings['warning_cols'] = warning_upload_cols

    return [
        dash_table.DataTable(
            data = df.to_dict('records'),
            columns = [{'name': i, 'id': i} for i in df.columns]
            ),
        warnings
    ]