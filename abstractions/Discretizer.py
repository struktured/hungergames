'''
Created on Jul 22, 2013

@author: carm
'''
from util.math import range_index

DEFAULT_WEIGHTS = [0.0, .1, 0.2, .3, 0.4, .6, 0.8, 0.95]

class TileDiscretizer :
    
    def __init__(self, my_rep_weights=DEFAULT_WEIGHTS, their_rep_weights=DEFAULT_WEIGHTS, m_bonus_weights=DEFAULT_WEIGHTS) :
        self.my_rep_weights = my_rep_weights
        self.their_rep_weights = their_rep_weights
        self.m_bonus_weights = m_bonus_weights
    def hashMBonus(self, m, p) :    
        
        # Normalize m between 0 and 1, noting that 0 < m < P*(P-1)
        i = float((m-1)) / (p*(p-1) - 1)
        return range_index(self.m_bonus_weights, i)
            
    def hashMyReputation(self, rep) :
        return range_index(self.my_rep_weights, rep)
                           
    def hashTheirReputation(self, rep) :
        return range_index(self.their_rep_weights, rep)

    def state(self, m, p, my_rep, their_rep):
        return (self.hashMBonus(m, p), self.hashMyReputation(my_rep), 
                     self.hashTheirReputation(their_rep))

class IdentityDiscretizer :
    
    def __init__(self) :
        pass
    def hashMBonus(self, m, p) :    
        i = float((m-1)) / (p*(p-1) - 1)    
        return i
    def hashMyReputation(self, rep) :
        return rep                        
    def hashTheirReputation(self, rep) :
        return rep
        
    def state(self, m, p, my_rep, their_rep):
        return (self.hashMBonus(m, p), self.hashMyReputation(my_rep), 
                     self.hashTheirReputation(their_rep))

    