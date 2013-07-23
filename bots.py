from Player import BasePlayer
from util.math import weighted_choice

class Pushover(BasePlayer):
    '''Player that always hunts.'''
    def __init__(self):
        self.name = "Pushover"
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h']*len(player_reputations)

        
class Freeloader(BasePlayer):
    '''Player that never hunts.'''
    
    def __init__(self):
        self.name = "Freeloader"
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['s']*len(player_reputations)
        

class Alternator(BasePlayer):
    '''Player that alternates between hunting and not.'''
    def __init__(self):
        self.name = "Alternator"
        self.moves = ['s', 'h']
        
    def update_strat(self):
        self.moves.reverse()
        
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        self.update_strat()
        return [self.moves[0]]*len(player_reputations)

class RandomPlayer(BasePlayer): 
    '''Player that alternates between hunting and not.'''    
    def __init__(self, dist=[.5, .5]):        
        self.name = "Random(" + str(dist) + ")" 
        self.moves = ['s', 'h']
        self.dist = dist
        
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return [self.moves[weighted_choice(self.dist)] for _ in range(len(player_reputations))]
