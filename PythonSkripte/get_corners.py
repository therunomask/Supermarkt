import cv2
import numpy as np
import copy


def get_corners(img, treshhold):
    LineCopy = copy.deepcopy(img)
    rows, cols, _ = img.shape
    BlackWhite = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(BlackWhite, treshhold, 255, 0)
    _, contours, _ = cv2.findContours(thresh, 1, 2)
    #cv2.imshow('img', thresh)
    # cv2.waitKey(1000)

    contours.sort(key=len, reverse=True)
    for con in contours[:1]:
        ImgTemp = np.zeros([rows, cols], dtype=np.uint8)
        for k in con:
            ImgTemp[k[0][1], k[0][0]] = np.array(255, dtype=np.uint8)
        #cv2.imshow('img', ImgTemp)
        # cv2.waitKey(1000)

    LineParameters = []

    geraden = []
    for k in range(4):
        lines = cv2.HoughLines(ImgTemp, 1, np.pi / 180, 10)

        a = np.cos(lines[0][0][1])
        b = np.sin(lines[0][0][1])
        x0 = a * lines[0][0][0]
        y0 = b * lines[0][0][0]
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        geraden.append([[x1, y1], [x2 - x1, y2 - y1]])

        cv2.line(LineCopy, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.line(ImgTemp, (x1, y1), (x2, y2), 0, 20)
        LineParameters.append([[x1, y2], [x2, y2]])
    return get_right_corners(get_all_corners(geraden))


def corner(a, b, c, d):
    x = (-a[0] * b[1] * d[0] + a[1] * b[0] * d[0] + c[0] * b[0] *
         d[1] - b[0] * c[1] * d[0]) / (-b[1] * d[0] + b[0] * d[1])
    y = (a[0] * b[1] * d[1] - a[1] * b[0] * d[1] - b[1] * c[0] *
         d[1] + b[1] * c[1] * d[0]) / (-b[0] * d[1] + b[1] * d[0])
    return [int(x), int(y)]


def get_right_corners(corner_list):
    corner_list = np.asarray(corner_list)
    middle = np.array([0.0, 0.0])
    for corner in corner_list:
        middle += corner
    middle /= 6
    corner_list = sorted(corner_list, key=lambda x: np.linalg.norm(x - middle))
    return corner_list[:4]


def get_all_corners(geraden):
    corner_list = []
    for i in range(4):
        for j in range(i + 1, 4):
            corner_list.append(corner(geraden[i][0], geraden[i][1],
                                      geraden[j][0], geraden[j][1]))
    return corner_list
