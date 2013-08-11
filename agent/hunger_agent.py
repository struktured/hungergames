'''
Created on Jul 22, 2013

@author: carm
'''
from Player import BasePlayer
from abstractions.Discretizer import TileDiscretizer
from numpy.ma.core import mod
from policies import GreedyPolicy


ACTIONS = ['s', 'h']
class BanditHungerAgent(BasePlayer) :
    def __init__(self, policy = GreedyPolicy(), discretizer = TileDiscretizer()) :
        self.policy = policy
        self.discretizer = discretizer        
        self.lastStates = None
        self.lastActions = None
        self.lastRewards = None
        self.name = "BanditHungerAgent(" + str(policy) + ")"
        self.my_rep = float(0)
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):      
        self.my_rep = current_reputation
        self.lastActions = list()
        self.lastStates = list()        
        self.lastRewards = None
        for their_rep in player_reputations :
            state = self.discretizer.state(m, len(player_reputations)+1, current_reputation, their_rep)          
            self.lastStates.append(state)
            self.lastActions.append(self.policy.act(state, ACTIONS))
        return self.lastActions
        
    def hunt_outcomes(self, food_earnings):
        self.lastRewards = list(food_earnings)
        
    def round_end(self, award, m, number_hunters): 
        P = len(self.lastRewards)
        for i in range(len(self.lastStates)) :
            #*(self.lastRewards[i] + award/(2*len(self.lastRewards)+1))
            #self.policy.reward(self.lastStates[i], self.lastActions[i], pow(.5, award/(2*(P+1)) + self.lastRewards[i]))
            self.policy.reward(self.lastStates[i], self.lastActions[i], award/(P+1) + self.lastRewards[i])

class HungerAgent2(BasePlayer) :
    def __init__(self, policy = GreedyPolicy(), discretizer = TileDiscretizer()) :
        self.policy = policy
        self.discretizer = discretizer        
        self.lastState = None
        self.lastAction = None
        self.lastReward = None
        self.name = "HungerAgent2(" + str(policy) + ")"
        self.my_rep = float(0)
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):      
        self.my_rep = current_reputation
        self.lastAction = list()
        self.lastState = None 
        self.lastReward = None
        self.lastState = list()
        for their_rep in player_reputations :
            state = self.discretizer.state(m, len(player_reputations)+1, current_reputation, their_rep)          
            self.lastState.append(state)
        
        num_actions = pow(len(ACTIONS), len(player_reputations))
        
        actions = list()
        for i in range(num_actions) :
            actions.append(i)
        
        self.lastState = tuple(self.lastState)
        self.lastAction = tuple(actions)
        chosen_action = self.policy.act(self.lastState, self.lastAction)
        
        cnt = num_actions
        ret_actions = list()
        while cnt > 0 :
            rem = chosen_action % len(ACTIONS)
            ret_actions.append(ACTIONS[rem])
            chosen_action /= 2
            cnt -= 1
            
        return ret_actions
        
    def hunt_outcomes(self, food_earnings):
        self.lastReward = sum(food_earnings)
        
    def round_end(self, award, m, number_hunters): 
        P = len(self.lastAction)
            #*(self.lastRewards[i] + award/(2*len(self.lastRewards)+1))
            #self.policy.reward(self.lastStates[i], self.lastActions[i], pow(.5, award/(2*(P+1)) + self.lastRewards[i]))
        self.policy.reward(self.lastState, self.lastAction, award/(P+1) + self.lastReward)
