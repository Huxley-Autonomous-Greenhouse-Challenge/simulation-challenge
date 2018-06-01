import scipy.optimize as optimize
import os
import math
import numpy as np
from email_utils import send_mail, read_mail
from time import sleep
from xlsx_utils import load_xlsx, get_variables, set_variables, print_sheet, load_xls
from score import score
import pandas as pd
import csv

counter = 1

def get_params(filename='MyValuesB3O85.txt'):
    MyValues_filePath =  os.path.join(os.getcwd(), 'MyValuesB3O85.txt')
    myValues_dataframe = pd.read_csv(MyValues_filePath, header=None)
    # Maybe just use csv to read the file.
    params = []
    for list in myValues_dataframe.values:
        for value in list:
            params.append(value)
    return(params, myValues_dataframe)

def get_xls_params(filename='SetpointInterfaceBatchFill.xls'):
    raw_list = load_xls(filename)
    myValues_dataframe = pd.DataFrame(raw_list)
    params = []
    for list in myValues_dataframe.values:
        for value in list:
            params.append(value)
    return(params, myValues_dataframe)

def set_params(df):
    filepath = os.path.join(os.getcwd(), 'MyValuesB3O85.txt')
    df.to_csv(path_or_buf=filepath, encoding='ascii', header=False, index=False)

#params, frame = get_xls_params()
#print(frame)
'''initial_params, df = get_params()

def loop(params, df):
    set_params(df)
    # take params, write them to spreadsheet
    send_mail(files=['MyValuesB3O85.txt'])
    sleep(45)
    read_mail(counter=counter)

    profit_filePath = os.path.join(os.getcwd(), 'profit.csv')
    profit_dataframe = pd.read_csv(profit_filePath, header=None)

    return -profit_dataframe[0][0]

initial_guess, params_dataframe = get_params()
result = optimize.minimize(loop, initial_guess, params_dataframe)
print(result.x)
if result.success:
    fitted_params = result.x
    print(fitted_params)
else:
    raise ValueError(result.message)'''
