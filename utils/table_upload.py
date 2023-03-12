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
                warning_upload = "Es werden nur die ersten 100 Zeilen hochgeladen"
            else:
                warning_upload = None
            df = df.head(100)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file - limit to 100 rows + header
            df = pd.read_excel(io.BytesIO(decoded))

            if len(df.index) > 100:
                warning_upload = "Es werden nur die ersten 100 Zeilen hochgeladen"
            else:
                warning_upload = None
            df = df.head(100)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return [
        dash_table.DataTable(
            data = df.to_dict('records'),
            columns = [{'name': i, 'id': i} for i in df.columns]
            ),
        warning_upload
    ]