import cv2
import numpy as np
import copy
import itertools
import matplotlib.pyplot as plt


img = cv2.imread('WhatsApp Image 2017-09-16 at 14.46.20(1).jpeg')
cap = cv2.VideoCapture('20171026_213832.mp4')
cap.set(1, 1000)
while True:
    _, frame = cap.read()
    #cv2.imshow('img', frame)
    # cv2.waitKey(100)
    img = frame
    rows, cols, ch = img.shape
    pts2 = np.float32([[0, 0], [300, 0], [0, 720], [300, 720]])
    M = cv2.getPerspectiveTransform(np.float32(
        [[822., 108.], [896.,  -24.],  [946., 542.], [1066.,  444.]]), pts2)

    dst = cv2.warpPerspective(img, M, (300, 720))
    for i in range(50):
        for j in range(300):
            dst[i, j] = (255, 255, 255)
    av = np.sum(dst, axis=1)
    av = np.sum(av, axis=1)
    spagetti = False
    for num in range(240):
        if av[num] < 210000:
            spagetti = True
    oreo = False
    for num in range(240, 480):
        if av[num] < 210000:
            oreo = True
    waschmittel = False
    for num in range(480, 720):
        if av[num] < 210000:
            waschmittel = True
    if spagetti:
        plt.text(90, 25000, 'spagetti')
    if oreo:
        plt.text(330, 25000, 'oreo')
    if waschmittel:
        plt.text(570, 25000, 'waschmittel')
    plt.plot(list(range(len(av))), av, 'ro')
    plt.axvline(240)
    plt.axvline(480)
    plt.axis([0, 720, 0, 240000])
    plt.pause(0.01)
    plt.clf()
    cv2.imshow('img', np.concatenate((dst, img), axis=1))
    cv2.waitKey(10)


LineCopy = copy.deepcopy(img)

BlackWhite = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = np.asarray((BlackWhite > 245) * 255, dtype=np.uint8)

#ret,thresh = cv2.threshold(BlackWhite,200,255,0)
image, contours, hierarchy = cv2.findContours(thresh, 1, 2)
cv2.imshow('img', thresh)
cv2.waitKey(1000)

contours.sort(key=len, reverse=True)
for con in contours[:1]:
    ImgTemp = np.zeros([rows, cols], dtype=np.uint8)
    for k in con:
        ImgTemp[k[0][1], k[0][0]] = np.array(255, dtype=np.uint8)
    cv2.imshow('img', ImgTemp)
    cv2.waitKey(1000)

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


coners = corner(geraden[3][0], geraden[3][1],
                geraden[1][0], geraden[1][1])


rows, cols, ch = img.shape

pts1 = np.float32(get_right_corners(get_all_corners(geraden)))
pts2 = np.float32([[0, 0], [300, 0], [0, 800], [300, 800]])

M = cv2.getPerspectiveTransform(np.float32(
    [[822., 108.], [896.,  1.],  [946., 542.], [1066.,  444.]]), pts2)


for cone in np.float32([[822., 108.], [896.,  1.], [1066.,  444.], [946., 542.]]):
    cv2.circle(LineCopy, (cone[0], cone[1]), 5, (255, 0, 0))

cv2.imshow('houghlines3.jpeg', LineCopy)

cv2.waitKey(5000)

cv2.imshow('bla', img)
cv2.waitKey(1000)
