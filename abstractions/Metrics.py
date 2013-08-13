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
    
    def __init__(self, weights=[1,1,1]):
        self.weights = weights;    
    def distance(self, x, y):
        
        numerator = 0
        for i in range(len(x)) :
            v_x = x[i]
            v_y = y[i]
            numerator += self.weights[i]*pow(v_x-v_y, 2)
                       
        return pow(numerator, .5)
        
    def weight(self, x, y):
        d = self.distance(x,y)
        return pow(e,-d)