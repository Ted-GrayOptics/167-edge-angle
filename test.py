import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import time



def line_to_point_distance(a,b,c,x0,y0):
    return abs(a*x0 + b*y0 + c) / math.sqrt(a*a+b*b)
def point_to_point_distance(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2 + (y0-y1)**2)

def find_chessboard(image, pattern_size):
    flags = 0
    flags |= cv2.CALIB_CB_ADAPTIVE_THRESH
    flags |= cv2.CALIB_CB_FAST_CHECK

    rv, points = cv2.findChessboardCorners(image, (pattern_size[0],pattern_size[1]), flags=flags)

    if not rv:
        return None
    else:
        return points 

image = cv2.imread('Image0.bmp',cv2.IMREAD_UNCHANGED)
resize_fraction = 0.2
roi_crop_fraction = 1
pattern_size = [5, 4]


start_time = time.time()
roi_width = roi_crop_fraction * image.shape[1] 
roi_height = roi_crop_fraction * image.shape[0]

diff_roi_width = image.shape[1] - roi_width
diff_roi_height = image.shape[0] - roi_height


x,y,w,h= [ int(diff_roi_width/2), int(diff_roi_height/2), int(roi_width), int(roi_height) ]
image = image[y:y+h, x:x+w].copy()

image = cv2.resize(image, (int(image.shape[1] * resize_fraction), int(image.shape[0] * resize_fraction)), interpolation = cv2.INTER_AREA)

corners = None
t=0
while corners is None:
    corners = find_chessboard(image, pattern_size)
    if corners is None:
        pattern_size[t] = pattern_size[t] - 1
        t = 1 - t
        if pattern_size[0] <=2 or pattern_size[1] <=2:
            print('Failed!')
            exit()

# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (image.shape[0],image.shape[1]),None,None)

# undistort
# u_image = cv2.undistort(image, mtx, dist, None, None)
# u_corners = cv2.undistortPoints(corners,mtx,dist,None,mtx)
#u_corners = find_chessboard(u_image)

# viz = u_image.copy()
# cv2.drawChessboardCorners(viz, pattern_size, u_corners, True)
# cv2.imshow('Viz',viz)
# cv2.waitKey(0)

center = (int(image.shape[1]/2),int(image.shape[0]/2))
lines = np.split(corners, pattern_size[1])

angles = []
distances_to_center = []
f_lines = []
for line in lines:
    line = np.reshape(line,(line.shape[0],line.shape[2]))
    points_to_center_distance = []
    for point in line:        
        points_to_center_distance.append(point_to_point_distance(point[0],point[1],center[0],center[1]))

    min_val = 99999999999999
    min_idx = 0
    for idx, val in enumerate(points_to_center_distance):
        if val < min_val:
            min_val = val
            min_idx = idx

    p1 = line[min_idx]  
    points_to_center_distance[min_idx] = 9999999999999
    min_val = 99999999999999
    min_idx = 0
    for idx, val in enumerate(points_to_center_distance):
        if val < min_val:
            min_val = val
            min_idx = idx
    p2 = line[min_idx]  
    
    xs = [p1[0], p2[0]]
    ys = [p1[1], p2[1]]
    fitted = np.polyfit(xs, ys, 1)
    angles.append(math.atan(fitted[0]) *180/math.pi)
    distances_to_center.append(line_to_point_distance(fitted[0],-1,fitted[1],center[0],center[1]))
    f_lines.append(fitted)


min_idx = distances_to_center.index(min(distances_to_center))
angle = angles[min_idx]
f_line = f_lines[min_idx]
fps = round(1/(time.time() - start_time))
print("FPS = " + str(fps))

print('angle = ' + str(angle))
pt1 = (int(-1000),int(f_line[0]*(-1000) + f_line[1]))
pt2 = (int(+5000),int(f_line[0]*(+5000) + f_line[1]))
cv2.namedWindow('Viz', cv2.WINDOW_NORMAL)
viz = image.copy()
cv2.line(viz,pt1,pt2,(0,0,255),3)
cv2.drawChessboardCorners(viz, (pattern_size[0],pattern_size[1]), corners, True)
angle_str = '{0:.2f}'.format(angle)
cv2.putText(viz,angle_str,center,1,4,(255,0,0),4)
cv2.imshow('Viz',viz)
cv2.waitKey(0)

cv2.destroyAllWindows()