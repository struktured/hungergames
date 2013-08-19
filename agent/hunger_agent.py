'''
Created on Jul 22, 2013

@author: carm
'''
from Player import BasePlayer
from abstractions.Discretizer import TileDiscretizer, IdentityDiscretizer
from numpy.ma.core import mod
from policies import GreedyPolicy


ACTIONS = ['s', 'h']
class BanditAgent(BasePlayer) :
    def __init__(self, policy = GreedyPolicy(), discretizer = TileDiscretizer(), slack_threshold=2) :
        self.policy = policy
        self.discretizer = discretizer        
        self.lastStates = None
        self.lastActions = None
        self.worker_rewards = None
        self.name = "BanditAgent(" + str(policy) + ")"
        self.my_rep = float(0)
        self.slack_threshold = slack_threshold
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):      
        P = len(player_reputations) + 1
        if self.slack_threshold >= P :
            return ['s' for _ in range(P)]
        self.my_rep = current_reputation
        self.lastActions = list()
        self.lastStates = list()        
        self.worker_rewards = None
        for their_rep in player_reputations :
            state = self.discretizer.state(m, len(player_reputations)+1, current_reputation, their_rep)          
            self.lastStates.append(state)
            self.lastActions.append(self.policy.act(state, ACTIONS))
        return self.lastActions
        
    def hunt_outcomes(self, food_earnings):
        self.worker_rewards = list(food_earnings)
        
    def round_end(self, award, m, number_hunters): 
        P = len(self.worker_rewards)
        if self.slack_threshold >= P :
            return
        for i in range(len(self.lastStates)) :
            #*(self.worker_rewards[i] + award/(2*len(self.worker_rewards)+1))
            #self.policy.reward(self.lastStates[i], self.lastActions[i], pow(.5, award/(2*(P+1)) + self.worker_rewards[i]))
            self.policy.reward(self.lastStates[i], self.lastActions[i], award/(P+1) + self.worker_rewards[i])

class ManagerAgent(BasePlayer) :
    def __init__(self, policy = GreedyPolicy(eps=.25), discretizer = IdentityDiscretizer(), worker_policy = GreedyPolicy(.85)) :
        self.policy = policy
        self.discretizer = discretizer        
        self.lastStates = None
        self.lastActions = None
        self.worker_rewards = None
        self.name = "ManagerAgent(" + str(policy) + ")"
        self.my_rep = float(0)        
        self.worker_policy = worker_policy
        self.worker_states = list()        
        self.worker_actions = list()        
        self.avg_opp_rep = 0
        self.current_food = 0
        self.old_food = 0
        self.count = 0
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):      
        self.my_rep = current_reputation
        P = len(player_reputations) + 1
        self.current_food = current_food
        if self.old_food == 0 :
            self.old_food = self.current_food
            
        self.avg_opp_rep = sum(player_reputations) / (P-1)
        
        state = self.discretizer.state(m, len(player_reputations)+1, current_reputation, self.avg_opp_rep)                  
        action = (self.policy.act(state, [i for i in range(P)]))
        
        self.lastState = state
        self.lastAction = action
        
        slacks_avail = action
        
        self.worker_states = list()        
        self.worker_actions = list()
        for i in range(len(player_reputations)) :
            worker_policy = self.worker_policy #//self.worker_policies[i]
            player_reputation = player_reputations[i]            
            worker_state = self.discretizer.state(m, len(player_reputations)+1, current_reputation, player_reputation)
            worker_action = worker_policy.act(worker_state, ACTIONS if slacks_avail > 0 else ['h'])
            self.worker_states.append(worker_state)
            self.worker_actions.append(worker_action)
            slacks_avail -= 1 if worker_action == 's' else 0              
        return self.worker_actions
        
    def hunt_outcomes(self, food_earnings):
        self.worker_rewards = list(food_earnings)
        
    def round_end(self, award, m, number_hunters): 
        for i in range(len(self.worker_states)) :
            self.worker_policy.reward(self.worker_states[i], self.worker_actions[i], self.worker_rewards[i] + award/len(self.worker_states))
        #self.policy.reward(self.lastState, self.lastAction, sum(self.worker_rewards)/len(self.worker_rewards) + award/len(self.worker_states))                
        self.policy.reward(self.lastState, self.lastAction, self.current_food - self.old_food)
        self.old_food = self.current_food
        
