import numpy as np


class RegionOfProduct:
    Productname = ""
    Region = np.zeros(1000)

    def __init__(self, name, ListOfVectors):
        oldvector = ListOfVectors[0]
        Region = ListOfVectors[0] - ListOfVectors[0]  # copy dimenions
        Norm = 0 * np.sum(oldvector, axis=0)
        for k in ListOfVectors:
            Region += (oldvector - k)**2
            Norm += np.sum((oldvector - k)**2, axis=0)
            oldvector = k
        Norm = np.transpose(np.reshape(np.repeat(Norm, 1000), (3, 1000)))
        print(np.shape(Norm), np.shape(Region))
        print(Norm)
        Region = Region / Norm
        self.Region = np.sqrt(Region)
        self.name = name

    def overlap(self, ProductPlacement):
        return np.vdot(self.Region, ProductPlacement) / 3
        # overlap=0
        # for k in self.Region*ProductPlacement:
#            s in k:
#                overlap+=s
#        return overlap


class RegionsOfStuff:
    ListOfProducts = []
    NumberOfProducts = len(ListOfProducts)
    Memory = np.zeros(1000)
    LastVector = np.zeros(1000)
    GeometricParamter = 0.95  # magic number for series

    def __init__(self,  ListOfListOfVector, Geomter=0.95):
        self.NumberOfProducts = len(ListOfListOfVector)
        ListOfProducts = []
        for N in range(self.NumberOfProducts):
            ListOfProducts.append(RegionOfProduct(
                "{}".format(N), ListOfListOfVector[N]))

        self.ListOfProducts = ListOfProducts
        self.Memory = ListOfListOfVector[0][0] - ListOfListOfVector[0][0]
        self.LastVector = self.Memory
        self.GeometricParamter = Geomter

    def WhichProduct(self, SeriesOfVectors):  # timing is given by scale
                    # could be an issue that we only use geometric series here
        MaxProbability = 0
        GoodsName = ""
        for Product in self.ListOfProducts:
            prob = Product.overlap(SeriesOfVectors)
            if prob > MaxProbability:  # Problem appears if several products have the same
                MaxProbability = prob  # overlap
                GoodsName = Product.Productname

        return GoodsName

    def update(self, VectorToMemorize):
        self.Memory *= self.GeometricParamter
        self.Memory += (VectorToMemorize - self.LastVector)
        self.LastVector = VectorToMemorize

    def Recall(self):
        return self.WhichProduct(self.Memory)
