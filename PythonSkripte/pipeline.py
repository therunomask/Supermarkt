import cv2
import numpy as np
import copy
import itertools
import matplotlib.pyplot as plt
from get_corners import get_corners
from FixingLocation import RegionOfProduct, RegionsOfStuff

cap = cv2.VideoCapture('20171026_213832.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 500)

while(True):
    _, frame = cap.read()
    corners = get_corners(frame, 245)
    # frame=mingziframe
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
items = 0
allframes = []
allproducts = []
while(True):
    _, frame = cap.read()
    allframes.append(frame)
    # frame=mingziframe
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        items += 1
        allproducts.append(copy.deepcopy(allframes))
        allframes = []
    if items == 6:
        break
regions = RegionsOfStuff(6, allframes)
while(True):
    _, frame = cap.read()
    allframes.append(frame)
    # frame=mingziframe
    cv2.imshow('frame', frame)


cap.release()
cv2.destroyAllWindows()
