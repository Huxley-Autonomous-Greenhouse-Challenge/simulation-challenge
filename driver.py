from email_utils import send_mail, read_mail
import optimize as op
import time
import argparse
import os
import shutil
import scipy.optimize as optimize
import pandas as pd

def main():
  print("Test Driver")
  parser = argparse.ArgumentParser()
  parser.add_argument("--single", action="store_true", help="Execute a single run and exit")
  parser.add_argument("--counter", type=int, help="The starting value of the counter", default=1)
  parser.add_argument("--read_retries", type=int, help="The number of email retries to attempt", default=10)
  parser.add_argument("--initial_wait", type=int, help="How long to wait after send (seconds)", default=30)
  parser.add_argument("--retry_wait", type=int, help="How long to wait for email reading retries (seconds)", default=15)
  parser.add_argument("--template", help="Initial template file, used if there are no results for \"counter - 1\" in the output directory", default="SetpointInterfaceBatchFill_template.xlsx")
  parser.add_argument("--output_dir", help="Absolute path to where to store simulation run results, default to one directory up from cwd")
  args = parser.parse_args()

  print(args.single)
  print(args.counter)
  print(args.read_retries)
  print(args.initial_wait)
  print(args.retry_wait)
  print(args.template)

  #latest_result_path(args)
  request_counter = args.counter
  '''if args.single:
      execute_run(args, request_counter)
  else:
      while True:
          execute_run(args, request_counter)
          request_counter = request_counter + 1'''
  execute_run2(args, request_counter)

counter = 0
def execute_run2(args, request_counter):
    global counter
    while True:
        initial_params, initial_df = op.get_params()
        print('Starting run {1} with initial initial params: {0}'.format(initial_params, request_counter))
        result = optimize.minimize(loop, initial_params, initial_df)
        # Capture the last set of results as a "check
        # MyValuesB3O85.txt

        print(result.x)
        if result.success:
            fitted_params = result.x
            print(fitted_params)
        else:
            raise ValueError(result.message)

def loop(params, df):
    global counter
    counter = counter + 1
    op.set_params(df)
    # take params, write them to spreadsheet
    print("Counter: {0}".format(counter))
    send_mail(counter=counter, files=['MyValuesB3O85.txt'])
    time.sleep(15)
    retries = 0
    while retries < 10:
        try:
            print("Checking for response email")
            directory = read_mail(counter=counter)
        except IndexError:
            print("Email has not yet arrived, retrying {0} of 10".format(retries))
            time.sleep(15)
            retries = retries + 1
            continue
        break;

    print("Run directory: {0}".format(directory))
    shutil.copyfile('MyValuesB3O85.txt', directory + '\\MyValuesB3O85.txt')
    #frame = load_xls(directory)

    #profit_filePath = os.path.join(os.getcwd(), 'profit.csv')
    profit_filePath = os.path.join(directory, 'profit.csv')
    profit_dataframe = pd.read_csv(profit_filePath, header=None)

    return -profit_dataframe[0][0]

def latest_result_path(args):
    if args.output_dir:
        directory = args.output_dir
    else:
        directory = os.getcwd().rsplit('\\', 1)[0] + "\\results"

    print("Searching path: {0}".format(directory))
    latest_result = [f.path for f in os.scandir(directory) if f.is_dir()][-1]

    print("Using: {0}".format(latest_result))
    return latest_result

def execute_run(args, request_counter):
    attempts = 0
    files = []
    files.append(latest_result_path(args) + "\\SetpointInterfaceBatchFill.xlsx")
    print("Files list: {0}".format(files))
    send_mail(counter=request_counter, files=files)
    wait = True
    print("Waiting {0} seconds before initial email check".format(args.initial_wait))
    time.sleep(args.initial_wait)
    while wait:
        try:
            attempts = attempts + 1
            print ("Read attempt {0}".format(attempts))
            read_mail(request_counter)
        except Exception as e:
            if attempts >= 10:
                print("Error, hasn't arrived, giving up")
                break;
            print("Catch exception: {0}".format(type(e)))
            print("Didn't find the expected email, waiting {0} seconds before re-trying".format(args.retry_wait))
            time.sleep(args.retry_wait)
            continue
        wait = False

main()
