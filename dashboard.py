from dash import dcc, html
from components.table import table
from components.variable_selection import variable_selection
from components.plot import plot
from components.dropdowns import dropdowns
from components.model_store import model_store
from components.results import results
from components.validation import validation, validation_col_names
from components.upload import upload, validation_upload
from components.formatting import formatting
from dash_app import dash_app

def serve_layout():
    
    '''Define the layout of the application'''

    return html.Div(
        [
        # a header for the webpage
        html.H1('My Dash App'),

        # the dashboard application
        html.Div(
            className="dashboard",
            children = [

                # left column
                variable_selection, 

                validation, validation_col_names,
                validation_upload,

                # middle column
                html.Div(
                    className="middle-column",
                    children = [
                    
                        formatting,
                        upload,
                        
                        table,

                        html.Div(
                            className="dashboard-plot",
                            children = [
                                dropdowns,
                                plot
                            ]
                        )
                    ]
                ),

                # right column
                results

            ]
        ),

        model_store, 
        dcc.Store(id='dict_traces'),
        dcc.Store(id='list_used_colors'),
        dcc.Store(id='counter'),
        dcc.Store(id='table_store')
        ]
    )


if __name__ == '__main__':  


    dash_app.layout = serve_layout()
    dash_app.run_server(debug=True)
