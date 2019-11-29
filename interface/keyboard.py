import pyautogui
from autof2.interface import clipboard


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

def f12(n=1):
    for i in range(n):
        pyautogui.hotkey(('f12'))


def enter(n=1):
    for i in range(n):
        pyautogui.hotkey(('enter'))


def home(n=1):
    for i in range(n):
        pyautogui.hotkey(('home'))
