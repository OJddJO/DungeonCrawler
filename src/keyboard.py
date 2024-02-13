from pynput import keyboard

def is_pressed(key):
    return keyboard.Controller().is_pressed(key)

def press(key):
    keyboard.Controller().press(key)
    keyboard.Controller().release(key)

def wait(key):
    with keyboard.Listener(on_press=lambda k: None if k != key else False) as listener:
        listener.join()

def read_key():
    with keyboard.Listener(on_press=lambda k: k) as listener:
        return listener.join().key