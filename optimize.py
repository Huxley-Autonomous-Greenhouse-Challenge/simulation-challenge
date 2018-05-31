import scipy.optimize as optimize
import os
import math
import numpy as np
from email_utils import send_mail, read_mail
from time import sleep
from xlsx_utils import load_xlsx, get_variables, set_variables, print_sheet
from score import score
import pandas as pd

MyValues_filePath =  os.path.join(os.getcwd(), 'MyValuesB3O85.txt')
myValues_dataframe = pd.read_csv(MyValues_filePath, header=None)

print(myValues_dataframe)
counter = 1

def f(params):
    # take params, write them to spreadsheet
    print(params)
    send_mail(files=['MyValuesB3O85.txt'])
    sleep(45)
    read_mail(counter=counter)

    profit_filePath = os.path.join(os.getcwd(), 'profit.csv')
    profit_dataframe = pd.read_csv(profit_filePath, header=None)

    return -profit_dataframe[0][0]

initial_guess = [1, 1, 1]
result = optimize.minimize(f, initial_guess)
print(result.x)
if result.success:
    fitted_params = result.x
    print(fitted_params)
else:
    raise ValueError(result.message)
