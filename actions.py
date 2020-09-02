import autoit
import win32api
import pyautogui
from directkeys import PressKey, ReleaseKey, W, A, S, D


def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)


def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(S)


def rotate_left():
    x, y = win32api.GetCursorPos()
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)
    autoit.mouse_move(0, y)
    pyautogui.moveTo(x, y)


def rotate_right():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)
    x, y = win32api.GetCursorPos()
    autoit.mouse_move(1900, y)
    pyautogui.moveTo(x, y)


def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(S)


def stop():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)


def back():
    PressKey(S)
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def action(self, choice):
    # Gives us 6 total movement options. (0,1,2,3,4,5,6)
    if choice == 0:
        straight()

    elif choice == 1:
        back()

    elif choice == 2:
        left()

    elif choice == 3:
        right()

    elif choice == 4:
        rotate_left()

    elif choice == 5:
        rotate_right()

    elif choice == 6:
        stop()
