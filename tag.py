#!/usr/bin/env python
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
import cv2
import apriltag
import numpy as np
import json
import threading
import tkinter

def checkNumDetections(ifBlank, argToSet):
    if ifBlank == 0:
        data = '0'
    else:
        data = argToSet
    return argToSet

def main():

    parser = ArgumentParser(
        description='test apriltag Python bindings')

    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')

    apriltag.add_arguments(parser)

    options = parser.parse_args()

    try:
        cap = cv2.VideoCapture(int(options.device_or_movie))
    except ValueError:
        cap = cv2.VideoCapture(options.device_or_movie)

    window = 'Camera'
    cv2.namedWindow(window)

    dataWindow = 'Tag Data'
    cv2.namedWindow(dataWindow)

    whiteBackground = cv2.imread('apriltagcontrol.jpg')
    whiteBackgroundWithText = cv2.imread('apriltagcontrol.jpg')

    
    detector = apriltag.Detector(options,
                                 searchpath=apriltag._get_demo_searchpath())
    loopBool = True
    
    while True:


        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        detections, dimg = detector.detect(gray, return_image=True)
        
        for i, j in enumerate(detections):
            listVar = j.tostring(indent=2)
            print(type(listVar))
            stringCode = listVar.format()
            print(stringCode)


        num_detections = len(detections)
        # print('Detected {} tags.\n'.format(num_detections))
        num_detections_string = str(num_detections)


        overlay = frame // 2 + dimg[:, :, None] // 2

        # clear_text = ''
        # text = checkNumDetections(num_detections, num_detections_string)
        
        # cv2.putText(whiteBackground, clear_text, (100, 100), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 0), 2)
        # cv2.putText(whiteBackground, text, (100, 100), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 0), 2)
        cv2.imshow(window, overlay)
        k = cv2.waitKey(1)
        # cv2.imshow(dataWindow, whiteBackground)

        if k == 27:
            break
        loopBool = False

# if __name__ == '__main__':
#     main()
main()