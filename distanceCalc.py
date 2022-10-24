from tagData import tagData
from C270Calibration.C270 import cameraMatrix, dist
import cv2
import numpy as np

########## PLAN FOR DISTANCE CALCULATION ##########
"""
Know the measurement of the april tags (in our case 100mm squares) and know the measurement of april tag in 
pixels when it is a set distance away from the camera (e.g. april tag is a 500 pixel square when it is 1 ft away from the camera) then do 
that math to scale it back up to 100mm along with the distance from the camera so we can figure out distance

OR

Use homography data (this is probably simpler overall)

OR 

Maybe checkout this package: https://satellogic.github.io/homography/

OR

This equation: https://www.reddit.com/r/logitech/comments/r6grj8/logitech_c270_specs/
"""


def calculateDistance(focalLengthMM, objectHeightMM, imageHeightPixels, objectHeightPixels, sensorHeightMM):
    numerator = (focalLengthMM * objectHeightMM * imageHeightPixels) 
    denominator = objectHeightPixels * sensorHeightMM
    return numerator / denominator


def PnPSolverTest(lengthOfTag, corners):
    objectPoints = np.array([
    [-lengthOfTag/2, lengthOfTag/2, 0], 
    [lengthOfTag/2, lengthOfTag/2, 0], 
    [lengthOfTag/2, -lengthOfTag/2, 0], 
    [-lengthOfTag/2, -lengthOfTag/2, 0]
    ])
    cv2.solvePnP(objectPoints, corners, cameraMatrix, dist)
    Z = np.zeros((4))
    retval,R, T = cv2.solvePnP(objectPoints,corners,cameraMatrix,dist) #from chessboard coordinate space to camera coordinate space
    R,jacobian = cv2.Rodrigues(R) #from R-vector to R-matrix
    for i in range(0,len(objectPoints)):
        point = np.dot(objectPoints[i],R) + np.matrix.transpose(T)
        # Z[i] = point[0,2] * 1000 #Z-value to mm
    
    return np.round(Z.reshape(2,2)), point

