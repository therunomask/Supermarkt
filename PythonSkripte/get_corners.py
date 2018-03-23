import cv2
import numpy as np
import copy


def get_corners(img, treshhold, oldcorners):
    LineCopy = copy.deepcopy(img)
    rows, cols, _ = img.shape
    BlackWhite = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(BlackWhite, treshhold, 255, 0)
    _, contours, _ = cv2.findContours(thresh, 1, 2)
#     cv2.imshow('img', thresh)
#     cv2.waitKey(1000)

    contours.sort(key=len, reverse=True)
    for con in contours[:1]:
        ImgTemp = np.zeros([rows, cols], dtype=np.uint8)
        for k in con:
            ImgTemp[k[0][1], k[0][0]] = np.array(255, dtype=np.uint8)
#         cv2.imshow('img', ImgTemp)
#         cv2.waitKey(100)

    LineParameters = []

    geraden = []
    for k in range(4):
        try:
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
#             cv2.imshow('img', LineCopy)
#             cv2.waitKey(100)
            cv2.line(ImgTemp, (x1, y1), (x2, y2), 0, 3)
            LineParameters.append([[x1, y2], [x2, y2]])
        except:
            return oldcorners
    corners = get_right_corners(get_all_corners(geraden))
    if len(corners) != 4:
        return oldcorners
    else:
        return corners


def corner(a, b, c, d):
    try:
        x = (-a[0] * b[1] * d[0] + a[1] * b[0] * d[0] + c[0] * b[0] *
             d[1] - b[0] * c[1] * d[0]) / (-b[1] * d[0] + b[0] * d[1])
        y = (a[0] * b[1] * d[1] - a[1] * b[0] * d[1] - b[1] * c[0] *
             d[1] + b[1] * c[1] * d[0]) / (-b[0] * d[1] + b[1] * d[0])
    except:
        return [np.NaN, np.NaN]
    return [int(x), int(y)]


def get_right_corners(corner_list):
    corner_list = [corner for corner in corner_list if corner[0]
                   is not np.NaN and corner[1] is not np.NaN]
    corner_list = np.asarray(corner_list)
    if len(corner_list) == 4:
        a = list(corner_list)
    elif len(corner_list) == 5:
        distance_list = []
        for num1, _ in enumerate(corner_list):
            distance_list.append(cornerdistance(
                [corner for num2, corner in enumerate(corner_list) if num1 != num2]))
        a = [corner for num2, corner in enumerate(
            corner_list) if np.argmin(distance_list) != num2]
    elif len(corner_list) == 6:
        distance_list = []
        hits = []
        for num1 in range(6):
            for num2 in range(num1, 6):
                hits.append([num1, num2])
                distance_list.append(cornerdistance([corner for num3, corner in enumerate(
                    corner_list) if num1 != num3 and num2 != num3]))
        a = [corner for num, corner in enumerate(corner_list) if hits[np.argmin(
            distance_list)][0] != num and hits[np.argmin(distance_list)][1] != num]
    else:
        return corner_list
    a.sort(key=lambda x: x[0] + x[1])
    a[1:3] = a[2:0:-1]
    return a


def cornerdistance(corner_list):
    dis = 0
    for corner1 in corner_list:
        for corner2 in corner_list:
            dis += np.linalg.norm(corner1 - corner2)
    return dis


def get_all_corners(geraden):
    corner_list = []
    for i in range(4):
        for j in range(i + 1, 4):
            corner_list.append(corner(geraden[i][0], geraden[i][1],
                                      geraden[j][0], geraden[j][1]))
    return corner_list
