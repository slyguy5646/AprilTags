from returnData import returnData

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