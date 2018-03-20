import cv2
import numpy as np
import copy
from Supermarkt.PythonSkripte.visualisation import drawArea
from Supermarkt.PythonSkripte.get_corners import get_corners
from Supermarkt.PythonSkripte.FixingLocation import RegionOfProduct, RegionsOfStuff
from Supermarkt.PythonSkripte.get_shelf_av import get_shelf_av
from Supermarkt.PythonSkripte.scale_gauss_model.py import GaussModels

cap = cv2.VideoCapture('20171026_213832.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 500)
print('corners')
while(True):
    _, frame = cap.read()
    # frame=mingziframe
    corners = get_corners(frame, 245)
    frame = drawArea(frame, corners, 0, 1, 0, 0.3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(corners)
print('corners')
items = 0
allframes = []
allproducts = []
alljumps=[]
jumpts_per_product=[]
scale1 = scale()
while(True):
    scale1.update()
    _, frame = cap.read()
    allframes.append(get_shelf_av(frame, corners, 1000, 200))
    # frame=mingziframe
    cv2.imshow('frame', frame)
    if scale1.detect_jump==True:
        jumps_per_product.append(np.absolute(scale1.jump_size()))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        items += 1
        allproducts.append(copy.deepcopy(allframes))
        allframes = []
        alljumps.append(copy.deepcopy(jumps_per_product))
        jumps_per_product=[]
    if items == 2:
        break
regions = RegionsOfStuff(allproducts,[len(k) for k in alljumps])
weight_prob=GaussModels(alljumps)
while(True):
    _, frame = cap.read()
    scale1.update()
    regions.update(get_shelf_av(frame, corners, 1000, 200)))
    if scale1.detect_jump==True:
        itemtaken=(np.sign(scalle.jump_size())==-1.)
        probabilities=weight_prob.classifier(np.absolute(scale1.jump_size()))*regions.WhichProduct()[0]
        N=np.argmax(probabilities)
        region.ChangeNumber()
    for num, stuff in enumerate(regions):
        frame = drawArea(
            frame, corners, stuff.LocationOnDisplay[0], stuff.LocationOnDisplay[1], num % 3, 0.3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print('corners')
