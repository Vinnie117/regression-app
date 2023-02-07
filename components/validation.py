from dash import dcc
from dash.dependencies import Input, Output, State
from dash_app import dash_app
import pandas as pd


validation =dcc.ConfirmDialog(
                id='warning_msg',
                message='',
                )

@dash_app.callback(
    Output('warning_msg', 'displayed'),
    Output('warning_msg', 'message'),
    Output('warning_msg', 'cancel_n_clicks'),
    State(component_id = 'table', component_property = 'data'),               
    Input('submit-button-state', 'n_clicks'),
    prevent_initial_call=True)
def validate(data, n_clicks):

    data = pd.DataFrame(data)

    warning = "Warnung! \n"
    warn_1 = None
    warn_2 = None

    # check NaNs: true if any NaN in df -> will send confirm dialog
    if data.isnull().values.any():  
        warn_1 = '- Datenfelder enthalten leere Werte, die beim Fortfahren verworfen werden \n'
    
    # type checking for each column 
    # (insight: though column might be of type 'object', the cells can be of mixed primitive types)
    for i in data.columns:
        types = data[i].apply(type).value_counts()

        if len(types) == 1:
            print("Column: ", i, "unique data type: ", types)
            pass
        else:
            try:
                # user input could be numeric but is interpreted as string -> try to convert
                data[i] = data[i].astype(float)  # applymap(numeric_converter)
                return False, '', None
            except:
                print("Column: ", i, "mixed data type: ", types) 
                warn_2 = '- Gemischte Datentypen in den Feldern gefunden'

    if warn_1 is not None and warn_2 is not None:
        return True, warning + warn_1 + warn_2, None
    elif warn_1 is not None:
        return True, warning + warn_1, None
    elif warn_2 is not None:
        return True, warning + warn_2, None

    return False, '', None