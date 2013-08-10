'''
Created on Jul 28, 2013

@author: carm
'''
from numpy.core.numeric import infty

'''
Created on Jul 22, 2013

@author: carm
'''

from math import e

class WeightedEuclideanDistanceMetric :
    
    def __init__(self, weights=[1,1]):
        self.weights = weights;    
    def distance(self, x, y):
        (m, their_rep, my_rep) = x
        (m2, their_rep2, my_rep2) = y
        
        numerator = self.weights[0]*pow(their_rep - their_rep2, 2) + self.weights[1]*pow(m - m2, 2)
                       
        return pow(numerator, .5)
        
    def weight(self, x, y):
        d = self.distance(x,y)
        return pow(e,-d)