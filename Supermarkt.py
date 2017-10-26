import cv2
import numpy as np
import copy

img = cv2.imread('/Users/noeth/Documents/Supermarkt/ReinGruen.jpeg')


ImgTemp = np.zeros([1280, 720], dtype=np.uint8)
LineCopy = copy.deepcopy(img)

BlackWhite = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = np.asarray((BlackWhite > 127) * 255, dtype=np.uint8)

#ret,thresh = cv2.threshold(BlackWhite,200,255,0)
image, contours, hierarchy = cv2.findContours(thresh, 1, 2)


contours.sort(key=len, reverse=True)

for k in contours[0]:
    ImgTemp[k[0][1], k[0][0]] = np.array(255, dtype=np.uint8)

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


def conner(a, b, c, d):
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


cone = conner(geraden[3][0], geraden[3][1],
              geraden[1][0], geraden[1][1])
print(LineCopy[cone[0], cone[1]])
LineCopy[cone[0], cone[1]] = [255, 0, 0]


rows, cols, ch = img.shape

pts1 = np.float32(get_right_corners(get_all_corners(geraden)))
pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

M = cv2.getPerspectiveTransform(pts1, pts2)
print(M)

dst = cv2.warpPerspective(img, M, (300, 300))


cv2.imshow('img', dst)
cv2.waitKey(0)

# = (255, 0, 0)
cv2.circle(LineCopy, (cone[0], cone[1]), 5, (255, 0, 0))

cv2.imshow('houghlines3.jpeg', LineCopy)

cv2.waitKey(0)

cv2.imshow('bla', img)
cv2.waitKey(0)
