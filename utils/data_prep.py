import pandas as pd
import numpy as np
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

# check if df cell contains a (string representation of a) number and convert it if true
# try to convert string representation of numerics to numeric
def numeric_converter(s):

    # comma as decimal separator
    try:

        if ',' in str(s):
            number = float(str(s).replace(',', '.'))
        else:
            number = float(s)
        return number

    # except ValueError:
    #     return s

    # except (ValueError, TypeError):
    #     return s

    except ValueError:
        return s
    except TypeError:
        pass



        



'''

# THE ORIGINAL FUNCTION
# # # try to convert string representation of numerics to numeric
def numeric_converter(s):
    try:
        number = float(s)
        return number
    except ValueError:
        return s


def numeric_converter(s):
    try:
        number = float(str(s).replace(',', '.'))
        return number
    except ValueError:
        return s


def numeric_converter(s, decimal_separator):

    try:
        s_str = str(s)
        if decimal_separator == ',':
            if '.' in s_str:
                return s_str == None
            else:
                number = float(s_str.replace(',', '.'))
        elif decimal_separator == '.':
            number = float(s_str)
        return number
    except ValueError:
        return str(s)

'''



def cat_inference(x_range, control_vars, drop_first):
    cat_df = pd.DataFrame({'cat': x_range})
    cat_dummies = pd.get_dummies(cat_df['cat'], prefix='cat', drop_first=drop_first)
    predictor_space_with_const = sm.add_constant(cat_dummies)

    # Partial regression: set all controls to 0
    for control in control_vars:
        predictor_space_with_const[control] = 0

    return predictor_space_with_const


def drop_minority_type(df, vars):
    for col in vars:
        types = df[col].apply(type).value_counts()
        
        if len(types) != 1:
            value_counts = df[col].apply(type).value_counts()
            minority_type = value_counts.index[-1]
            df = df[df[col].apply(type) != minority_type] 
            df = df.applymap(numeric_converter) 
            
        return df