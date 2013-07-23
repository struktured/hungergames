'''
Created on Jul 22, 2013

@author: carm
'''
from util.math import weighted_choice
from random import randint
from sys import maxint

class StateCache  :
    rewards = {}
    counts = {}
    
    def update(self, state, action, reward) :
        if (state, action) not in self.rewards :
            self.counts[(state,action)] = 0
            self.rewards[(state, action)] = 0        
        self.counts[(state,action)] += 1
        self.rewards[(state, action)] += (reward - self.rewards[(state, action)]) / self.counts[(state,action)]
            
class Policy :    
    def act(self, state, actions) :
        return None
    def reward(self, state, action, reward):
        pass

    
class GreedyPolicy(Policy) :
    
    def __init__(self, eps=.99) :
        self.eps = eps
        self.stateCache = StateCache()
    
    def act(self, state, actions) :        
        choice = weighted_choice([1.0-self.eps, self.eps])
        if choice == 0 : return actions[randint(0, len(actions)-1)]
        
        (bestAction, bestReward) = actions[0], -maxint
        for a in actions :
            if (state, a) in self.stateCache.rewards :                 
                reward = self.stateCache.rewards[(state, a)]
                (bestAction, bestReward) = (a, reward) if (reward > bestReward) else (bestAction, bestReward)
            else : continue
        return bestAction                                        
                
    def reward(self, state, action, reward) :
        self.stateCache.update(state, action, reward)
