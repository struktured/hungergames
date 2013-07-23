from __future__ import division, print_function
from Game import Game
from bots import Pushover, Freeloader, Alternator, RandomPlayer

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':
    players = [Pushover(), Freeloader(), Alternator(), RandomPlayer([1.0,.0])]
    game = Game(players)
    game.play_game()
