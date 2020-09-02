import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
import win32api

old_x, old_y = win32api.GetCursorPos()


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array

    [A,W,D] boolean values.
    '''
    global old_x
    global old_y

    output = [0, 0, 0, 0, 0, 0]
    new_x, new_y = win32api.GetCursorPos()
    rotation = new_x - old_x
    if rotation < 0:
        output[4] = 1
    if rotation > 0:
        output[5] = 1
    old_x, old_y = win32api.GetCursorPos()
    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    elif 'S' in keys:
        output[3] = 1
    elif 'W' in keys:
        output[1] = 1
    return output


file_name = 'training_data-4.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    #training_data = list(np.loadtxt(file_name))
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while True:

        if not paused:
            # 800x600 windowed mode
            screen = grab_screen(region=(0, 40, 1920, 1080))
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (160, 120))
            # resize to something a bit more acceptable for a CNN
            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen, output])

            if len(training_data) % 1000 == 0:
                print(len(training_data))
                np.save(file_name, training_data)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main()
