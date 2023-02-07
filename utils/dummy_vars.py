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