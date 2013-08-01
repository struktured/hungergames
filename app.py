from __future__ import division, print_function
from Game import Game
from Player import Player
from abstractions.Discretizer import TileDiscretizer, IdentityDiscretizer
from agent.hunger_agent import HungerAgent
from agent.policies import UCBPolicy, GreedyPolicy, DUCBPolicy, MetaPolicy,\
    RandomPolicy, NonParametricStateCache
from bots import *
from random import random

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':

#    players = [Freeloader(), Pushover(), HungerAgent(), Random([.5,.5]), Random([.5,.5]), 
 #              Random([.1,.9]), Random([.2,.8]), Pushover(), Freeloader(), Freeloader(), 
  #             Freeloader(), Random([.6,.4]), Freeloader(), Alternator(), Alternator(), Alternator(), Alternator(), Alternator(), 
   #            Random([.5,.5]), Random([.8,.2])]
#    players = [HungerAgent(discretizer=IdentityDiscretizer(), policy=GreedyPolicy(stateCache=NonParametricStateCache(), eps=.90)), Freeloader(), Freeloader(), FairHunter(), FairHunter(), Pushover(), Random(.51), MaxRepHunter(), HungerAgent(MetaPolicy(meta_policy=UCBPolicy())), HungerAgent(MetaPolicy(meta_policy=GreedyPolicy(.90), policies=[RandomPolicy(.9),RandomPolicy(.1)])), 
  #                                                                             HungerAgent(MetaPolicy()),
   #                                                                             HungerAgent(MetaPolicy(meta_policy=GreedyPolicy(.85))), HungerAgent(MetaPolicy(meta_policy=UCBPolicy(B=1, eps=2))), 
    #                                                                                                          Freeloader(), FairHunter(), Random(.6), #Random(), MaxRepHunter(), FairHunter(), Pushover(),
               #Random(.8), Random(.6), Random(.5), 
 #              HungerAgent(policy= DUCBPolicy()), HungerAgent(policy = UCBPolicy(B=20, eps=1)), HungerAgent(policy = UCBPolicy())]
    

    #players = [#HungerAgent(policy=GreedyPolicy(.90)), FairHunter(), Freeloader(), Freeloader(), Random(.6), Random(.4), Random(.8),  
  #            HungerAgent(policy=GreedyPolicy(.40)), HungerAgent(policy=GreedyPolicy(.80)), HungerAgent(policy=MetaPolicy()), 
  #             Freeloader(), FairHunter(), HungerAgent(UCBPolicy()), HungerAgent(policy=MetaPolicy(meta_policy=GreedyPolicy(.90), 
   # policies=[DUCBPolicy(stateCache=NonParametricStateCache(), discount=.85), GreedyPolicy(.95), GreedyPolicy(.25), RandomPolicy(.999)])), HungerAgent(DUCBPolicy(discount=.8, eps=2)), 
               
    players=[HungerAgent(policy=UCBPolicy(B=2, eps=.00000000001)),  Freeloader()]

#    $players[Freeloader(), HungerAgent(policy=GreedyPolicy(stateCache=NonParametricStateCache(), eps=.98), discretizer=IdentityDiscretizer()), HungerAgent(policy=GreedyPolicy(.95))]
  # num_random = 100
   # for i in range(num_random):
    #    players.append(Random(random()))
        
   # players = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(.2), Random(.8
    #num_greedy = 10
    #for i in range(num_greedy):
     #   players.append(HungerAgent(policy=GreedyPolicy(.80 + (float(i)/ num_greedy/5))))

    game = Game(players, average_rounds=50000)
    game.play_game()
    