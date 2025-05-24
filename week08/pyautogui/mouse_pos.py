#! python3
# mouse_pos.py - Displays the mouse cursor's current position.
import pyautogui
print('Press Ctrl-C to quit.')

try:
    # this is basically an infinite loop
    while True:
        # get mouse position
        x, y = pyautogui.position()
        # format the string to display the mouse position
        positionStr = f"x: {str(x).rjust(4)}, y: {str(y).rjust(4)}"
        # print the string
        print(positionStr, end="")
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\nDone.')
