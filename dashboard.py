from dash import dcc, html
from components.table import table
from components.variable_selection import variable_selection
from components.plot import plot
from components.dropdowns import dropdowns
from components.results import results
from dash_app import dash_app

def serve_layout():
    
    '''Define the layout of the application'''

    return html.Div(
        [
            # a header for the webpage
            html.H1('My Dash App'),

            # the dashboard application
            html.Div(children = [

                # left column
                variable_selection, 

                # middle column
                html.Div(children = [
                    table,

                    html.Div(children = [
                        dropdowns,
                        plot
                    ], style={'margin-top': '50px'}
                    )
                    
                ], style={
                    'width': '55%', 
                    'border': '1px dashed black'
                }),

                # right column
                results

            ], style={'display': 'flex', 'align-items': 'top'}
            ),

            dcc.Store(id='regression_results'),
            dcc.Store(id='dict_traces'),
            dcc.Store(id='list_used_colors')

        ]
    )


if __name__ == '__main__':  
    dash_app.layout = serve_layout()
    dash_app.run_server(debug=True)