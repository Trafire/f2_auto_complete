import pyautogui
from autof2.interface import clipboard


def make_mixed_string(data, data_list=[]):
    if '{' in data and '}' in data[data.index('{'):]:
        if data[0] != '{':
            curly_index = data.index('{')

        else:
            curly_index = data.index('}') + 1

        data_list.append(data[:curly_index])
        data = data[curly_index:]
        if data:
            make_mixed_string(data, data_list)
        return data_list
    else:
        data_list.append(data)
        return data_list


def write_mix(data):
    data_list = make_mixed_string(data)
    for d in data_list:
        if '{' in d and '}' in d[d.index('{'):]:
            command(d)
        else:
            write_text(d)

def paste_write(data):
    clipboard.empty_clipboard()
    clipboard.set_clipbaord(data)
    command(('alt', 'v'))


def write_text(data, interval=.01):
    pyautogui.typewrite(data, interval)


def pgdn(n=1):
    for i in range(n):
        pyautogui.hotkey(('pgdn'))


def pgup(n=1):
    for i in range(n):
        pyautogui.hotkey(('pgup'))


def command(data):
    if type(data) == tuple:
        pyautogui.hotkey(*data)
    else:
        pyautogui.hotkey(data)


def f11(n=1):
    for i in range(n):
        pyautogui.hotkey(('f11'))


def shift_f11(n=1):
    for i in range(n):
        pyautogui.hotkey(
            'shift', 'f11'
        )


def f12(n=1):
    for i in range(n):
        pyautogui.hotkey(('f12'))


def enter(n=1):
    for i in range(n):
        pyautogui.hotkey(('enter'))


def home(n=1):
    for i in range(n):
        pyautogui.hotkey(('home'))



