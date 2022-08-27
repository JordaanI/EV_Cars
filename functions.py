import pandas as pd
import numpy as np
import re

def model_formatter(series):
    if ' - ' in series['Model']:
        model = series['Model'].split(' - ')
        model = model[0] + ' – ' + model[1]
        return model.strip()
    models = ['i4', 'IONIQ 5', 'Model 3', '60 Recharge']
    for model in models:
        if model in series['Model']:
            return series['Model'].replace(model, model + ' – ').strip()
    return series['Model'].strip()

def model_splitter(series):
    if ' – ' in series['Model']:
        res = series['Model'].split(' – ')
        return res[1].strip()
    else:
        return ''

def model_correction(series):
    if ' – ' in series['Model']:
        res = series['Model'].split(' – ')
        return res[0].strip()
    else:
        return series['Model'].strip()

def separator(series,separator,column,suffix):
    df = pd.DataFrame()
    str = series[column]
    res = re.split(separator, str)
    for ind in res:
        car_make = series['Make']
        car_model = series['Model']
        car_category = series['Category']
        car_rebate = series['Rebate-' + suffix]
        car_eligibility = series['Eligibility']
        if column == 'Trim':
            car_model_year = series['Year-' + suffix]
            temp_dict={'Make':car_make,'Model':car_model, 'Trim':ind,'Rebate-' + suffix:car_rebate,'Year-' + suffix:car_model_year,'Category':car_category,'Eligibility':car_eligibility}
            df = df.append(temp_dict, ignore_index=True)
        else:
            car_trim = series['Trim']
            temp_dict={'Make':car_make,'Model':car_model,'Trim': car_trim,'Rebate-' + suffix:car_rebate,'Year-' + suffix:ind,'Category':car_category,'Eligibility':car_eligibility}
            df = df.append(temp_dict, ignore_index=True)
    return df

def splitter(df,separators, column, suffix):
    drop_list = []
    for ind in range(len(df)):
        series = df.iloc[ind]
        if any([separator in series[column] for separator in separators]):
            temp= separator(series, '|'.join(separators),column,suffix)
            df = df.append(temp, ignore_index=True)
            drop_list.append(ind)
    df = df.drop(drop_list)
    df = df.sort_values(by = ['Make'])
    df = df.reset_index(drop = True)
    return df