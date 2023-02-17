import pandas as pd
import statsmodels.api as sm

def dummy_vars(df, cat_cols, num_cols, dummy_marker):
    # extract all dummy columns that are part of predictor variables
    dummies = []
    for cat in cat_cols:
        dummy = cat + dummy_marker
        for column in df.columns:
            if dummy in column:
                dummies.append(column)            
    x_vars = num_cols + dummies

    return x_vars

# check if df cell contain a (string representation of a) number and convert it if true
def numeric_converter(s):
    try:
        number = float(s)
        return number
    except ValueError:
        return s

def cat_inference(x_range, control_vars, drop_first):
    cat_df = pd.DataFrame({'cat': x_range})
    cat_dummies = pd.get_dummies(cat_df['cat'], prefix='cat', drop_first=drop_first)  # only the dummy case
    predictor_space_with_const = sm.add_constant(cat_dummies)

    # Partial regression: set all controls to 0
    for control in control_vars:
        predictor_space_with_const[control] = 0

    return predictor_space_with_const