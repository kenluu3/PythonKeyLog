import pynput, time

from KeyboardListener import *
from pynput.keyboard import Key, Listener



# Create Keyboard Listener.
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
