from __future__ import division, print_function
from Game import Game

from abstractions.Discretizer import Discretizer
from agent.hunger_agent import HungerAgent
from agent.policies import UCBPolicy, GreedyPolicy
from bots import *
from Player import Player

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':

#    players = [Freeloader(), Pushover(), HungerAgent(), Random([.5,.5]), Random([.5,.5]), 
 #              Random([.1,.9]), Random([.2,.8]), Pushover(), Freeloader(), Freeloader(), 
  #             Freeloader(), Random([.6,.4]), Freeloader(), Alternator(), Alternator(), Alternator(), Alternator(), Alternator(), 
   #            Random([.5,.5]), Random([.8,.2])]
    players = [Random(), MaxRepHunter(), FairHunter(), Pushover(),
               Random(.8), Random(.6), Random(.5), 
               HungerAgent(policy= GreedyPolicy(.95)), HungerAgent(policy = UCBPolicy())]
       
   # players = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(.2), Random(.8)]
    game = Game(players)
    game.play_game()
