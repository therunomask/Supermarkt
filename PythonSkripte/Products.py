import numpy as np
from FindingLocation import BestPositions


class Products:
    Productname = ""
    Region = np.zeros(1000)
    LocationOnDisplay = []
    Number = 1
    product_weigth = 0

    def __init__(self, name, brigthness_history, jump_list):
        oldvector = brigthness_history[0]
        Region = brigthness_history[0] - \
            brigthness_history[0]  # copy dimenions
        Norm = 0 * np.sum(oldvector, axis=0)
        for k in brigthness_history:
            Region += (oldvector - k)**2
            Norm += np.sum((oldvector - k)**2, axis=0)
            oldvector = k
        Norm = np.transpose(np.reshape(np.repeat(Norm, 1000), (3, 1000)))
 #       print(np.shape(Norm), np.shape(Region))
#        print(Norm)
        Region = Region / Norm
        self.Region = np.sqrt(Region)
        self.name = name
        self.Number = self.product_number(jump_list)

    def SetLocationOnDisplay(self, Loc):
        LocationOnDisplay = Loc

    def overlap(self, ProductPlacement):
        return np.vdot(self.Region, ProductPlacement) / 3

    def product_number(self, jumplist):
        av_weigth = [jumplist[0]]
        for jump in jumplist[1:]:
            av_weigth += [jump / int(jump / np.mean(av_weigth) + 0.5)
                          for _ in range(int(jump / np.mean(av_weigth) + 0.5))]
        return len(av_weigth), np.mean(av_weigth)


class Product_list:
    ListOfProducts = []
    NumberOfProducts = len(ListOfProducts)
    Memory = np.zeros(1000)
    LastVector = np.zeros(1000)
    GeometricParamter = 0.95  # magic number for series

    def __init__(self,  all_brigthness_histories, ListOfNumbers, Geomter=0.95):
        self.NumberOfProducts = len(all_brigthness_histories)
        ListOfProducts = []
        for N in range(self.NumberOfProducts):
            ListOfProducts.append(Products(
                "{}".format(N), all_brigthness_histories[N], ListOfNumbers[N]))

        self.ListOfProducts = ListOfProducts
        self.Memory = all_brigthness_histories[0][0] - all_brigthness_histories[0][0]
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
        probabilities = []
        for Product in self.ListOfProducts:
            prob = Product.overlap(self.Memory)
            probabilities.append(prob)
            if prob > MaxProbability:  # Problem appears if several products have the same
                MaxProbability = prob  # overlap
                GoodsName = Product.Productname

        return [np.array(probabilities), GoodsName]

    def update(self, VectorToMemorize):
        self.Memory *= self.GeometricParamter
        self.Memory += (VectorToMemorize - self.LastVector)
        self.LastVector = VectorToMemorize

    def Recall(self):
        return self.WhichProduct(self.Memory)

    def ChangeNumber(self, Number, jump_size):
        self.ListOfProducts[Number].Number += int(
            jump_size / self.ListOfProducts[Number].product_weigth + 0.5)
        if self.ListOfProducts[Number].Number < 0:
            raise Exception("negative number of items on the shelf!")