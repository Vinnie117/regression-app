from dash import Dash, dash_table
import pandas as pd
from collections import OrderedDict

data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
        ("Temperature2", [1, -20, 3.512, 4, 10423, -441.2])
    ]
)

df = pd.DataFrame(data)

size = '{}%'.format(len(df.columns))
print(size)

app = Dash(__name__)

app.layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],

    css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
    style_cell={
        'width': '{}%'.format(len(df.columns)),
        'textOverflow': 'ellipsis',
        'overflow': 'hidden'
    }
    
    #style_cell={'textAlign':'right','minWidth': 300, 'maxWidth': 300, 'width': 300,'font_size': '12px','whiteSpace':'normal','height':'auto'}
)

if __name__ == '__main__':


    app.run_server(debug=True)