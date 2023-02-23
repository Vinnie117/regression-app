from dash import dcc
from dash.dependencies import Input, Output, State
from dash_app import dash_app
import pandas as pd
from utils.data_prep import numeric_converter

validation =dcc.ConfirmDialog(
                id='warning_msg',
                message='',
                )

@dash_app.callback(
    Output('warning_msg', 'displayed'),
    Output('warning_msg', 'message'),
    Output('warning_msg', 'cancel_n_clicks'),
    State(component_id = 'table', component_property = 'data'),
    State(component_id = 'target', component_property = 'value'),
    State(component_id = 'predictors', component_property = 'value'),
    State(component_id = 'controls', component_property = 'value'),               
    Input('submit-button-state', 'n_clicks'),
    prevent_initial_call=True)
def validate(data, target_var, predictor_var, control_vars, n_clicks):

    # only check columns relevant for calculation
    control_vars = [item for item in control_vars if len(item)>0]
    x_vars = [predictor_var] + control_vars

    data = pd.DataFrame(data)
    data = data.applymap(numeric_converter)

    warning = "Warnung! \n"
    warn_1 = None
    warn_2 = None

    # check NaNs: true if any NaN in df -> will send confirm dialog
    if data[[target_var] + x_vars].isnull().values.any():  
        warn_1 = '- Datenfelder für die Berechnung enthalten fehlerhafte / leere Werte, die beim Fortfahren ignoriert werden \n'
    
    # type checking for each column 
    # (insight: though column might be of type 'object', the cells can be of mixed primitive types)
    for col in [target_var] + x_vars:
        types = data[col].apply(type).value_counts()

        if len(types) == 1 or (len(types) == 2 and "<class 'NoneType'>" in str(types)):
            print("Column: ", col, "unique data type: ", types)
            pass
        else:
            try:
                # user input could be numeric but is interpreted as string -> try to convert
                data[col] = data[col].astype(float)  # applymap(numeric_converter)
                # data[col] = data[col].apply(numeric_converter)
                return False, '', None
            except:
                print("Column: ", col, "mixed data type: ", types) 
                warn_2 = '- Einige Spalten für die Berechnung enthalten gemischte Datentypen. Diese Zeilen werden ignoriert.'


    if warn_1 is not None and warn_2 is not None:
        return True, warning + warn_1 + warn_2, None
    elif warn_1 is not None:
        return True, warning + warn_1, None
    elif warn_2 is not None:
        return True, warning + warn_2, None

    return False, '', None