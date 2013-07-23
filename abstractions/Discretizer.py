'''
Created on Jul 22, 2013

@author: carm
'''
from math import log
from util.math import range_index

DEFAULT_REP_WEIGHTS = [0.0, 0.2, 0.4, 0.8, 0.95]
class Discretizer :
    
    def __init__(self, my_rep_weights=DEFAULT_REP_WEIGHTS, their_rep_weights=DEFAULT_REP_WEIGHTS) :
        self.my_rep_weights = my_rep_weights
        self.their_rep_weights = their_rep_weights
    
    def hashMBonus(self, m) :
        b = int(round(log(m*2, 2)))
        return b
            
    def hashMyReputation(self, rep) :
        return range_index(self.my_rep_weights, rep)
                           
    def hashTheirReputation(self, rep) :
        return range_index(self.their_rep_weights, rep)