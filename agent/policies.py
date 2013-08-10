'''
Created on Jul 22, 2013

@author: carm
'''
from util.math import weighted_choice
from random import randint
from sys import maxint
from math import log, sqrt, e
from abstractions.Metrics import WeightedEuclideanDistanceMetric
import random

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


class StateCache  :
    rewards = {}
    counts = {}
    
    def reward(self, state, action):
        return self.rewards[(state, action)] if (state,action) in self.rewards else 0
    def count(self, state, action):
        return self.counts[(state, action)] if (state,action) in self.counts else 0    
    def update(self, state, action, reward, fn = update_cache) :
        fn(key=(state,action),counts=self.counts,rewards=self.rewards, reward=reward)
    def __str__(self):
        return "discrete"
    
class NonParametricStateCache  :
    rewards = {}
    counts = {}
    t = 0
    def __init__(self, weights=WeightedEuclideanDistanceMetric(), min_size=100, max_size=50000):
        self.weights = weights        
        self.min_size = min_size
        self.max_size = max_size
        
    def reward(self, state, action):        
        avg = 0.0
        total = 0.0
        for (s,a), r in self.rewards.iteritems() :
            if action != a :
                continue
            w = self.weights.weight(state, s)
            avg += w*r
            total += w
        return 0 if total == 0 else avg / total;
    
    def count(self, state, action):
        total = 0.0
        for (s,a), _ in self.rewards.iteritems() :
            if action != a :
                continue
            w = self.counts[(s,a)]*self.weights.weight(state, s)
            total += w
        return total
        
    def update(self, state, action, reward, fn = update_cache) :
        fn(key=(state,action),counts=self.counts,rewards=self.rewards, reward=reward)
        ## Hack to pop old arbitrary items
        self.t += 1
        log_orig_len = self.t;
        while len(self.counts) >= min(self.max_size, max(self.min_size, log_orig_len)) :
            (s,a), _ = self.counts.popitem()
            self.rewards.pop((s,a))
    def __str__(self):
        return "nonpara"
            
class Policy :    
    
    stateCache = StateCache()
    
    def __init__(self, stateCache = StateCache()):
        self.stateCache = stateCache
        pass    
    def act(self, state, actions) :
        return None
    def reward(self, state, action, reward):
        pass
    def argmax(self, state, actions, bias=None) :
        if bias == None : bias = [0]*len(actions)
        (bestAction, bestReward) = actions[0], -maxint
        for i in range(len(actions)) :
            a = actions[i]
            reward = self.stateCache.reward(state, a) + bias[i]
            (bestAction, bestReward) = (a, reward) if (reward > bestReward) else (bestAction, bestReward)            
        return bestAction

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
    
class GreedyPolicy(Policy) :
    
    def __init__(self, eps=.75, stateCache = StateCache()) :
        self.eps = float(eps)
        self.stateCache = stateCache
    
    def act(self, state, actions) :        
        choice = weighted_choice([1.0-self.eps, self.eps])
        if choice == 0 : return actions[randint(0, len(actions)-1)]
        return self.argmax(state, actions)
    def __str__(self):
        return "GreedyPolicy(" + str(self.eps) + ", cache="  + str(self.stateCache) + ")"
                    
    def reward(self, state, action, reward) :
        self.stateCache.update(state, action, reward)

class UCBPolicy(Policy) :
    
    def __init__(self, B=2, eps = 1, stateCache=StateCache()) :
        self.B = float(B)
        self.eps = float(eps)
        self.stateCache = stateCache
    def bias(self, total, state, action) :
        denom = self.stateCache.count(state, action)
        return self.B if denom == 0 else self.B*sqrt(self.eps*log(total, e) / self.stateCache.count(state, action))
    def act(self, state, actions) :
        for a in actions :            
            if self.stateCache.count(state,a) < 1 :
                return a
        total = sum([self.stateCache.count(state,a) for a in actions])
        biases = [self.bias(total, state, a) for a in actions]
        return self.argmax(state, actions, biases)  
    def __str__(self):
        return "UCBPolicy(" + str(self.B) + "," + str(self.eps) + ", cache="  + str(self.stateCache) +  ")"           
    def reward(self, state, action, reward) :
        self.stateCache.update(state, action, reward)


class DUCBPolicy(Policy) :
     
    def __init__(self, B=4, eps = .5, discount=.9, stateCache = StateCache()) :
        self.stateCache = stateCache
        self.B = B
        self.eps = eps
        self.discount = discount
    def bias(self, total, state, action) :
        denom = self.stateCache.count(state, action)
        return self.B if denom == 0 or total < 1 else self.B*sqrt(self.eps*log(total, e) / denom)        
    def act(self, state, actions) :
        for a in actions :
            if self.stateCache.count(state, a) == 0 :
                return a
        total = sum([self.stateCache.count(state,a) for a in actions])
        biases = [self.bias(total, state, a) for a in actions]
        return self.argmax(state, actions, biases)  
    def __str__(self):
        return "DUCBPolicy(" + str(self.B) + "," + str(self.eps) + ")"           
    def reward(self, state, action, reward) :        
        update_discounted_cache((state,action), self.stateCache.counts, self.stateCache.rewards, reward, self.discount)

        
class MetaPolicy(Policy) :
    'Multi policy oriented Meta Policy'
    def __init__(self, meta_policy=DUCBPolicy(.05),  
                 policies=[GreedyPolicy(.85), RandomPolicy(.999), DUCBPolicy(.05), UCBPolicy()]) :
        self.meta_policy = meta_policy
        self.policies = policies
    def act(self, state, actions) :    
        self.last_p = self.meta_policy.act(state, self.policies)        
        #print 'meta_policy: chose policy ' + str(self.last_p)
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