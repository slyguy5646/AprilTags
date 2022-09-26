import apriltag
import cv2
from webcam import greyFrame, image


# img = cv2.imread('tag.jpg', cv2.IMREAD_GRAYSCALE)
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)
# result = detector.detect(img)

# tf = result[0].tag_family
# cx = result[0].center[0]


        


