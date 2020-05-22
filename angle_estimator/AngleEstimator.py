import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import time

class AngleEstimator:

    def __init__(
        self,
        resize_factor,
        crop_factor,
        pattern_size,
        ):
        self.resize_factor = resize_factor
        self.crop_factor = crop_factor
        self.pattern_size = pattern_size

    def Estimate(self, image):
        roi = self.__ResizeAndCrop(image)
        corners, pattern_size = self.__DetectCorners(roi)
        if corners is None:
            return None, None, None
        angle, p1, p2 =  self.__EstimateAngle(roi, corners, pattern_size)
        if self.resize_factor != 1:
            p1[0] /= self.resize_factor
            p1[1] /= self.resize_factor
            p2[0] /= self.resize_factor
            p2[1] /= self.resize_factor
        if self.crop_factor != 1:
            p1[0] += (1 - self.crop_factor) * image.shape[1] / 2
            p1[1] += (1 - self.crop_factor) * image.shape[0] / 2
            p2[0] += (1 - self.crop_factor) * image.shape[1] / 2
            p2[1] += (1 - self.crop_factor) * image.shape[0] / 2
        return angle, p1, p2

    def RenderResult(self, image, angle, p1, p2):
        viz = image.copy()
        cv2.line(viz, (int(p1[0]),int(p1[1])), (int(p2[0]),int(p2[1])), (0, 0, 255), 3)
        # cv2.drawChessboardCorners(viz, (pattern_size[0],pattern_size[1]), corners, True)
        angle_str = '{0:.2f}'.format(angle)
        cv2.putText(
            viz,
            angle_str,
            (int(image.shape[1] / 2), int(image.shape[0] / 2)),
            1,
            4,
            (255, 0, 0),
            4,
            )
        return viz

    def __LineToPointDistance(
        self,
        a,
        b,
        c,
        x0,
        y0,
        ):
        return abs(a * x0 + b * y0 + c) / math.sqrt(a * a + b * b)

    def __PointToPointDistance(
        self,
        x0,
        y0,
        x1,
        y1,
        ):
        return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

    def __FindChessboard(self, image, pattern_size):
        flags = 0
        flags |= cv2.CALIB_CB_ADAPTIVE_THRESH
        flags |= cv2.CALIB_CB_FAST_CHECK
        (rv, points) = cv2.findChessboardCorners(image,
                (pattern_size[0], pattern_size[1]), flags=flags)
        if not rv:
            return None
        else:
            return points

    def __ResizeAndCrop(self, image):
        roi_width = self.crop_factor * image.shape[1]
        roi_height = self.crop_factor * image.shape[0]
        diff_roi_width = image.shape[1] - roi_width
        diff_roi_height = image.shape[0] - roi_height
        (x, y, w, h) = [int(diff_roi_width / 2),
                        int(diff_roi_height / 2), int(roi_width),
                        int(roi_height)]
        image = image[y:y + h, x:x + w].copy()
        image = cv2.resize(image, 
                            (int(image.shape[1] * self.resize_factor),
                            int(image.shape[0] * self.resize_factor)),
                            interpolation=cv2.INTER_AREA)
        return image

    def __DetectCorners(self, image):
        corners = None
        t = 0
        pattern_size = self.pattern_size
        while corners is None:
            corners = self.__FindChessboard(image, pattern_size)
            if corners is None:
                pattern_size[t] = pattern_size[t] - 1
                t = 1 - t
                if pattern_size[0] <= 2 or pattern_size[1] <= 2:
                    return None, None
        return corners, pattern_size

    def __EstimateAngle(self, image, corners, pattern_size):
        center = (int(image.shape[1] / 2), int(image.shape[0] / 2))
        direction = math.atan2(corners[0][0][1] - corners[1][0][1],
                                corners[0][0][0] - corners[1][0][0])
        if direction > 3 * math.pi / 4 or direction < -3 * math.pi \
            / 4 or abs(direction - 0) < math.pi / 4:
            flip = False
        else:
            flip = True
        lines = np.split(corners, pattern_size[1])
        for i in range(0, len(lines)):
            lines[i] = np.squeeze(lines[i], 1)
        lines = np.array(lines)
        flipped_lines = np.zeros((lines.shape[1], lines.shape[0],
                lines.shape[2]))
        if flip:
            for i in range(0, len(lines)):
                for j in range(0, len(lines[i])):
                    flipped_lines[j][i] = lines[i][j]
            lines = flipped_lines
        angles = []
        distances_to_center = []
        f_lines = []
        p1s = []
        p2s = []
        for line in lines:
            points_to_center_distance = []
            for point in line:
                points_to_center_distance.append(self.__PointToPointDistance(point[0],
                        point[1], center[0], center[1]))
            min_val = float('inf')
            min_idx = 0
            for (idx, val) in enumerate(points_to_center_distance):
                if val < min_val:
                    min_val = val
                    min_idx = idx

            p1 = line[min_idx]
            points_to_center_distance[min_idx] = float('inf')
            min_val = float('inf')
            min_idx = 0
            for (idx, val) in enumerate(points_to_center_distance):
                if val < min_val:
                    min_val = val
                    min_idx = idx
            p2 = line[min_idx]
            xs = [p1[0], p2[0]]
            ys = [p1[1], p2[1]]
            fitted = np.polyfit(xs, ys, 1)
            angles.append(math.atan(fitted[0]) * 180 / math.pi)
            distances_to_center.append(self.__LineToPointDistance(fitted[0],
                    -1, fitted[1], center[0], center[1]))
            f_lines.append(fitted)
            p1s.append(p1)
            p2s.append(p2)

        min_idx = \
            distances_to_center.index(min(distances_to_center))
        angle = angles[min_idx]
        p1 = p1s[min_idx]
        p2 = p2s[min_idx]
        return (angle, p1, p2)