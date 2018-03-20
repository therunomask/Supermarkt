import cv2
import numpy as np
import copy
from Supermarkt.PythonSkripte.visualisation import drawArea
from Supermarkt.PythonSkripte.get_corners import get_corners
from Supermarkt.PythonSkripte.FixingLocation import RegionOfProduct, RegionsOfStuff
from Supermarkt.PythonSkripte.get_shelf_av import get_shelf_av


# cap = cv2.VideoCapture('20171026_213832.mp4')
# cap.set(cv2.CAP_PROP_POS_FRAMES, 500)
cap = cv2.VideoCapture('0')
print('corners')
while(True):
    _, frame = cap.read()
    # frame=mingziframe
    corners = get_corners(frame, 245)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame = drawArea(frame, corners, 0, 1, 0, 0.3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(corners)
print('corners')
items = 0
allframes = []
allproducts = []
while(True):
    _, frame = cap.read()
    allframes.append(get_shelf_av(frame, corners, 1000, 200))
    # frame=mingziframe
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        items += 1
        allproducts.append(copy.deepcopy(allframes))
        allframes = []
    if items == 2:
        break
regions = RegionsOfStuff(allproducts)
while(True):
    _, frame = cap.read()
    allframes.append(frame)
    for num, stuff in enumerate(regions):
        frame = drawArea(
            frame, corners, stuff.LocationOnDisplay[0], stuff.LocationOnDisplay[1], num % 3, 0.3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print('corners')
