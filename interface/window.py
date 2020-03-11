import win32gui, win32con
import re, time
from verification import reference
import win32gui
import win32con
from autof2.interface import mouse
from autof2.interface import clipboard
from autof2.interface.send_data import SendData
import win32clipboard, win32con
from ctypes import windll

def get_clipboard():
    win32clipboard.OpenClipboard()
    try:
        text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    except (TypeError, win32clipboard.error):
        try:
            text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            text = py3compat.cast_unicode(text, py3compat.DEFAULT_ENCODING)
        except (TypeError, win32clipboard.error):
            raise ClipboardEmpty
    finally:
        win32clipboard.CloseClipboard()
    return text

def callback(hwnd, strings):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if window_title and right - left and bottom - top:
            handle = hwnd
            strings.append({'handle': handle, 'window_title': window_title})
    return True

def get_matching_handles(title):
    win_list = []  # list of strings containing win handles and window titles
    win32gui.EnumWindows(callback, win_list)  # populate list
    r = re.compile(title)

    connect = []
    for window in win_list:
        if r.search(window['window_title']):
            connect.append(window)
    return connect

def maximize_window(handle):
    win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)

def setfocus(handle):
    win32gui.SetForegroundWindow(handle)

def focus_login():
    title = reference.VERIFICATION['f2_window']['login']
    handles = get_matching_handles(title)
    if handles:
        setfocus(handles[0])
    return None




def enumHandler(hwnd, lParam):
    global f2_hwnd
    if win32gui.IsWindowVisible(hwnd):
        if 'Connect 2000 (© Uniware Computer Systems BV) (Session 1 : 192.168.180.1)' in win32gui.GetWindowText(hwnd):
            f2_hwnd = hwnd


def Dutch_enumHandler(hwnd, lParam):
    global f2_hwnd
    if win32gui.IsWindowVisible(hwnd):
        if 'Connect 2000 (© Uniware Computer Systems BV) (Session 1 : connect.metz.com)' in win32gui.GetWindowText(
                hwnd):
            f2_hwnd = hwnd
        elif 'Connect (© Uniware Computer Systems BV) (Session 1 : connect.metz.com)' in win32gui.GetWindowText(hwnd):
            f2_hwnd = hwnd


def Canada_enumHandler(hwnd, lParam):
    global f2_hwnd
    if win32gui.IsWindowVisible(hwnd):
        if 'Connect 2000 (© Uniware Computer Systems BV) (Session 1 : 192.168.180.1)' in win32gui.GetWindowText(hwnd):
            f2_hwnd = hwnd


# def get_hwnd():
#    win32gui.EnumWindows(enumHandler, f2_hwnd) # stops when f2_hwnd is not None

def get_hwnd():
    win32gui.EnumWindows(Dutch_enumHandler, f2_hwnd)  # stops when f2_hwnd is not None


def get_corners(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x0 = rect[0]
    y0 = rect[1]
    x1 = rect[2]  # - x
    y1 = rect[3]  # - y

    return x0, y0, x1, y1


def drag_window():
    win32gui.ShowWindow(f2_hwnd, win32con.SW_MAXIMIZE)
    try:
        win32gui.SetForegroundWindow(f2_hwnd)
    except:
        get_hwnd()
        # win32gui.SetForegroundWindow(f2_hwnd)
    c = get_corners(f2_hwnd)
    mouse.click_and_drag(c[0] + 25, c[1] + 50, c[2] - 25, c[3] - 50)


def get_window(attempt=0):
    send = SendData()
    drag_window()
    send.send('%c')
    data = None
    for i in range(3):
        try:
            data = get_clipboard()
            break
        except:
            time.sleep(0.01)
    #clipboard.empty_clipboard()
    if data == None and attempt < 10:
        return get_window(attempt + 1)
    return data


f2_hwnd = None
get_hwnd()
