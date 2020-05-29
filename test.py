from angle_estimator.AngleEstimator import AngleEstimator
import time
import cv2
from os import listdir
from os.path import isfile, join


estimator = AngleEstimator(resize_factor = 1.0, crop_factor = 0.5, max_pattern_size = [4,3], min_pattern_size = [4,3])
cv2.namedWindow('Viz', cv2.WINDOW_NORMAL)

process = 'test'

if process == 'test':
    test_images = [f for f in listdir('./TestImages/') if isfile(join('./TestImages/', f))]
    for test_image in test_images:
        image = cv2.imread('./TestImages/' + test_image, cv2.IMREAD_UNCHANGED)
        start_time = time.time()
        angle, p1, p2 = estimator.Estimate(image)
        end_time = time.time()
        fps = round(1 / (end_time - start_time))
        #print('FPS = ' + str(fps))
        if angle is None or p1 is None or p2 is None:
            print(test_image + ' Fail!')
            viz = image
        else:   
            print(test_image + ' Success! angle = ' + str(angle))
            viz = estimator.RenderResult(image, angle, p1, p2)
        cv2.imshow('Viz', viz)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
else:
    cap = cv2.VideoCapture("C:/GrayOptics/RollImages/WIN_20200527_11_49_50_Pro_compress.mp4")
    ret, image = cap.read()
    output_video_size = (int(image.shape[1]/2), int(image.shape[0]/2))
    out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, output_video_size)
    frame_idx = 0
    while(True):
        ret, image = cap.read()
        if ret == False:
            break
        start_time = time.time()
        angle, p1, p2 = estimator.Estimate(image)
        end_time = time.time()
        fps = round(1 / (end_time - start_time))
        #print('FPS = ' + str(fps))
        if angle is None or p1 is None or p2 is None:
            print('Frame #' + str(frame_idx) + ' Fail!')
            viz = image
        else:   
            print('Frame #' + str(frame_idx) + ' Success! angle = ' + str(angle))
            viz = estimator.RenderResult(image, angle, p1, p2)
        viz = cv2.resize(viz, output_video_size)
        cv2.imshow('Viz', viz)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        out.write(viz)
        frame_idx += 1
        
cv2.destroyAllWindows()
cap.release()
out.release()