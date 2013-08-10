from __future__ import division, print_function
from Game import Game
from Player import Player
from abstractions.Discretizer import TileDiscretizer, IdentityDiscretizer
from agent.hunger_agent import BanditHungerAgent
from agent.policies import UCBPolicy, GreedyPolicy, DUCBPolicy, MetaPolicy, \
    RandomPolicy, NonParametricStateCache
from bots import *
from random import random

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':

#    players = [Freeloader(), Pushover(), BanditHungerAgent(), Random([.5,.5]), Random([.5,.5]), 
 #              Random([.1,.9]), Random([.2,.8]), Pushover(), Freeloader(), Freeloader(), 
  #             Freeloader(), Random([.6,.4]), Freeloader(), Alternator(), Alternator(), Alternator(), Alternator(), Alternator(), 
   #            Random([.5,.5]), Random([.8,.2])]
#    players = [BanditHungerAgent(discretizer=IdentityDiscretizer(), policy=GreedyPolicy(stateCache=NonParametricStateCache(), eps=.90)), Freeloader(), Freeloader(), FairHunter(), FairHunter(), Pushover(), Random(.51), MaxRepHunter(), BanditHungerAgent(MetaPolicy(meta_policy=UCBPolicy())), BanditHungerAgent(MetaPolicy(meta_policy=GreedyPolicy(.90), policies=[RandomPolicy(.9),RandomPolicy(.1)])), 
  #                                                                             BanditHungerAgent(MetaPolicy()),
   #                                                                             BanditHungerAgent(MetaPolicy(meta_policy=GreedyPolicy(.85))), BanditHungerAgent(MetaPolicy(meta_policy=UCBPolicy(B=1, eps=2))), 
    #                                                                                                          Freeloader(), FairHunter(), Random(.6), #Random(), MaxRepHunter(), FairHunter(), Pushover(),
               #Random(.8), Random(.6), Random(.5), 
 #              BanditHungerAgent(policy= DUCBPolicy()), BanditHungerAgent(policy = UCBPolicy(B=20, eps=1)), BanditHungerAgent(policy = UCBPolicy())]
    

    #players = [#BanditHungerAgent(policy=GreedyPolicy(.90)), FairHunter(), Freeloader(), Freeloader(), Random(.6), Random(.4), Random(.8),  
  #            BanditHungerAgent(policy=GreedyPolicy(.40)), BanditHungerAgent(policy=GreedyPolicy(.80)), BanditHungerAgent(policy=MetaPolicy()), 
  #             Freeloader(), FairHunter(), BanditHungerAgent(UCBPolicy()), BanditHungerAgent(policy=MetaPolicy(meta_policy=GreedyPolicy(.90), 
   # policies=[DUCBPolicy(stateCache=NonParametricStateCache(), discount=.85), GreedyPolicy(.95), GreedyPolicy(.25), RandomPolicy(.999)])), BanditHungerAgent(DUCBPolicy(discount=.8, eps=2)), 
               
    #players=[BanditHungerAgent(policy=UCBPolicy(B=2, eps=.5)),  BanditHungerAgent(GreedyPolicy(.20)), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), Random(.1), BanditHungerAgent(GreedyPolicy(.70)), Pushover(), FairHunter(), Freeloader(), Freeloader(), Pushover(), Random(.9), MaxRepHunter(), FairHunter(), FairHunter(), Random(.6), Random(.3), FairHunter(), Pushover(), BanditHungerAgent(GreedyPolicy(.99))]

    players=[BanditHungerAgent(policy=UCBPolicy(B=1, eps=2, stateCache=NonParametricStateCache(max_size=100))), 
             FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), Freeloader(), Random(.4), FairHunter(), Random(.2), Random(.8), BanditHungerAgent(policy=GreedyPolicy(eps=.95)), 
                                                                       BanditHungerAgent(policy=MetaPolicy()), Pushover(), Pushover(), Pushover(), BanditHungerAgent(policy=GreedyPolicy())]
    #players=[BanditHungerAgent(discretizer=IdentityDiscretizer(), policy=GreedyPolicy(eps=.90, stateCache=NonParametricStateCache())), 
             
     #        FairHunter(), FairHunter(), FairHunter(), Pushover(), Pushover(), Pushover(), Pushover(), Pushover(),    Freeloader(), Freeloader(),Freeloader(),Freeloader(),Freeloader(),Freeloader(),Freeloader(),Freeloader(),]
             #BanditHungerAgent(policy=UCBPolicy(B=2, eps=.5)), BanditHungerAgent(GreedyPolicy(.20)), FairHunter(), FairHunter(), Freeloader(), Random(.6), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), Freeloader(), Random(.5), Random(.1), MaxRepHunter()]
    
#    $players[Freeloader(), BanditHungerAgent(policy=GreedyPolicy(stateCache=NonParametricStateCache(), eps=.98), discretizer=IdentityDiscretizer()), BanditHungerAgent(policy=GreedyPolicy(.95))]
  # num_random = 100
   # for i in range(num_random):
    #    players.append(Random(random()))
        
   # players = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(.2), Random(.8
    #num_greedy = 10
    #for i in range(num_greedy):
     #   players.append(BanditHungerAgent(policy=GreedyPolicy(.80 + (float(i)/ num_greedy/5))))

    game = Game(players, average_rounds=20000)
    game.play_game()
    