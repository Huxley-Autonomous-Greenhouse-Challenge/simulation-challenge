import pandas as pd
#import tensorflow as tf
import os
import math
import numpy as np
from email_utils import send_mail, read_mail
from time import sleep
from xlsx_utils import load_xlsx, get_variables, set_variables, print_sheet

def score():
    # turn this into a scoring function
    cropOutput_filePath = os.path.join(os.getcwd(), 'cropModelOutput.csv')
    climate_filePath = os.path.join(os.getcwd(), 'climateModelOutput.csv')
    profit_filePath = os.path.join(os.getcwd(), 'profit.csv');

    crop_dataframe = pd.read_csv(cropOutput_filePath, header=None)
    climate_dataframe = pd.read_csv(climate_filePath, header=None)
    profit_dataframe = pd.read_csv(profit_filePath, header=None)

    crop_cols = [
        'DAYNR',
        'Number of fruits per plant',
        'Fresh weight of harvested fruit',
        'Number of harvested fruits',
        'Age of harvested fruit'
    ]

    climate_cols = [
        'GlobRad',
        'Tout',
        'RHout',
        'Wind speed',
        'Tair',
        'RHair',
        'PAR light',
        'CO2air',
        'Heating setpoint',
        'Ventilation setpoint',
        'Pipe temperature',
        'Heating power',
        'CO2 dosing',
        'Screen 1 position',
        'Screen 2 position',
        'Power lamps',
        'Window opening'
    ]

    # Todo: we loose the first line of data when we do this since the simulation results don't give
    # us proper CSV
    climate_dataframe.columns = climate_cols
    crop_dataframe.columns = crop_cols

    # Maximize these
    fruits = crop_dataframe['Number of harvested fruits'].sum()
    weight_of_fruits = crop_dataframe['Fresh weight of harvested fruit'].sum()
    fruits_per_plant = crop_dataframe['Number of fruits per plant'].sum()

    # Minimize these
    heat_power = climate_dataframe['Heating power'].sum()
    lamp_power = climate_dataframe['Power lamps'].sum()

    print('fruits ' + str(fruits))
    print('weight ' + str(weight_of_fruits))
    print('fruits per plant ' + str(fruits_per_plant))

    print('heat power used ' + str(heat_power))
    print('light power used ' + str(lamp_power))

    return([fruits, weight_of_fruits, fruits_per_plant, heat_power, lamp_power])
