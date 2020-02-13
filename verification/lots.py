from interface import keyboard, window
import time


def verify_lot(lot_number):
    keyboard.command(('shift','f10'))
    text = f'Intern partijnummer  : {lot_number}'
    for i in range(20):
        if text in window.get_window():
            keyboard.f12()
            return True
        else:
            time.sleep(.05)
    keyboard.f12()
    return False

def pricing_screen():
    text = 'Alle Tariefgroepen'
    for i in range(20):
        if text in window.get_window():
            return True
        else:
            time.sleep(.05)
    return False