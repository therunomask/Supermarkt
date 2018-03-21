import cv2
import numpy as np
import copy
from Supermarkt.PythonSkripte.visualisation import drawArea
from Supermarkt.PythonSkripte.get_corners import get_corners
from Supermarkt.PythonSkripte.Products import Product_list
from Supermarkt.PythonSkripte.get_shelf_av import get_shelf_av
from Supermarkt.PythonSkripte.scale_gauss_model import GaussModels
from Supermarkt.PythonSkripte.scale_jumps import scale

cap = cv2.VideoCapture('20171026_213832.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 500)
#cap = cv2.VideoCapture(0)
print('corners')
cornerlist = [[[0, 0], [0, 0], [0, 0], [0, 0]]]
while(True):
    _, frame = cap.read()
    # frame=mingziframe
    cornerlist.append(get_corners(frame, 245, cornerlist[-1]))
    print(cornerlist[-1])
    frame = drawArea(frame, cornerlist[-1], 0, 1, 0, 0.3)
    cv2.imshow('frame', frame)
    print(cornerlist[-1])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
corners = np.mean(cornerlist[-1:-10:-1], axis=0)
items = 0
allframes = []
allproducts = []
alljumps = []
jumps_per_product = []
scale1 = scale()
while(True):
    scale1.update()
    _, frame = cap.read()
    allframes.append(get_shelf_av(frame, corners, 1000, 200))
    # frame=mingziframe
    cv2.imshow('frame', frame)
    if scale1.detect_jump == True:
        jumps_per_product.append(np.absolute(scale1.jump_size()))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        items += 1
        allproducts.append(copy.deepcopy(allframes))
        allframes = []
        alljumps.append(copy.deepcopy(jumps_per_product))
        jumps_per_product = []
    if items == 2:
        break
regions = Product_list(allproducts, alljumps)
weight_prob = GaussModels(alljumps)
while(True):
    _, frame = cap.read()
    scale1.update()
    regions.update(get_shelf_av(frame, corners, 1000, 200))
    if scale1.detect_jump == True:
        probabilities = weight_prob.classifier(np.absolute(
            scale1.jump_size())) * regions.WhichProduct()[0]
        N = np.argmax(probabilities)
        regions.ChangeNumber(N, scale1.jump_size())
    for num, stuff in enumerate(regions):
        frame = drawArea(
            frame, corners, stuff.LocationOnDisplay[0], stuff.LocationOnDisplay[1], num % 3, 0.3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print('corners')
