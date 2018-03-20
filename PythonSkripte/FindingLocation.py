import numpy as np
from scipy.stats import binom
import Supermarkt.PythonSkripte.FixingLocation


def BinomialVec(n, p):
    prevector = [binom.pmf(k, n, p) for k in range(n)]
    return np.array(prevector)


def ProbabilityDensity(VectorToLocate):
    PartialSum = np.sum(VectorToLocate.Region, axis=0)
    n = np.shape(VectorToLocate)[0]
    overlap = [np.dot(PartialSum, BinomialVec(n, k / n)) for k in range(n)]
    return np.array(overlap)


def BestPositions(PileOfStuff):
    Probabilities = np.array([ProbabilityDensity(goods)
                              for goods in PileOfStuff.ListOfProducts])
    Positions = np.argmax(Probabilities, axis=0)
#    Changes=[]
    FoundProducts = []
    for k in range(Positions[:-1]):
        if Positions[k + 1] != Positions[k]:
         #          Changes.append(k)
            FoundProducts.append(Positions[k])

    if len(FoundProducts) != len(PileOfStuff.ListOfProducts):
        raise Exception("positions of products is not unique!")

    FoundProducts.append(Positions[-1])  # this too
    return FoundProducts

    # todo: use this information in RegionsOfStuff in order to save where each product ends
    # for simplest setup we need to revert the order of objects. (i.e. Product 0 is the
    # one which is rightmost in the brightness vector)
