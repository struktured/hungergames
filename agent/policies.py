'''
Created on Jul 22, 2013

@author: carm
'''
from util.math import weighted_choice
from random import randint
from sys import maxint
from math import log, sqrt, e
class StateCache  :
    rewards = {}
    counts = {}
    
    def update(self, state, action, reward) :
        if (state, action) not in self.rewards :
            self.counts[(state,action)] = 0
            self.rewards[(state, action)] = 0        
        self.counts[(state,action)] += 1
        self.rewards[(state, action)] += float((reward - self.rewards[(state, action)])) / self.counts[(state,action)]
            
class Policy :    
    stateCache = StateCache()
    
    def act(self, state, actions) :
        return None
    def reward(self, state, action, reward):
        pass
    def argmax(self, state, actions, bias=None) :
        if bias == None : bias = [0]*len(actions)
        (bestAction, bestReward) = actions[0], -maxint
        for i in range(len(actions)) :
            a = actions[i]
            if (state, a) in self.stateCache.rewards :          
                reward = self.stateCache.rewards[(state, a)] + bias[i]
                (bestAction, bestReward) = (a, reward) if (reward > bestReward) else (bestAction, bestReward)
            else : continue
        return bestAction                                        
    
class GreedyPolicy(Policy) :
    
    def __init__(self, eps=.75) :
        self.eps = eps
    
    def act(self, state, actions) :        
        choice = weighted_choice([1.0-self.eps, self.eps])
        if choice == 0 : return actions[randint(0, len(actions)-1)]
        return self.argmax(state, actions)
    def __str__(self):
        return "GreedyPolicy(" + str(self.eps) + ")"
                    
    def reward(self, state, action, reward) :
        self.stateCache.update(state, action, reward)

class UCBPolicy(Policy) :
    
    def __init__(self, B=2, eps = 20) :
        self.B = B
        self.eps = eps
        self.stateCache = StateCache()    
    def bias(self, total, state, action) :
        return self.B*sqrt(self.eps*log(total, e) / self.stateCache.counts[(state, action)])
    def act(self, state, actions) :
        for a in actions :
            if (state, a) not in self.stateCache.counts :
                return a
        total = sum([self.stateCache.counts[(state,a)] for a in actions])
        biases = [self.bias(total, state, a) for a in actions]
        return self.argmax(state, actions, biases)  
    def __str__(self):
        return "UCBPolicy(" + str(self.B) + "," + str(self.eps) + ")"           
    def reward(self, state, action, reward) :        
        self.stateCache.update(state, action, reward)
