import pynput

from pynput.keyboard import Key


def on_press(key):
    if (key.char != None):
        print("{0} was pressed.".format(key.char))

def on_release(key):

    if key == Key.esc:
        return False
