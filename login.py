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
    paths = [
        {'dir': r'c:/Program Files (x86)/Connect Internet/', 'filename':'Connect.exe'},
        {'dir': r'c:/Program Files (x86)/Connect2000_Internet/', 'filename':'Connect2000.exe'}
                   ]
    for path in paths:
        try:   
            os.chdir(path['dir'])
            os.system(path['filename'])
            break
        except:
            print("not found")
            print(path)
    while not is_login_dialogue_open():
        time.sleep(.1)
    keyboard.write_text(password)
    pyautogui.hotkey('shift', 'tab')
    keyboard.write_text(username)
    keyboard.enter()


def sign_in_toronto(username, password, system, attempts=0):
    print(f"starting login attempt: {attempts}")
    if attempts > 5:
        return False
    login(username, password)

    if not f2.is_system_open(100):
        print(f"system is not open attempt{attempts}")
        return sign_in_toronto(username, password, attempts + 1)
    else:
        print("system has opened")

    # sign into f2 Canada
    window_data_size_1 = VERIFICATION['screens']['text_login_menu_1']
    print('verifying window')
    print(window_data_size_1)
    if not f2.verify_contains(window_data_size_1, attempts=500):
        print("attempting to varify")
        return sign_in_toronto(username, password, attempts + 1)

    keyboard.write_text(VERIFICATION['system_options']['f2_canada_menu_number'])
    # sign into life system

    window_data_size_1 = VERIFICATION['screens']['text_login_menu_2']

    if not f2.verify_contains(window_data_size_1, attempts=500):
        print(f'sign in attempt {attempts}')
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
    print('signed in')
    return True


username = f2_password['username']
password = f2_password['password']
system = 'f2_canada_real'

if __name__ == '__main__':
    for i in range(5):
        closef2.close()
        sign_in_toronto(username, password,system)
        closef2.close()
