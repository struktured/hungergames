from __future__ import division, print_function
from Game import Game
from bots import Pushover, Freeloader, Alternator, RandomPlayer
from hunger_agent import HungerAgent

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':
    players = [Freeloader(), Pushover(), HungerAgent(), RandomPlayer([.5,.5]), RandomPlayer([.5,.5]), 
               RandomPlayer([.1,.9]), RandomPlayer([.2,.8]), Pushover(), Freeloader(), Freeloader(), 
               Freeloader(), RandomPlayer([.6,.4]), Freeloader(), Alternator(), Alternator(), Alternator(), Alternator(), Alternator(), 
               RandomPlayer([.5,.5]), RandomPlayer([.8,.2])]
    game = Game(players)
    game.play_game()
