'''
Created on Aug 14, 2013

@author: carm
'''
from Player import BasePlayer
from abstractions.Discretizer import IdentityDiscretizer, \
    TheirRepTileDiscretizer, TileDiscretizer
from agent.hunger_agent import ACTIONS
from agent.policies import GreedyPolicy, UCBPolicy, DUCBPolicy, \
    NonParametricStateCache
    
REP_ACTIONS = [0, .2, .6, 1]

class ReputationAgent(BasePlayer) :
    def __init__(self, policy = UCBPolicy(), discretizer = TheirRepTileDiscretizer(), 
                 worker_policy = UCBPolicy(stateCache=NonParametricStateCache()), 
                 worker_discretizer = IdentityDiscretizer(),
                 reward_ind = lambda(x) : x % 10 == 0) :
        self.policy = policy
        self.discretizer = discretizer        
        self.lastStates = None
        self.lastActions = None
        self.worker_rewards = None
        self.name = "ReputationAgent(" + str(policy) + ")"
        self.my_rep = float(0)
        self.target_rep = 1.0
        self.worker_discretizer = worker_discretizer
        self.worker_policy = worker_policy
        self.worker_states = list()        
        self.worker_actions = list()        
        self.avg_opp_rep = 0
        self.current_food = 0
        self.old_food = 0
        self.count = 0
        self.reward_ind = reward_ind
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
        
        if self.count == 0 or self.reward_ind(self.count) :            
            state = self.discretizer.state(m, len(player_reputations)+1, current_reputation, self.avg_opp_rep)                  
            action = self.policy.act(state, REP_ACTIONS)
            self.lastState = state
            self.lastAction = action
        
        slacks_avail = min(P-1, self.lastAction*(P-1))
        
        self.worker_states = list()        
        self.worker_actions = list()
        for i in range(len(player_reputations)) :
            worker_policy = self.worker_policy #//self.worker_policies[i]
            player_reputation = player_reputations[i]            
            worker_state = self.worker_discretizer.state(m, len(player_reputations)+1, current_reputation, player_reputation)
            worker_action = worker_policy.act(worker_state, ACTIONS if slacks_avail > 0 else ['h'])
            self.worker_states.append(worker_state)
            self.worker_actions.append(worker_action)
            slacks_avail -= 1 if worker_action == 's' else 0              
        return self.worker_actions
        
    def hunt_outcomes(self, food_earnings):
        self.worker_rewards = list(food_earnings)
        
    def round_end(self, award, m, number_hunters):
        self.count += 1 
        for i in range(len(self.worker_states)) :
            self.worker_policy.reward(self.worker_states[i], self.worker_actions[i], self.worker_rewards[i] + award/len(self.worker_states))
        #self.policy.reward(self.lastState, self.lastAction, sum(self.worker_rewards)/len(self.worker_rewards) + award/len(self.worker_states))                
        if self.reward_ind(self.count) :
            self.policy.reward(self.lastState, self.lastAction, self.current_food - self.old_food)
            self.old_food = self.current_food