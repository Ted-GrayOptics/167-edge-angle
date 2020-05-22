from angle_estimator.AngleEstimator import AngleEstimator
import time
import cv2


image = cv2.imread('Image0.bmp', cv2.IMREAD_UNCHANGED)

estimator = AngleEstimator(resize_factor = 0.5, crop_factor = 0.8, pattern_size = [4,4])
start_time = time.time()
angle, p1, p2 = estimator.Estimate(image)
end_time = time.time()
fps = round(1 / (end_time - start_time))
print('FPS = ' + str(fps))

if angle is None or p1 is None or p2 is None:
    print('Fail!')
else:   
    print('angle = ' + str(angle))
    cv2.namedWindow('Viz', cv2.WINDOW_NORMAL)
    viz = estimator.RenderResult(image, angle, p1, p2)
    cv2.imshow('Viz', viz)
    cv2.waitKey(0)
    cv2.destroyAllWindows()