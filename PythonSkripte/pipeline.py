import cv2
import numpy as np
import copy
""""from Supermarkt.PythonSkripte.visualisation import drawArea, draw_number
from Supermarkt.PythonSkripte.get_corners import get_corners
from Supermarkt.PythonSkripte.Products import Product_list
from Supermarkt.PythonSkripte.get_shelf_av import get_shelf_av
from Supermarkt.PythonSkripte.scale_gauss_model import GaussModels"""
from Supermarkt.PythonSkripte.scale_jumps import scale
from visualisation import drawArea, draw_number
from get_corners import get_corners
from Products import Product_list
from get_shelf_av import get_shelf_av
from scale_gauss_model import GaussModels
#from scale_jumps import scale
import time
import threading
from microphone import AudioRecording
from ReplaceAudio import replace_audio, shorten_audio
from frame_collection import cut_frames


thread_signal = False
endtimea = 0
starttimea = 0


def AudioLoop():
    """Thread needs a function to call 
    in this example the thread executing this
    function simply waits for the global variable
    to change value. Which is done by the other thread"""
    global thread_signal
    global endtimea
    global starttimea
    starttimea = time.time()
    print('audio begin:', starttimea)
    recording = AudioRecording()
    while thread_signal == False:
        recording.update()
        # time.sleep(3)
    endtimea = time.time()
    print('audio ende:', endtimea)
    recording.close()


t1 = threading.Thread(target=AudioLoop)


# Thread.start() forces the object to execute its target()
t1.start()


timestamps = []
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


frame_list = []
#cap = cv2.VideoCapture('20171026_213832.mp4')
#cap.set(cv2.CAP_PROP_POS_FRAMES, 500)
cap = cv2.VideoCapture(0)
print('corners')
cornerlist = [[[0, 0], [0, 0], [0, 0], [0, 0]]]
startv = time.time()
print('video begin:', startv)
while(True):
    _, frame = cap.read()
    # frame=mingziframe
    cornerlist.append(get_corners(frame, 245, cornerlist[-1]))
    # print(cornerlist[-1])
    frame = drawArea(frame, cornerlist[-1], 0, 1, 0, 0.3)
    cv2.imshow('frame', frame)
    # out.write(frame)
    frame_list.append(frame)
    timestamps.append(time.time())
    # print(cornerlist[-1])
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
    allframes.append(get_shelf_av(frame, corners, 200, 50))
    frame = drawArea(frame, corners, 0, 1, 0, 0.3)
    cv2.imshow('frame', frame)
    # out.write(frame)
    frame_list.append(frame)
    timestamps.append(time.time())
    if scale1.detect_jump() == True:
        print(scale1.jump_size())
        jumps_per_product.append(np.absolute(scale1.jump_size()))
    print(jumps_per_product)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        items += 1
        allproducts.append(copy.deepcopy(allframes))
        allframes = []
        alljumps.append(copy.deepcopy(jumps_per_product))
        jumps_per_product = []
    if items == 5:
        break
regions = Product_list(allproducts, alljumps)
weight_prob = GaussModels(
    [regions.ListOfProducts[0].massuered_weights(jump) for jump in alljumps])
while(True):
    _, frame = cap.read()
    scale1.update()
    regions.update(get_shelf_av(copy.deepcopy(frame), corners, 200, 50))
    if scale1.detect_jump() == True:
        jump = scale1.jump_size()
        probabilities = weight_prob.classifier(np.absolute(
            jump)) * regions.WhichProduct()[0]
        print(jump)
        N = np.argmax(probabilities)
        regions.ChangeNumber(N, jump)
    for num, stuff in enumerate(regions.ListOfProducts):
        frame = drawArea(
            frame, copy.deepcopy(corners), stuff.LocationOnDisplay[0], stuff.LocationOnDisplay[1], num, 0.7)
        frame = draw_number(
            frame, stuff.picture_position, num, stuff.Number)
    cv2.imshow('frame', frame)
    frame_list.append(frame)
    # out.write(frame)
    timestamps.append(time.time())
    if cv2.waitKey(1) & 0xFF == ord('w'):
        break

cap.release()
endv = time.time()
print('video ende:', endv)
frame_list = cut_frames(timestamps, frame_list)
for frame in frame_list:
    out.write(frame)
out.release()

cv2.destroyAllWindows()
print('corners')

# signal to audioloop to stop recording
thread_signal = True


# join() waits for the thread to finish
t1.join()
shorten_audio('audio', 'saudio', startv - starttimea, endv - starttimea)
replace_audio("output", "newvideo", 'saudio')
