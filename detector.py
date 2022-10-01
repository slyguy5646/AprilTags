#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from math import sqrt

from C270Calibration.C270 import noDistMatrix, cameraMatrix
from distanceCalc import calculateDistance
from argparse import ArgumentParser
from array import array
from os import remove
from textwrap import indent
from tkinter import font
import cv2
from cv2 import displayStatusBar, displayOverlay
import apriltag
from tagData import tagData
import numpy as np
from array import *


# for some reason pylint complains about members being undefined :(
# pylint: disable=E1101

def main():

    '''Main function.'''

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
    cv2.namedWindow(window, cv2.WINDOW_KEEPRATIO)
    



    dataWindow = 'Tag Data'
    cv2.namedWindow(dataWindow, cv2.WINDOW_NORMAL)
    whiteBackground = np.full((1000, 1000, 1), 255, dtype = "uint8")
    # set up a reasonable search path for the apriltag DLL inside the
    # github repo this file lives in;
    #
    # for "real" deployments, either install the DLL in the appropriate
    # system-wide library directory, or specify your own search paths
    # as needed.
    
    detector = apriltag.Detector(options,
                                 searchpath=apriltag._get_demo_searchpath())

    while True:
        whiteBackground = np.full((1000, 1000, 1), 255, dtype = "uint8")
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        detections, dimg = detector.detect(gray, return_image=True)
        detector1 = detector.detect(gray)
        num_detections = len(detections)
        print('Detected {} tags.\n'.format(num_detections))

        for i, detection in enumerate(detections, 0):
            print('Detection {} of {}:'.format(i+1, num_detections))
            print()
            
            data = detection.tostring(indent=0) #data from tag
            tagData.clear() #clear my list of the data
            tagData.append(data) #add the new tag data to my list
            tagDataDict = tagData[0]    #get the dict of the data from my list
            tagFamily = tagDataDict['Family']
            tagId = tagDataDict['ID']
            hammingError = tagDataDict['Hamming error']
            goodness = tagDataDict['Goodness']
            decisionMargin = tagDataDict['Decision margin']
            homography = tagDataDict['Homography']
            center = tagDataDict['Center']
            corners = tagDataDict['Corners']
            cornersRounded = corners.round(decimals=2)
            #cornersList = corners.tolist() ##########THIS IS HOW YOU CHANGE AN NUMPY NDARRAY TO A REGULAR PYTHON USABLE LIST
            corner1 = {'X': float(corners[0][0]), 'Y': float(corners[0][1])}
            corner2 = {'X': float(corners[1][0]), 'Y': float(corners[1][1])}
            corner3 = {'X': float(corners[2][0]), 'Y': float(corners[2][1])}
            corner4 = {'X': float(corners[3][0]), 'Y': float(corners[3][1])}

            xPartForEquation = (corner2['X'] - corner1['X']) ** 2
            yPartForEquation = (corner2['Y']- corner1['Y']) ** 2
            tagHeight = sqrt(xPartForEquation + yPartForEquation)
            # print(tagHeight)
            
            straightDistanceToTag = calculateDistance(3.22, 100, 720, tagHeight, 2.02)
            straightDistanceToTagInches = straightDistanceToTag / 25.4
            # print(straightDistanceToTagInches)
            guiListText = {
                'Family': [f'Family: {tagFamily}', 50],
                'ID': [f'ID: {tagId}', 100], 
                'HammingError': [f'Hamming Error: {hammingError}', 150], 
                'Goodness': [f'Goodness: {goodness}', 200], 
                'DecisionMargin': [f'Decision Margin: {round(decisionMargin)}%', 250],
                'Distance to Tag': [f'Distance to Tag: {round(straightDistanceToTagInches)}', 300] 
                # 'Homography': [f'Homography: {homography}', 300], 
                # 'Center': [f'Center: {center}', 350], 
                #'Corners': [f'Corners: {corners}', 400]
            }
            
            # print('Corner Coordinates:' + str(corner1) + str(corner2) + str(corner3), str(corner4))
            # print(f'Homography Coordinates:\n {homography}')
            # print('Center Coordinates:' + str(center))

            
            


            
            # if len(tagData) > 1:
            #     for i in tagData[1:]:
            #         scndTagDataDict = tagData[1]
            #         print(scndTagDataDict['ID'])
            for key in guiListText.keys():
                listOfStringAndPos = guiListText[key]
                cv2.putText(whiteBackground, listOfStringAndPos[0], (25, listOfStringAndPos[1]), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)



            
        overlay = frame // 2 + dimg[:, :, None] // 2
        cv2.imshow(window, overlay)
        cv2.imshow(dataWindow, whiteBackground)
        k = cv2.waitKey(1)

        if k == 27:
            break
if __name__ == '__main__':
    main()





