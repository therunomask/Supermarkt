import cv2
import numpy as np
import copy
import itertools
import matplotlib.pyplot as plt


#erstelle Vektor mit farbverteilungen nach gaussglocke mit großer breite
#
#rechne skalarprodukte mit den produkten in der produktliste aus
#
#aendere breite, stelle fest, ab welcher breite es mehr als einen uebergang
#
#von einem produkt zum naechsten gibt. ueberang zwischen produkten ist
#
#dann gegeben und wechsel zwischen den produkten der letztgroesseren gaussglocke
#
#
#
