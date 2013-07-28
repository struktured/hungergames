'''
Created on Jul 22, 2013

@author: carm
'''
from util.math import weighted_choice
from random import randint
from sys import maxint
from math import log, sqrt, e
from bots import FairHunter, Freeloader, Random

def update_cache(key, counts, rewards, reward, prior = lambda (k, c, e) : (0,0)):
        if key not in rewards :
            (c, r) = prior((key, counts, rewards))
            counts[key] = c
            rewards[key] = r
        counts[key] += 1
        rewards[key] += float((reward - rewards[key])) / counts[key]

def update_discounted_cache(key, counts, rewards, reward, discount=.9, prior = lambda (k, c, e) : (0,0)):
        if key not in rewards :
            (c, r) = prior((key, counts, rewards))
            counts[key] = c
            rewards[key] = r
        prev_count = counts[key]
        counts[key] = 1.0 + discount*prev_count
        rewards[key] = (1.0/counts[key])*(reward + discount * prev_count * rewards[key])

def update_distance_metric_cache(key, counts, rewards, reward, prior = lambda (k, c, e) : (0,0), d  = lambda(x,y)  : 0 if x == y else 1):
        if key not in rewards :
            (c, r) = prior((key, counts, rewards))
            counts[key] = c
            rewards[key] = r
        counts[key] += 1                
        rewards[key] += float((reward - rewards[key])) / counts[key]

class StateCache  :
    rewards = {}
    counts = {}
    
    def update(self, state, action, reward) :
        update_cache(key=(state,action),counts=self.counts,rewards=self.rewards, reward=reward)
            
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


class DUCBPolicy(Policy) :
     
    def __init__(self, B=2, eps = 20, discount=.9) :
        self.B = B
        self.eps = eps
        self.discount = discount
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
        return "DUCBPolicy(" + str(self.B) + "," + str(self.eps) + ")"           
    def reward(self, state, action, reward) :        
        update_discounted_cache((state,action), self.stateCache.counts, self.stateCache.rewards, reward, self.discount)

class SlidingWindowStateCache(StateCache):
    rewards = {}
    counts = {}
    
    def update(self, state, action, k, reward) :
        if (state, k, action) not in self.rewards :
            self.counts[(state,action)] = 0
            self.rewards[(state, action)] = 0        
        self.counts[(state,action)] += 1
        self.rewards[(state, action)] += float((reward - self.rewards[(state, action)])) / self.counts[(state,action)]
    
class SlidingWindowUCBPolicy(Policy) :
    
    def __init__(self, B=2, eps = 20) :
        self.B = B
        self.eps = eps
    def bias(self, total, state, action, k) :
        return self.B*sqrt(self.eps*log(min(total, k), e) / self.stateCache.counts[(state, action, k)])
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
        
            


class RandomPolicy(Policy) :
    'Fixed Random Distribution Policy'
    def __init__(self, dist=[.5, .5]) :  
        self.dist = [dist, 1 - dist] if isinstance(dist, float) or isinstance(dist, int) else dist
    def act(self, state, actions) :    
        return actions[weighted_choice(self.dist)]
    def __str__(self):
        return "RandomPolicy(dist=" + str(self.dist) + ")"
    def reward(self, state, action, reward) :        
        pass
        
class MetaPolicy(Policy) :
    'Multi policy oriented Meta Policy'
    def __init__(self, meta_policy=DUCBPolicy(discount=.5, eps=1), 
                 policies=[GreedyPolicy(.99), RandomPolicy(.95), RandomPolicy(.05), DUCBPolicy(), UCBPolicy()]) :
        self.meta_policy = meta_policy
        self.policies = policies
    def act(self, state, actions) :    
        self.last_p = self.meta_policy.act(state, self.policies)        
        return self.last_p.act(state, actions)
    def __str__(self):
        return "MetaPolicy(meta_p=" + str(self.meta_policy) + ",num_p=" + str(len(self.policies)) + ")"      
    def reward(self, state, action, reward) :        
        # Reward all policies to learn the right action off line.
        for p in self.policies : 
            p.reward(state, action, reward)        
        # Reward only the strategy the meta policy chose
        # Alternative: reward all strategies that would have selected the right policy?
        self.meta_policy.reward(state, self.last_p, reward)        