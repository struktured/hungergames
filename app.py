from __future__ import division, print_function
from Game import Game
from Player import Player
from abstractions.Discretizer import Discretizer
from agent.hunger_agent import HungerAgent
from agent.policies import UCBPolicy, GreedyPolicy, DUCBPolicy, MetaPolicy
from bots import *
from random import random

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':

#    players = [Freeloader(), Pushover(), HungerAgent(), Random([.5,.5]), Random([.5,.5]), 
 #              Random([.1,.9]), Random([.2,.8]), Pushover(), Freeloader(), Freeloader(), 
  #             Freeloader(), Random([.6,.4]), Freeloader(), Alternator(), Alternator(), Alternator(), Alternator(), Alternator(), 
   #            Random([.5,.5]), Random([.8,.2])]
    players = [HungerAgent(MetaPolicy()), Freeloader(), FairHunter(), Random(.6), #Random(), MaxRepHunter(), FairHunter(), Pushover(),
               #Random(.8), Random(.6), Random(.5), 
               HungerAgent(policy= DUCBPolicy()), HungerAgent(policy = UCBPolicy(B=4, eps=2)), HungerAgent(policy = UCBPolicy())]
    
    num_greedy = 200
    for i in range(num_greedy):
        players.append(HungerAgent(policy=GreedyPolicy(.80 + (float(i)/ num_greedy/5))))

  # num_random = 100
   # for i in range(num_random):
    #    players.append(Random(random()))
        
   # players = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(.2), Random(.8
    game = Game(players, average_rounds=50000)
    game.play_game()
    