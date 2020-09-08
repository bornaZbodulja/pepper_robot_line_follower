#!/usr/bin/env python

import cv2
import numpy as np

def image_loading(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    #cv2.imshow('original image', img)
    return img

def white_segmentation(img, sensitivity):
    height, width, shape = img.shape
    descentre = 160
    rows_to_watch = 60
    width_crop_decrement = width/4
    height_crop_decrement = height/4
    croped_img = img[300:height, width_crop_decrement:(width-width_crop_decrement)]
    #print(height)
    #print(croped_img.shape)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    
    lower_white = np.array([0,0,255-sensitivity], dtype=np.uint8)
    upper_white = np.array([255,sensitivity,255], dtype=np.uint8)

    mask = cv2.inRange(hsv_img, lower_white, upper_white)

    return mask

    #cv2.imshow('filtered image', mask)

def calculating_center(filtered_image):
    moments = cv2.moments(filtered_image, False)

    cx, cy = moments['m10']/moments['m00'], moments['m01']/moments['m00']
    rounded_cx = int(round(cx))
    rounded_cy = int(round(cy))
    #print(filtered_image.shape)
    #filtered_image[(rounded_cx-5):(rounded_cx+5), (rounded_cy-5):(rounded_cy+5)] = (0,0,0)
    cv2.imshow('filtered image', filtered_image)
    return rounded_cx, rounded_cy

def main():
    path = './pepper_white_2.jpg'
    sensitivity = 15
    img = image_loading(path)
    mask = white_segmentation(img, sensitivity)
    cx, cy = calculating_center(mask)
    img[(cy-5):(cy+5), (cx-5):(cx+5)] = (0,0,0)
    print(str(cx) + ", " + str(cy))
    cv2.imshow('original image', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()