import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_shelf_av(img, corners, length, hight):
    pts2 = np.float32([[0, 0], [hight, 0], [0, length], [hight, length]])
    M = cv2.getPerspectiveTransform(np.float32(
        corners), pts2)
    dst = cv2.warpPerspective(img, M, (hight, length))
    av = np.sum(dst, axis=0)
#     plt.plot(list(range(len(av))), av, 'ro')
#     #plt.axis([0, 50, 0, 240000])
#     plt.pause(0.01)
#     plt.clf()
#    cv2.imshow('shelf', dst)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         pass
    return av
