import imaplib
import smtplib
import sys
import json
import os
import os.path as op
import email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

with open('email_credentials.json', 'r') as f:
    credentials = json.load(f)

sender = credentials['email']
passwd = credentials['password']

# TODO: include Setpoint excel file to send
#TO = 'GreenhouseSimulation@gmail.com'
TO = 'frank.marcus@grnlight.ca'
SUBJECT = 'FastSimReq'
TEXT = 'Here is a message from python.'


def read_mail(counter=1,
              send_from=sender,
              send_to=TO,
              subject=SUBJECT,
              message=TEXT,
              files=[],
              server='smtp.gmail.com',
              port=587,
              username=sender,
              password=passwd,
              use_tls=True ):
    imapSession = imaplib.IMAP4_SSL(server)
    typ, accountDetails = imapSession.login(username, password)
    if typ != 'OK':
        print ('Not able to sign in!')
        raise

    imapSession.select('inbox')
    subject_str = '(SUBJECT "RE: FastSimReq' + str(counter) + '")'
    print("Searching for subject {0}".format(subject_str))
    typ, data = imapSession.search(None, subject_str)
    if typ != 'OK':
        print ('Error searching Inbox.')
        raise

    print("len: {1} data: {0}".format(data, len(data)))
    # Get the latest message.
    typ, messageParts = imapSession.fetch(data[0].split()[-1], '(RFC822)')
    if typ != 'OK':
        print ('Error fetching mail.')
        raise

    emailBody = messageParts[0][1]
    mail = email.message_from_bytes(emailBody)
    #Create a folder to store the results of the run
    directory = os.getcwd().rsplit('\\', 1)[0] + "\\results\\run_" + str(counter)
    print("directory: {0}".format(directory))
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Created directory {0}".format(directory))
    else:
        print("Directory {0} already exists".format(directory))

    print("Subject: {0}".format(mail['Subject']))
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(directory, fileName)
            if not os.path.isfile(filePath) :
                print (fileName)
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
    imapSession.close()
    imapSession.logout()

def send_mail(counter=1,
              send_from=sender,
              send_to=TO,
              subject=SUBJECT,
              message=TEXT,
              files=['SetpointInterfaceBatchFill.xlsx'],
              server='smtp.gmail.com',
              port=587,
              username=sender,
              password=passwd,
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (str): to name
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    print("User: {0} Passwd: {1}".format(username, password))
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject + str(counter)
    print("Sending with to {1} with subject {0}".format(msg['Subject'], msg['To']))

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)

    print("Sending email")
    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
