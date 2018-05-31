import pandas as pd
import tensorflow as tf
import os
import math
import numpy as np
from email_utils import send_mail, read_mail
from time import sleep
from xlsx_utils import load_xlsx, get_variables, set_variables, print_sheet
from score import score

# Checks
v1 = get_variables()
v2 = set_variables(v1)

# Check to make sure we are getting and setting the same variables
if v1 != v2:
    print('Warning! get_variables() is returning different results than set variables().')

# pick the next set of variables
# send_mail()
# print('Request sent waiting for response')
# sleep(30)
read_mail()

initial = score()
print(initial)
