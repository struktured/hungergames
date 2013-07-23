# This file is intended to be a final submission. python tester.py Player.py
# should work at all times. If it does not, there is a bug.
# If you're just trying to test a solution, scroll down to the Player
# class.

# This file is intended to be in the same format as a valid solution, so
# that users can edit their solution into Player and then submit just this
# file to the contest. If you see any reason this would not work, please submit
# an Issue to https://github.com/ChadAMiller/hungergames/issues or email me.

class BasePlayer(object):
    '''
    Base class so I don't have to repeat bookkeeping stuff.
    Do not edit unless you're working on the simulation.
    '''
    
    def __repr__(self):
        try:
            return self.name
        except AttributeError:
            return super(BasePlayer, self).__repr__()
    
    def hunt_choices(*args, **kwargs):  # @NoSelf
        raise NotImplementedError("You must define a strategy!")
        
    def hunt_outcomes(*args, **kwargs):  # @NoSelf
        pass
        
    def round_end(*args, **kwargs):  # @NoSelf
        pass


class Player(BasePlayer):
    '''
    Your strategy starts here.
    '''
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['s']*len(player_reputations)
        
    def hunt_outcomes(self, food_earnings):
        pass
        
    def round_end(self, award, m, number_hunters):
        pass
        