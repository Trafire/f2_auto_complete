from interface import keyboard, window
from verification import lots as lot_verify
import time

def go_to_lot(lot_number):
    window.get_window()
    keyboard.command('f7')
    keyboard.write_text(lot_number)
    keyboard.enter(n=2)
    return lot_verify.verify_lot(lot_number)


def go_to_pricing():
    screen = window.get_window()
    if not screen:
        time.sleep(.1)
        screen = window.get_window()
    if 'Pricegroup:' in screen:
        keyboard.command('f1')
        keyboard.write_text('0')
        keyboard.enter()

    keyboard.command('f2')
    keyboard.shift_f11()
    keyboard.home(3)
    return lot_verify.pricing_screen()



def go_to_price_lot(lot_number):
    return go_to_lot(lot_number) and go_to_pricing()



def close_pricing():
    for i in range(10):
        screen = window.get_window()
        if not 'Val╦═Perc.' in screen:
            return True
        time.sleep(.02)
    keyboard.f12()
    close_pricing()