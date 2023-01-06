from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Input(
            id='adding-rows-name',
            placeholder='Enter a column name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Column', id='adding-rows-button', n_clicks=0)
    ], style={'height': 50}),

    dash_table.DataTable(
        id='adding-rows-table',
        columns=[{
            'name': 'Column {}'.format(i),
            'id': 'column-{}'.format(i),
            'deletable': True,
            'renamable': True
        } for i in range(1, 5)],    # Default Anzahl der Spalten
        data=[
            {'column-{}'.format(i): (j + (i-1)*9) for i in range(1, 9)}    # Startwerte der Tabelle
            for j in range(9)    # Default Anzahl der Reihen
        ],
        editable=True,
        fill_width=False,
        row_deletable=True
    ),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),

    dcc.Graph(id='adding-rows-graph'),
    dcc.Graph(id="scatter-plot"),
])



# behaviour for adding rows 
@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

# behaviour for adding columns
@app.callback(
    Output('adding-rows-table', 'columns'),
    Input('adding-rows-button', 'n_clicks'),
    State('adding-rows-name', 'value'),
    State('adding-rows-table', 'columns'))
def update_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns


# Interaction between data table and plot
@app.callback(
    Output('adding-rows-graph', 'figure'),
    Input('adding-rows-table', 'data'),
    Input('adding-rows-table', 'columns'))
def display_output(rows, columns):
    return {
        'data': [{
            'type': 'heatmap',
            'z': [[row.get(c['id'], None) for c in columns] for row in rows],
            'x': [c['name'] for c in columns]
        }]
    }


if __name__ == '__main__':



    app.run_server(debug=True)