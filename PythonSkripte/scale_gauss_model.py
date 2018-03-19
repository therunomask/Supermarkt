import numpy as np
from scipy import multivariate_normal

def GaussModels
    number_of_objects
    list_of_gaussians

    def __init__(self, ListOfListOfVectors):
        self.number_of_objects=len(ListOfListOfVectors)
        for k in range(len(ListOfListOfVectors)):
            means=np.mean(ListOfListOfVectors[k],axis=0)
            covanriance_matrix=np.cov(np.array(ListOfVectors[k]).T)
            list_of_gaussians.append(multivariate_normal(mean,covariance_matrix))

    def classifier(weight_vector):
        Normalisation=np.sum([gaussian.pdf(weight_vector) for gaussian in self.list_of_gaussians])
        
        probabilities=[gaussian.pdf(obj)/Normalisation for gaussian in list_of_gaussians]

        return(probabilities)
