#!/usr/bin/env python
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
from textwrap import indent
from xml.etree.ElementTree import tostring
import cv2
import apriltag
from returnData import tagData

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

    # set up a reasonable search path for the apriltag DLL inside the
    # github repo this file lives in;
    #
    # for "real" deployments, either install the DLL in the appropriate
    # system-wide library directory, or specify your own search paths
    # as needed.
    
    detector = apriltag.Detector(options,
                                 searchpath=apriltag._get_demo_searchpath())

    while True:

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
            tagId = tagDataDict['ID']
            hammingError = tagDataDict['Hamming error']
            goodness = tagDataDict['Goodness']
            decisionMargin = tagDataDict['Decision margin']
            homography = tagDataDict['Homography']
            center = tagDataDict['Center']
            corners = tagDataDict['Corners']
            print(tagId)
            # if len(tagData) > 1:
            #     for i in tagData[1:]:
            #         scndTagDataDict = tagData[1]
            #         print(scndTagDataDict['ID'])
            
            
        overlay = frame // 2 + dimg[:, :, None] // 2
        cv2.imshow(window, overlay)
        k = cv2.waitKey(1)

        if k == 27:
            break
if __name__ == '__main__':
    main()





