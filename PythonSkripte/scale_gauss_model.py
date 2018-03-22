import numpy as np
from scipy.stats import multivariate_normal


class GaussModels:
    number_of_objects = 0
    list_of_gaussians = []

    def __init__(self, ListOfListOfVectors):
        self.number_of_objects = len(ListOfListOfVectors)
        for k in range(len(ListOfListOfVectors)):
            mean = np.mean(ListOfListOfVectors[k], axis=0)
            print("the mean is {}".format(mean))
            #covariance_matrix = np.cov(np.array(ListOfListOfVectors[k]).T)
            covariance_matrix = 20
            print("the covariance matrix is {}".format(covariance_matrix))
            self.list_of_gaussians.append(
                multivariate_normal(mean, covariance_matrix))

    def classifier(self, weight_vector):
        Normalisation = np.sum([gaussian.pdf(weight_vector)
                                for gaussian in self.list_of_gaussians])

        probabilities = [gaussian.pdf(
            weight_vector) / Normalisation for gaussian in self.list_of_gaussians]

        return(probabilities)

#
#
# G=GaussModels([np.array([1,2]),np.array([1,1,9])])
#
#
# print(G.number_of_objects)
# print(G.classifier(4))
