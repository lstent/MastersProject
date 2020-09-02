import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D
from alexnet import alexnet
import pyautogui
import autoit
import win32api
from getkeys import key_check
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)


WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'fps-exploration-0.001-alexnetv2-10-epochs.model'.format(LR, 'alexnetv2', EPOCHS)
old_x, old_y = win32api.GetCursorPos()

def straight():
    PressKey(W)
    ReleaseKey(S)


def left():
    PressKey(A)
    ReleaseKey(D)


def rotate_left():
    x, y = win32api.GetCursorPos()
    autoit.mouse_move(x-1, y)


def rotate_right():
    x, y = win32api.GetCursorPos()
    autoit.mouse_move(x+1, y)

    
def right():
    PressKey(D)
    ReleaseKey(A)


def back():
    PressKey(S)
    ReleaseKey(W)


model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

# movement weightings
forward_weight = 0.5
left_weight = 0.015
right_weight = 0.015
back_weight = 0.003
rotate_right_weight = 0.45
rotate_left_weight = 0.4
not_going_forward_deduction = 0.07
not_going_forward_deduction_rotation = 0.07


def main():
    last_time = time.time()

    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while True:
        if not paused:
            # 800x600 windowed mode
            screen = grab_screen(region=(0, 40, 1920, 1080))
            print('loop took {} seconds'.format(time.time() - last_time))
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            #screen = cv2.resize(screen, (80, 60))
            screen = cv2.resize(screen, (160, 120))
            #prediction = model.predict([screen.reshape(80, 60, 1)])[0]
            prediction = model.predict([screen.reshape(160, 120, 1)])[0]
            print(prediction)

            # move forward
            if prediction[1] > forward_weight:
                straight()
            # if not moving forward
            if prediction[1] < forward_weight:
                ReleaseKey(W)
                # move left
                if prediction[0] > left_weight - not_going_forward_deduction:
                    left()
                # if not moving left
                if prediction[0] < left_weight - not_going_forward_deduction:
                    ReleaseKey(A)
                    # move right
                    if prediction[2] > right_weight - not_going_forward_deduction:
                        right()
                    # stop moving right
                    if prediction[2] < right_weight - not_going_forward_deduction:
                        ReleaseKey(D)
                # rotate right
                if prediction[5] > rotate_right_weight - not_going_forward_deduction_rotation:
                    rotate_right()
                # if not rotating right
                if prediction[5] < rotate_right_weight - not_going_forward_deduction_rotation:
                    # rotate left
                    if prediction[4] > rotate_left_weight - not_going_forward_deduction_rotation:
                        rotate_left()
                # move back
                if prediction[3] > back_weight:
                    back()
                # stop moving back
                if prediction[3] < back_weight:
                    ReleaseKey(S)
            # move left
            if prediction[0] > left_weight:
                left()
            # if not moving left
            if prediction[0] < left_weight:
                ReleaseKey(A)
                # move right
                if prediction[2] > right_weight:
                    right()
                # stop moving right
                if prediction[2] < right_weight:
                    ReleaseKey(D)
            # rotate right
            if prediction[5] > rotate_right_weight:
                rotate_right()
            # if not rotating right
            if prediction[5] < rotate_right_weight:
                # rotate left
                if prediction[4] > rotate_left_weight:
                    rotate_left()

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


main()
