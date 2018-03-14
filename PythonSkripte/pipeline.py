import cv2
import numpy as np
import copy
from Supermarkt.PythonSkripte.get_corners import get_corners
from Supermarkt.PythonSkripte.FixingLocation import RegionOfProduct, RegionsOfStuff
from Supermarkt.PythonSkripte.get_shelf_av import get_shelf_av


cap = cv2.VideoCapture('20171026_213832.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 500)
print('corners')
while(True):
    _, frame = cap.read()
    corners = get_corners(frame, 245)
    # frame=mingziframe
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
    # frame=mingziframe
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print('corners')
