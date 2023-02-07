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