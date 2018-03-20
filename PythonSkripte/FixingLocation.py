import numpy as np
from Supermarkt.PythonSkripte.FindingLocation import BestPositions


class RegionOfProduct:
    Productname = ""
    Region = np.zeros(1000)
    LocationOnDisplay=[]
    Number=1

    def __init__(self, name, ListOfVectors,M):
        oldvector = ListOfVectors[0]
        Region = ListOfVectors[0] - ListOfVectors[0]  # copy dimenions
        Norm = 0 * np.sum(oldvector, axis=0)
        for k in ListOfVectors:
            Region += (oldvector - k)**2
            Norm += np.sum((oldvector - k)**2, axis=0)
            oldvector = k
        Norm = np.transpose(np.reshape(np.repeat(Norm, 1000), (3, 1000)))
 #       print(np.shape(Norm), np.shape(Region))
#        print(Norm)
        Region = Region / Norm
        self.Region = np.sqrt(Region)
        self.name = name
        self.Number=M

    def SetLocationOnDisplay(self, Loc):
        LocationOnDisplay = Loc

    def overlap(self, ProductPlacement):
        return np.vdot(self.Region, ProductPlacement) / 3


class RegionsOfStuff:
    ListOfProducts = []
    NumberOfProducts = len(ListOfProducts)
    Memory = np.zeros(1000)
    LastVector = np.zeros(1000)
    GeometricParamter = 0.95  # magic number for series

    def __init__(self,  ListOfListOfVector, ListOfNumbers,Geomter=0.95):
        self.NumberOfProducts = len(ListOfListOfVector)
        ListOfProducts = []
        for N in range(self.NumberOfProducts):
            ListOfProducts.append(RegionOfProduct(
                "{}".format(N), ListOfListOfVector[N],ListOfNumbers[N]))

        self.ListOfProducts = ListOfProducts
        self.Memory = ListOfListOfVector[0][0] - ListOfListOfVector[0][0]
        self.LastVector = self.Memory
        self.GeometricParamter = Geomter

        transitions = BestPositions(self)

        beginning = 0
        for k in range(len(transitions)):
            end = transitions[len(transitions) - k]
            ListOfProducts[len(transitions) - k].SetLocationOnDisplay(
                [beginning / transitions[-1], end / transitions[-1]])
            beginning = end

    def WhichProduct(self):  # timing is given by scale
                    # could be an issue that we only use geometric series here
        MaxProbability = 0
        GoodsName = ""
        probabilities=[]
        for Product in self.ListOfProducts:
            prob = Product.overlap(self.Memory)
            probabilities.append(prob)
            if prob > MaxProbability:  # Problem appears if several products have the same
                MaxProbability = prob  # overlap
                GoodsName = Product.Productname

        return [np.array(probabilities),GoodsName]

    def update(self, VectorToMemorize):
        self.Memory *= self.GeometricParamter
        self.Memory += (VectorToMemorize - self.LastVector)
        self.LastVector = VectorToMemorize

    def Recall(self):
        return self.WhichProduct(self.Memory)
