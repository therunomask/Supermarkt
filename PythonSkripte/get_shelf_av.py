import cv2
import numpy as np
import copy


def get_shelf_av(img, corners, length, hight):
    pts2 = np.float32([[0, 0], [hight, 0], [0, length], [hight, length]])
    M = cv2.getPerspectiveTransform(np.float32(
        corners), pts2)
    dst = cv2.warpPerspective(img, M, (hight, length))
    av = np.sum(dst, axis=1)
    return av
