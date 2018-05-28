import sys
import openpyxl as xl
import pandas as pd

def load_xlsx():
    wb = xl.load_workbook(filename = 'SetpointInterfaceBatchFill.xlsx')
    wb.save(filename = "saved.xlsx")
    for sheet in wb:
        print(sheet.title)
        if (sheet.title == 'MyValues'):
            df = pd.DataFrame(sheet.values)
            print(df)

load_xlsx()
