'''
Created on Jul 22, 2013

@author: carm
'''
from math import log
from util.math import range_index

class Discretizer :
    def hashMBonus(self, m) :
        return int(round(log(m, 2)))
                   
    def hashMyReputation(self, rep) :
        return range_index([0.0, 0.2, 0.4, 0.8, 0.95], rep)
                           
    def hashTheirReputation(self, rep) :
        return range_index([0.0, 0.2, 0.4, 0.8, 0.95], rep)