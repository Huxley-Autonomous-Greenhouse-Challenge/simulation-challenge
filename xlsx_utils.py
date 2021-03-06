import sys
import openpyxl as xl
import xlrd
import pandas as pd
import csv

def load_xlsx(filename = 'SetpointInterfaceBatchFill_template.xlsx'):
    wb = xl.load_workbook(filename)
    for sheet in wb:
        if (sheet.title == 'MyValues'):
            return(sheet, wb)

def load_xls(path = None, filename = 'SetpointInterfaceBatchFill.xls'):
    frame = []
    wb = xlrd.open_workbook(filename)
    sheet_names = wb.sheet_names()
    print('Sheet Names', sheet_names)
    xl_sheet = wb.sheet_by_name(sheet_names[3])
    #get cell 2, 1
    num_cols = xl_sheet.ncols

    num_cols = xl_sheet.ncols   # Number of columns
    for row_idx in range(2, xl_sheet.nrows - 2):    # Iterate through rows
        frame_row = []
        print ('-'*40)
        print ('Row: %s' % row_idx)   # Print row number
        for col_idx in range(1, 15):  # Iterate through columns
            cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            frame_row.append(cell_obj.value)
            #print ('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj))
        #print(frame_row)
        frame.append(frame_row)

    #print(frame)
    return frame


def load_csv(filename = 'MyValuesB3O85.txt'):
    with open('file.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)

# Note: this is all the variables. TOO MANY TO OPTIMIZE
# We should remove some of the variables so there is a reasonable amount to do linear regression on.
def get_variables():
    sheet, wb = load_xlsx()
    variables = []

    for cellObj in sheet['B3':'O22']:
        for cell in cellObj:
            variables.append(cell.value)

    for cellObj in sheet['B23':'O42']:
        for cell in cellObj:
            variables.append(cell.value)

    for cellObj in sheet['B43':'F49']:
        for cell in cellObj:
            variables.append(cell.value)

    variables.append(sheet['B50'].value)
    variables.append(sheet['B51'].value)

    for cellObj in sheet['B52':'C54']:
        for cell in cellObj:
            variables.append(cell.value)

    variables.append(sheet['B55'].value)

    for cellObj in sheet['B57':'C60']:
        for cell in cellObj:
            variables.append(cell.value)

    variables.append(sheet['B61'].value)

    for cellObj in sheet['B62':'F66']:
        for cell in cellObj:
            variables.append(cell.value)

    variables.append(sheet['B67'].value)

    for cellObj in sheet['B68':'H71']:
        for cell in cellObj:
            variables.append(cell.value)

    variables.append(sheet['B72'].value)

    for cellObj in sheet['B73':'C75']:
        for cell in cellObj:
            variables.append(cell.value)

    variables.append(sheet['B76'].value)

    for cellObj in sheet['B77':'C79']:
        for cell in cellObj:
            variables.append(cell.value)

    variables.append(sheet['B80'].value)

    for cellObj in sheet['B81':'C83']:
        for cell in cellObj:
            variables.append(cell.value)

    return(variables)

def set_variables(variables):
    i = 0
    sheet, wb = load_xlsx()
    variables.reverse()

    for cellObj in sheet['B3':'O22']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    for cellObj in sheet['B23':'O42']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    for cellObj in sheet['B43':'F49']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    sheet['B50'].value = variables.pop()
    variables.append(sheet['B50'].value)
    sheet['B51'].value = variables.pop()
    variables.append(sheet['B51'].value)

    for cellObj in sheet['B52':'C54']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    sheet['B55'].value = variables.pop()
    variables.append(sheet['B55'].value)

    for cellObj in sheet['B57':'C60']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    sheet['B61'].value = variables.pop()
    variables.append(sheet['B61'].value)

    for cellObj in sheet['B62':'F66']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    sheet['B67'].value = variables.pop()
    variables.append(sheet['B67'].value)

    for cellObj in sheet['B68':'H71']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    sheet['B72'].value = variables.pop()
    variables.append(sheet['B72'].value)

    for cellObj in sheet['B73':'C75']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    sheet['B76'].value = variables.pop()
    variables.append(sheet['B76'].value)

    for cellObj in sheet['B77':'C79']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    sheet['B80'].value = variables.pop()
    variables.append(sheet['B80'].value)

    for cellObj in sheet['B81':'C83']:
        for cell in cellObj:
            cell.value = variables.pop()
            variables.append(cell.value)

    return(variables, sheet)

def print_sheet():
    ### Below is some code to print out the values of the spreadsheet with some notes.
    sheet, wb = load_xlsx()

    # Todo: Run simulation on August 1st plant date, then manually set setpoints for climate changes
    # Lower temperatures at night will save on energy.
    print('Heating setpoints')
    for cellObj in sheet['B3':'O22']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    print('Ventilation setpoints')
    for cellObj in sheet['B23':'O42']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    # These increase temperature on when conditions are sunny
    # Format: date, radiation_min, radiation_max, heating, venting
    print('Setpoint increments on radiation')
    for cellObj in sheet['B43':'F49']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    print('Planting date')
    print(sheet['B50'].value)

    # 1.5 appears to be pretty standard
    print('Plant denisity')
    print(sheet['B51'].value)

    # Format date, density
    print('Stem density')
    for cellObj in sheet['B52':'C54']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    # Normally 2-3 weeks before final harvest.
    print('Date to remove head')
    print(sheet['B55'].value)

    print('Fruits Maintaned')
    for cellObj in sheet['B57':'C60']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    print('Illumination Intensity')
    print(sheet['B61'].value)

    # Format: date, time_lights_on, time_lights_off, radiation_50percent_shutoff, radiation_complete_shutoff
    print('Lamp control')
    for cellObj in sheet['B62':'F66']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    print('CO2 capacity')
    print(sheet['B67'].value)

    print('CO2 control')
    for cellObj in sheet['B68':'H71']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    print('MaxOutside Screen1')
    print(sheet['B72'].value)

    print('Screen control 1')
    for cellObj in sheet['B73':'C75']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    print('MaxOutside Screen2')
    print(sheet['B76'].value)

    print('Screen control 1')
    for cellObj in sheet['B77':'C79']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)

    print('Screen 2 for shading')
    print(sheet['B80'].value)

    print('Shade control')
    for cellObj in sheet['B81':'C83']:
        for cell in cellObj:
                print(cell.coordinate, cell.value)
