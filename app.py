from __future__ import division, print_function

import arguments
from Game import Game
from Player import Player
from abstractions.Discretizer import TileDiscretizer, IdentityDiscretizer
from agent.hunger_agent import BanditAgent, HungerAgent2, \
    ManagerAgent
from agent.policies import UCBPolicy, GreedyPolicy, DUCBPolicy, MetaPolicy, \
    RandomPolicy, NonParametricStateCache, StateCache
from bots import *
from random import random


# BEST PLAYER:

best_player = BanditAgent(policy=UCBPolicy(B=1, eps=2, stateCache=NonParametricStateCache(max_size=100))) 


# Change these to edit the default Game parameters
DEFAULT_VERBOSITY = True
DEFAULT_MIN_ROUNDS = 300
DEFAULT_AVERAGE_ROUNDS = 1000
DEFAULT_END_EARLY = False
DEFAULT_PLAYERS = [Player(), Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(.2), Random(.8)]

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':

#    players = [Freeloader(), Pushover(), BanditAgent(), Random([.5,.5]), Random([.5,.5]), 
 #              Random([.1,.9]), Random([.2,.8]), Pushover(), Freeloader(), Freeloader(), 
  #             Freeloader(), Random([.6,.4]), Freeloader(), Alternator(), Alternator(), Alternator(), Alternator(), Alternator(), 
   #            Random([.5,.5]), Random([.8,.2])]
#    players = [BanditAgent(discretizer=IdentityDiscretizer(), policy=GreedyPolicy(stateCache=NonParametricStateCache(), eps=.90)), Freeloader(), Freeloader(), FairHunter(), FairHunter(), Pushover(), Random(.51), MaxRepHunter(), BanditAgent(MetaPolicy(meta_policy=UCBPolicy())), BanditAgent(MetaPolicy(meta_policy=GreedyPolicy(.90), policies=[RandomPolicy(.9),RandomPolicy(.1)])), 
  #                                                                             BanditAgent(MetaPolicy()),
   #                                                                             BanditAgent(MetaPolicy(meta_policy=GreedyPolicy(.85))), BanditAgent(MetaPolicy(meta_policy=UCBPolicy(B=1, eps=2))), 
    #                                                                                                          Freeloader(), FairHunter(), Random(.6), #Random(), MaxRepHunter(), FairHunter(), Pushover(),
               #Random(.8), Random(.6), Random(.5), 
 #              BanditAgent(policy= DUCBPolicy()), BanditAgent(policy = UCBPolicy(B=20, eps=1)), BanditAgent(policy = UCBPolicy())]
    

    #players = [#BanditAgent(policy=GreedyPolicy(.90)), FairHunter(), Freeloader(), Freeloader(), Random(.6), Random(.4), Random(.8),  
  #            BanditAgent(policy=GreedyPolicy(.40)), BanditAgent(policy=GreedyPolicy(.80)), BanditAgent(policy=MetaPolicy()), 
  #             Freeloader(), FairHunter(), BanditAgent(UCBPolicy()), BanditAgent(policy=MetaPolicy(meta_policy=GreedyPolicy(.90), 
   # policies=[DUCBPolicy(stateCache=NonParametricStateCache(), discount=.85), GreedyPolicy(.95), GreedyPolicy(.25), RandomPolicy(.999)])), BanditAgent(DUCBPolicy(discount=.8, eps=2)), 
               
    #players=[BanditAgent(policy=UCBPolicy(B=2, eps=.5)),  BanditAgent(GreedyPolicy(.20)), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), Random(.1), BanditAgent(GreedyPolicy(.70)), Pushover(), FairHunter(), Freeloader(), Freeloader(), Pushover(), Random(.9), MaxRepHunter(), FairHunter(), FairHunter(), Random(.6), Random(.3), FairHunter(), Pushover(), BanditAgent(GreedyPolicy(.99))]

#    players=[BanditAgent(policy=UCBPolicy(B=1, eps=2, stateCache=NonParametricStateCache(max_size=100))), 
 #            FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), Freeloader(), Random(.4), FairHunter(), Random(.2), Random(.8), BanditAgent(policy=GreedyPolicy(eps=.95)), 
  #                                                                     BanditAgent(policy=MetaPolicy()), Pushover(), Pushover(), Pushover(), BanditAgent(policy=GreedyPolicy())]
    #players=[BanditAgent(discretizer=IdentityDiscretizer(), policy=GreedyPolicy(eps=.90, stateCache=NonParametricStateCache())), 
             
     #        FairHunter(), FairHunter(), FairHunter(), Pushover(), Pushover(), Pushover(), Pushover(), Pushover(),    Freeloader(), Freeloader(),Freeloader(),Freeloader(),Freeloader(),Freeloader(),Freeloader(),Freeloader(),]
             #BanditAgent(policy=UCBPolicy(B=2, eps=.5)), BanditAgent(GreedyPolicy(.20)), FairHunter(), FairHunter(), Freeloader(), Random(.6), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), FairHunter(), Freeloader(), Random(.5), Random(.1), MaxRepHunter()]
    
#    $players[Freeloader(), BanditAgent(policy=GreedyPolicy(stateCache=NonParametricStateCache(), eps=.98), discretizer=IdentityDiscretizer()), BanditAgent(policy=GreedyPolicy(.95))]
  # num_random = 100
   # for i in range(num_random):
    #    players.append(Random(random()))
        
   # players = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(.2), Random(.8
    #num_greedy = 10
    #for i in range(num_greedy):
     #   players.append(BanditAgent(policy=GreedyPolicy(.80 + (float(i)/ num_greedy/5))))


#    players = [best_player, Freeloader(), FairHunter(), Freeloader(), FairHunter(), MaxRepHunter(), Pushover(), Random(.2), FairHunter(), Random(.10), Random(.5), Pushover(), 
 #              ManagerAgent(policy=MetaPolicy()), Freeloader(), BanditAgent(UCBPolicy()), ManagerAgent(policy=GreedyPolicy(.95, stateCache=NonParametricStateCache())), FairHunter(), FairHunter(), FairHunter(), FairHunter(), 
  #             BanditAgent(UCBPolicy()), ManagerAgent(policy=DUCBPolicy(discount=.85), worker_policy=GreedyPolicy(eps=.95)), 
   #            Random(.6), Random(.1), Random(.95), Random(.4), BanditAgent(GreedyPolicy()), Random(.3), Random(.95), Random(.5), BanditAgent(policy=MetaPolicy())]
                                  
    #players = [Freeloader(), BanditAgent(), FairHunter(),  best_player, Pushover(), HungerAgent2(), FairHunter(), Random(.5), FairHunter(), Random(.8)]
    (players, options) = arguments.get_arguments()
    # The list of players for the game is made up of
    #   'Player' (your strategy)
    #   bots from get_arguments (the bots to use)
    player_list = players
    # **options -> interpret game options from get_arguments
    #              as a dictionary to unpack into the Game parameters
    game = Game(player_list, **options)
    game.play_game()
    
