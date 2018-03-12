import cv2
import numpy as np
import copy
import itertools
import matplotlib.pyplot as plt

class RegionOfProduct:
    Productname=""
    Region=np.zeros(1000)

    def __init__(self,name,ListOfVectors):
        oldvector=ListOfVectors[0]
        Region=ListOfVectors[0]-ListOfVectors[0]#copy dimenions
        Norm =0
        for k in ListOfVectors:
            Region+= (oldvector-k)**2
            for l in (oldvector-k)**2:
                Norm+=l
            oldvector=k
        Region/=Norm
        self.Region.Region
        self.name=name

    def overlap(self,ProductPlacement):
        overlap=0
        for k in oldvector*ProductPlacement:
            overlap+=k

        return overlap

class RegionsOfStuff:
    ListOfProducts=[]
    NumberOfProducts=ListOfProducts.len()
    Memory=np.zeros(1000)
    GeometricParamter=0.95      #magic number for series

    def __init__(self, NumberOfProducts,ListOfListOfVectors,Geomter=0.95):
        ListOfProducts=[]
        for N in range(NumberOfProducts):
            ListOfProducts.append(RegionOfStuff("{}".format(N),ListOfListOfVector[N]))

        self.ListOfProducts=ListOfProducts
        self.NumberOfProducts=N
        self.Memory=ListOfListOfVector[0][0]-ListOfListOfVector[0][0]
        self.GeometricParamter=Geomter

    def WhichProduct(SeriesOfVectors)# timing is given by scale
                    # could be an issue that we only use geometric series here
        MaxProbability=0
        GoodsName=""
        for Product in self.ListOfProducts:
            prob=Product.overlap(SeriesOfVectors)
            if prob>MaxProbability:  #Problem appears if several products have the same 
                MaxProbability=prob     #overlap
                GoodsName=Product.Productname

        return GoodsName

    def update(VectorToMemorize):
        self.Memory*=self.GeometricParamter
        self.Memory+=VectorToMemorize

    def Recall():
        return WhichProduct(self.Memory)
    

















    
