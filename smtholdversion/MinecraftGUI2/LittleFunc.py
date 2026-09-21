

import pyautogui


def turn(vectx, vecty):
    x, y = pyautogui.position()
    pyautogui.moveTo(vectx, vecty)