from verification import f2
from verification.reference import VERIFICATION
from interface import keyboard
from interface import window
from parse import parse
import time


def price_item(price):
    points = VERIFICATION['pricing']['f8-pricing']
    if True or f2.verify(points, attempts=10):
        keyboard.shift_f11()
        keyboard.home()
        keyboard.enter()
        keyboard.paste_write(make_price_str(price))
        keyboard.f11()
        keyboard.f12(2)
    else:
        return False

def make_price_str(price):
    price = str(price) + '\n'
    return price * 13

def top_of_list():
    uscreen = window.get_window()
    keyboard.home(2)
    if f2.is_new_screen(uscreen):
        return top_of_list()
    return True

def count_items_in_category(count=0, oldcreen=''):
    points = VERIFICATION['pricing']['in_group-pricing']
    if f2.verify(points, attempts=10):
        if f2.is_new_screen(oldcreen):
            uscreen = window.get_window()
            count += parse.count_category(uscreen)
            keyboard.pgdn()
            time.sleep(.1)
            return count_items_in_category(count, uscreen)
        return count
    return None


