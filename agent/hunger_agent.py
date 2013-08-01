'''
Created on Jul 22, 2013

@author: carm
'''
from Player import BasePlayer
from abstractions.Discretizer import TileDiscretizer
from policies import GreedyPolicy


ACTIONS = ['s', 'h']
class HungerAgent(BasePlayer) :
    def __init__(self, policy = GreedyPolicy(), discretizer = TileDiscretizer()) :
        self.policy = policy
        self.discretizer = discretizer        
        self.lastStates = None
        self.lastActions = None
        self.lastRewards = None
        self.name = "HungerAgent(" + str(policy) + ")"
      
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):      
        self.lastActions = list()
        self.lastStates = list()        
        self.lastRewards = None
        for their_rep in player_reputations :
            state = (self.discretizer.hashMBonus(m, len(player_reputations)+1), self.discretizer.hashMyReputation(current_reputation), 
                     self.discretizer.hashTheirReputation(their_rep))          
            self.lastStates.append(state)
            self.lastActions.append(self.policy.act(state, ACTIONS))
        return self.lastActions
        
    def hunt_outcomes(self, food_earnings):
        self.lastRewards = list(food_earnings)
        
    def round_end(self, award, m, number_hunters): 
        for i in range(len(self.lastStates)) :
            self.policy.reward(self.lastStates[i], self.lastActions[i], self.lastRewards[i] + award)   
        