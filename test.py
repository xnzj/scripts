import pygetwindow as gw
import pyautogui
import time

def is_screen_on():
    active_window = gw.getActiveWindow()

    if active_window is not None:
        # Check if the active window is visible
        return active_window.isMaximized or active_window.isActive

    return False

while True:
    if is_screen_on():
        print("Screen is on")
    else:
        print("Screen is off")

    time.sleep(1)
