import sys
import win32gui, win32con
import pyautogui
from interface import window, keyboard
import time, os

from verification.reference import VERIFICATION


def click_button(handle, buttontype):
    win32gui.ShowWindow(handle, 5)
    win32gui.SetForegroundWindow(handle)
    cancel_button_location = pyautogui.locateOnScreen(VERIFICATION['login'][f'image_{buttontype}_button'])
    if cancel_button_location:
        buttonx, buttony = pyautogui.center(cancel_button_location)
        pyautogui.click(buttonx, buttony)
        pyautogui.move(-200, -200)
        return True


def callback(hwnd, strings):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if window_title and right - left and bottom - top:
            handle = hwnd
            strings.append({'handle': handle, 'window_title': window_title})
    return True


def close_f2_login():
    check = VERIFICATION['login']

    win_list = []  # list of strings containing win handles and window titles
    win32gui.EnumWindows(callback, win_list)  # populate list
    open_windows = 0
    for window_info in win_list:  # print results
        screentype = None
        if window_info['window_title'] in check['list_str_screen_titles_ok']:
            screentype = 'ok'
        elif window_info['window_title'] in check['list_str_screen_titles_cancel']:
            screentype = 'cancel'

        elif window_info['window_title'] in check['list_str_screen_titles_annulern']:
            screentype = 'annulern'
        if screentype:
            open_windows += 1
            print(screentype)
            if not click_button(window_info['handle'], screentype):
                '''try:
                    win32gui.PostMessage(window_info['handle'], win32con.WM_CLOSE, 0, 0)
                except:
                    pass'''
    return open_windows


def close_f2_wondows():
    key_phrase = VERIFICATION['f2_window']['any']
    open_windows = window.get_matching_handles(key_phrase)
    for w in open_windows:
        close_window(w)


def close_window(open_window):
    handle = open_window['handle']
    for i in range(8):
        try:
            window.maximize_window(handle)
            win32gui.SetForegroundWindow(handle)
            time.sleep(1)
            keyboard.f12(7)
            keyboard.enter()
        except:
            return True

    win32gui.PostMessage(open_window['handle'], win32con.WM_CLOSE, 0, 0)

def restart_pc():
    close()
    os.system("shutdown /r /t 1")

def close():
    for i in range(4):
        close_f2_wondows()
        close_f2_login()
        time.sleep(.1)
