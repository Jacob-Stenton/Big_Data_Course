import pyautogui
import time

time.sleep(2)
pyautogui.click()
# click to put drawing program in focus
distance = 200
while distance > 0:
    pyautogui.dragRel(distance, 0, duration=0.2, button='left')
    # move right
    distance = distance - 5
    pyautogui.dragRel(0, distance, duration=0.2, button='left')
    # move down
    pyautogui.dragRel(-distance, 0, duration=0.2, button='left') # move left
    distance = distance - 5
    pyautogui.dragRel(0, -distance, duration=0.2, button='left') # move up
