import apriltag
import cv2


def detectFromImage(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    options = apriltag.DetectorOptions(families="tag36h11")
    detector = apriltag.Detector(options)
    result = detector.detect(img)

    try:
        tf = result[0].tag_family
        cx = result[0].center[0]
        print(tf, cx)
    
    except:
        print('No April Tag was detected')

detectFromImage('phoneTag.jpg')

        


