import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt


def BinomialVec(n, p):
    prevector = [binom.pmf(k, n, p) for k in range(n)]
    return np.array(prevector)


def ProbabilityDensity(product):
    PartialSum = np.sum(product.Region, axis=1)
    n = np.shape(product.Region)[0]
    overlap = [np.dot(PartialSum, BinomialVec(n, k / n)) for k in range(n)]
    return np.array(overlap)


def BestPositions(Product_list):
    Probabilities = np.array([ProbabilityDensity(product)
                              for product in Product_list.ListOfProducts])
    Positions = np.argmax(Probabilities, axis=0)
    print(Positions)
    for n in range(Product_list.NumberOfProducts):
        Product_list.ListOfProducts[n].SetLocationOnDisplay([next(num for num, i in enumerate(Positions) if i == n) / len(
            Positions), (len(Positions) - next(num for num, i in enumerate(reversed(Positions)) if i == n)) / len(Positions)])
        print(Product_list.ListOfProducts[n].LocationOnDisplay)
#    Changes=[]

    # todo: use this information in RegionsOfStuff in order to save where each product ends
    # for simplest setup we need to revert the order of objects. (i.e. Product 0 is the
    # one which is rightmost in the brightness vector)
