from verification.reference import VERIFICATION
import pyautogui
import os



def is_login_dialogue_open():
    verification_image = VERIFICATION['login']['image_screen_open']
    if  pyautogui.locateOnScreen(verification_image):
        return True
    return False

