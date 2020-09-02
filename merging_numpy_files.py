import numpy as np
import os
import cv2


# Merge all our training data files into one file
def merge_training_data():
    starting_value = 1
    train_data = np.load('training_data-{}.npy'.format(starting_value), allow_pickle=True)
    train_data_arr = []
    # load training data from pc
    while True:
        file_name = 'training_data-{}.npy'.format(starting_value)
        if os.path.isfile(file_name):
            train_data_arr += list(np.load(file_name, allow_pickle=True))
            starting_value += 1
        else:
            print('File does not exist, finished merging!', starting_value)
            train_data_arr = np.array(train_data_arr)
            print('created array')
            np.save(file_name, train_data_arr)
            print('saved')
            break


'''#testing
starting_value = 4
train_data = np.load('training_data-{}.npy'.format(starting_value), allow_pickle=True)
for data in train_data:
    img = cv2.imread(data[0])
    choice = data[1]
    cv2.imshow('test', img)
    print(choice)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break'''


merge_training_data()