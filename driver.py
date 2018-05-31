from email_utils import send_mail, read_mail
import time
import argparse
import os

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
  if args.single:
      execute_run(args, request_counter)
  else:
      while True:
          execute_run(args, request_counter)
          request_counter = request_counter + 1

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
