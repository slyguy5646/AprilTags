import numpy as np
import cv2
import glob

checkerBoardSize = (7,7)
frameSize = (1280, 720)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


objp = np.zeros((checkerBoardSize[0] * checkerBoardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:checkerBoardSize[0], 0:checkerBoardSize[1]].T.reshape(-1, 2)

objPoints = []
imgPoints = []

images = glob.glob('*.png')

for image in images:
    print(image)
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, checkerBoardSize, None)


    if ret == True:
        objPoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgPoints.append(corners)

        cv2.drawChessboardCorners(img, checkerBoardSize, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(1000)

cv2.destroyAllWindows()

ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, frameSize, None, None)

# print("camera calibrate: ", ret)
print(cameraMatrix)
# print(f'Distortion:\n{dist}')
# print(f'RotationVectors:\n{rvecs}')
# print(f'TranslationalVectors:\n{tvecs}')


img = cv2.imread('opencv_frame_0.png')
h, w = img.shape[:2]
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 0, (w,h))

#undistort
dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
#crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
# cv2.imwrite('result.png', dst)

# undistort
mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
# cv2.imwrite('calibresult.png', dst)


mean_error = 0
for i in range(len(objPoints)):
    imgpoints2, _ = cv2.projectPoints(objPoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv2.norm(imgPoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objPoints)) )



print(newCameraMatrix)
print(type(newCameraMatrix))













