import os, subprocess
import pyautogui
import time
from verification.login import is_login_dialogue_open
from verification import f2
from verification.reference import VERIFICATION

from interface import window, keyboard
import closef2
from auth.passwords import f2_password

def login(username, password):
    closef2.close()
    p = r'c:/Program Files (x86)/Connect Internet/'
    os.chdir(p)
    os.system('Connect.exe')
    while not is_login_dialogue_open():
        time.sleep(.1)
    keyboard.write_text(password)
    pyautogui.hotkey('shift', 'tab')
    keyboard.write_text(username)
    keyboard.enter()


def sign_in_toronto(username, password, system, attempts=0):
    tries = 0
    if attempts > 5:
        return False
    login(username, password)

    if not f2.is_system_open(100):
        return sign_in_toronto(username, password, attempts + 1)

    # sign into f2 Canada
    window_data_size_1 = VERIFICATION['screens']['text_login_menu_1']

    if not f2.verify_contains(window_data_size_1, attempts=500):
        return sign_in_toronto(username, password, attempts + 1)

    keyboard.write_text(VERIFICATION['system_options']['f2_canada_menu_number'])
    # sign into life system

    window_data_size_1 = VERIFICATION['screens']['text_login_menu_2']

    if not f2.verify_contains(window_data_size_1, attempts=500):
        return sign_in_toronto(username, password, attempts + 1)

    # choose syste,
    if system == 'f2_canada_real':
        keyboard.write_text(VERIFICATION['system_options']['f2_canada_real_system_number'])
        window_data = VERIFICATION['system']['f2_canada_real']
    elif system == 'f2_canada_test':
        keyboard.write_text(VERIFICATION['system_options']['f2_canada_test_system_number'])
        window_data = VERIFICATION['system']['f2_canada_test']
    else:
        return False
    if not f2.verify(window_data, attempts=500):
        return sign_in_toronto(username, password, attempts + 1)

    window_data = VERIFICATION['screens']['main_menu']
    if not f2.verify(window_data, attempts=500):
        return sign_in_toronto(username, password, attempts + 1)

    return True


username = f2_password['username']
password = f2_password['password']
system = 'f2_canada_real'
if __name__ == '__main__':
    sign_in_toronto(username, password,system)
