#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from math import sqrt

"""
ONLY WORKING ON PYTHON 3.7.1 AS FAR AS MY TESTING GOES
"""
from distanceCalc import *
from argparse import ArgumentParser
import cv2
import apriltag
from tagData import tagData
import numpy as np
from array import *
from C270Calibration.C270 import *


# for some reason pylint complains about members being undefined
# pylint: disable=E1101

def main():
    

    '''Main function.'''

    parser = ArgumentParser(
        description='test apriltag Python bindings')

    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')

    apriltag.add_arguments(parser)

    options = parser.parse_args()


    #######WEBCAM STREAM#########
    try:
        cap = cv2.VideoCapture(int(options.device_or_movie))
    except ValueError:
        cap = cv2.VideoCapture(options.device_or_movie)
    ###########

    #####CAM WINDOW####
    window = 'Camera'
    cv2.namedWindow(window, cv2.WINDOW_KEEPRATIO)
    ##########

    ####DATA WINDOW#####
    dataWindow = 'Tag Data'
    cv2.namedWindow(dataWindow, cv2.WINDOW_NORMAL)
    whiteBackground = np.full((1000, 1000, 1), 255, dtype = "uint8") #set window to white on startup
    ########

    detector = apriltag.Detector(options,
                                 searchpath=apriltag._get_demo_searchpath())

    while True:
        whiteBackground = np.full((1000, 1000, 1), 255, dtype = "uint8") #set data window to white every time loop iterates (makes data update on the window)
        success, frame = cap.read() #read webcam stream
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) #convert webcam to gray
        detections, dimg = detector.detect(gray, return_image=True) #detect tags
        num_detections = len(detections)
        # print('Detected {} tags.\n'.format(num_detections))
        

        for i, detection in enumerate(detections, 0):
            # print('Detection {} of {}:'.format(i+1, num_detections))
            # print()
            
            
            
            data = detection.tostring(indent=0) #data from tag
            tagData.clear() #clear my list of the data
            tagData.append(data) #add the new tag data to my list
            tagDataDict = tagData[0]    #get the dict of the data from my list
            tagFamily = tagDataDict['Family']
            tagId = tagDataDict['ID']
            hammingError = tagDataDict['Hamming error']
            goodness = tagDataDict['Goodness']
            decisionMargin = tagDataDict['Decision margin']
            tagHomography = tagDataDict['Homography']
            tagCenter = tagDataDict['Center']
            #####CORNERS######
            corners = tagDataDict['Corners']
            tagCornersRounded = corners.round(decimals=2)
            #cornersList = corners.tolist() ##########THIS IS HOW YOU CHANGE AN NUMPY NDARRAY TO A REGULAR PYTHON USABLE LIST
            tagCorner1 = {'X': float(corners[0][0]), 'Y': float(corners[0][1])}
            tagCorner2 = {'X': float(corners[1][0]), 'Y': float(corners[1][1])}
            tagCorner3 = {'X': float(corners[2][0]), 'Y': float(corners[2][1])}
            tagCorner4 = {'X': float(corners[3][0]), 'Y': float(corners[3][1])}
            # print(corners)
            ####################

            #####Distance between tag corner 1 and 2 (in pixels)######
            xPartForEquation = (tagCorner2['X'] - tagCorner1['X']) ** 2
            yPartForEquation = (tagCorner2['Y']- tagCorner1['Y']) ** 2
            tagHeight = sqrt(xPartForEquation + yPartForEquation)
            # print(tagHeight)
            #######################

            objectPointsForPNP = np.array([[-0.060325/2, 0.060325/2, 0],
                                            [0.060325/2, 0.060325/2, 0],
                                            [0.060325/2, -0.060325/2, 0],
                                            [-0.060325/2, -0.060325/2, 0]])

            ###### CAN NOW GET BOTH ROTATION AND TRANSLATION MATRICES FROM HOMOGRAPHY MATRIX ######
            value = cv2.decomposeHomographyMat(tagHomography, cameraMatrixFromLibrary) #####GIVES YOU THREE OF EACH ROTATION AND TRANSLATION MATRICES
            print(value)
            
            #####CALCULATE DISTANCE TO APRILTAG with some pretty sketchy math#####
            straightDistanceToTag = calculateDistance(4.22, 100, 720, tagHeight, 2.02)
            straightDistanceToTagInches = straightDistanceToTag / 25.4
            # print(f"My distance estimation (inches): {poseZInches - 10}")
            # print()

            

            #####DICTIONARY OF DATA AND PIXEL COORDINATES TO SEND TO DATA WINDOW######
            guiListText = {
                'Family': [f'Family: {tagFamily}', 50],
                'ID': [f'ID: {tagId}', 100], 
                'HammingError': [f'Hamming Error: {hammingError}', 150], 
                'Goodness': [f'Goodness: {goodness}', 200], 
                'DecisionMargin': [f'Decision Margin: {round(decisionMargin)}%', 250]
                # 'Homography': [f'Homography: {tagHomography}', 350], 
                # 'Center': [f'Center: {tagCenter}', 400], 
                #'Corners': [f'Corners: {tagCorners}', 450]
            }
            ##############


            ####FOR LOOP TO PUT DATA ON DATA WINDOW####
            for key in guiListText.keys():
                listOfStringAndPos = guiListText[key]
                cv2.putText(whiteBackground, listOfStringAndPos[0], (25, listOfStringAndPos[1]), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            ############


        
        overlay = frame // 2 + dimg[:, :, None] // 2 #overlay tag border
        cv2.imshow(window, overlay) #show webcam window with overlay
        cv2.imshow(dataWindow, whiteBackground) #show data window
        k = cv2.waitKey(1)

        if k == 27:
            break
if __name__ == '__main__':
    main()





