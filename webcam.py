import apriltag
from apriltag import Detector
import cv2


# img = cv2.imread('tag.jpg', cv2.IMREAD_GRAYSCALE)
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)
# result = detector.detect(img)

# tf = result[0].tag_family
# cx = result[0].center[0]


cap = cv2.VideoCapture(0)

success = cap.grab() # get the next frame
fno = 0

while success:
    if fno % 5 == 0:
        dumb, img = cap.retrieve()
        result = detector.detect(img)
        print(result)
    else:
        pass
	# read next frame
    success, img = cap.grab()











# # Check if the webcam is opened correctly
# if not cap.isOpened():
#     raise IOError("Cannot open webcam")

# while True:
#     ret, frame = cap.grab()
#     frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
#     greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('Input', greyFrame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     # for i in greyFrame:
#     #     image = greyFrame.grab()
    

# cap.release()
# cv2.destroyAllWindows()
