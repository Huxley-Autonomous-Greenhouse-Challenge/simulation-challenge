from email_utils import send_mail, read_mail
import time

def main():
  print("Test Driver")
  request_counter = 16
  attempts = 0
  send_mail(counter=request_counter)
  wait = True
  print("Waiting 30 seconds before initial email check")
  time.sleep(30)
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
          print("Didn't find the expected email, waiting 15 seconds before re-trying")
          time.sleep(15)
          continue
      wait = False

main()
