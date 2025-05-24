import math
import time


import pyautogui as pg


time.sleep(2) # Time to move the mouse in seconds
pg.click()  # automated click wherever the cursor is

distance = 30
counter = 0

while distance > 0:
    x = math.cos(counter) * distance
    y = math.sin(counter) * distance

    # drag the mouse with the left button using the specified coordinates
    pg.dragRel(x, y, duration=0.2, button='left')

    counter += 1/5
    distance -= 1
    
