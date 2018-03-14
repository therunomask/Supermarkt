import cv2
import numpy as np
from scipy.stats import binom
import copy
import itertools
import matplotlib.pyplot as plt


#erstelle Vektor mit farbverteilungen nach binomialverteilung mit kleinem p
#
#rechne skalarprodukte mit den produkten in der produktliste aus
#
#aendere p, stelle fest, ab welcher breite es mehr als einen uebergang
#
#von einem produkt zum naechsten gibt. ueberang zwischen produkten ist
#
#dann gegeben und wechsel zwischen den produkten der letztgroesseren gaussglocke
#

def BinomialVec(n,p):
    prevector=[binom.pmf(k,n,p) for k in range(n) ]
    return np.array(prevector)


def MostLikelyPlace(VectorToLocate):
    overlap=[ for k in range(n)]
