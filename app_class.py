import numpy as np
import cv2
import time
from grabscreen import grab_screen





def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    # blur
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    # corner detection
    corners = cv2.goodFeaturesToTrack(processed_img, 100, 0.01, 10)
    corners = np.int0(corners)
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(processed_img, (x, y), 3, 255, -1)


    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                                     rho   theta   thresh  min length, max gap:
    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, 30, 15)
    return processed_img, original_image


def main():
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
    last_time = time.time()
    
    while True:
        screen = grab_screen(region=(0, 40, 1920, 1080))
        print('Frame took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        new_screen, original_image = process_img(screen)
        #cv2.imshow('window', new_screen)

        #cv2.imshow('window2', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))


        cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


main()
