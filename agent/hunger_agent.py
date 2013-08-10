'''
Created on Jul 22, 2013

@author: carm
'''
from Player import BasePlayer
from abstractions.Discretizer import TileDiscretizer
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

