import random
import time

import pyautogui as pg


from randomuser import RandomUser


def get_chars():
    chars = []
    # Numbers
    for i in range(48, 58):
        chars.append(chr(i))
    # Lowercase chars
    for i in range(65, 91):
        chars.append(chr(i))
    # Uppercase chars
    for i in range(97, 123):
        chars.append(chr(i))
    return chars


def generate_password(len):
    chars = get_chars()
    password = []
    for _ in range(len):
        password.append(random.choice(chars))
    return ''.join(password)


type_in_loc = {
    "first_name": (237, 256),
    "last_name": (250, 279),
    "city": (259, 308),
    "password_a": (212, 335),
    "password_b": (272, 356),
}


click_on_loc = {
    "remember_me": (232, 383),
    "login_btn": (48, 689),
}



for j in range(3):
    user = RandomUser()
    # password = generate_password(12)

    type_in_val = {
        "first_name": user.get_first_name(),
        "last_name": user.get_last_name(),
        "city": user.get_city(),
        "password_a": user.get_password(),
        "password_b": user.get_password(),
    }

    click_on_val = {
        "remember_me": random.random() < 0.5,
        "login_btn": True,
    }

    time.sleep(4)
    # Fill out the form
    for item, loc in type_in_loc.items():
        pg.click(loc)
        pg.typewrite(type_in_val[item])
        time.sleep(2)

    # Click on the things
    for item, loc in click_on_loc.items():
        if(click_on_val[item]):
            pg.click(loc)
            time.sleep(2)

    time.sleep(2)
    print(f"Done for user {user.get_first_name()}!")

print("Completely done!")


