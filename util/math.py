'''
Created on Jul 22, 2013

@author: carm
'''
import random
def weighted_choice(probabilities):
    random_position = random.random() * sum(probabilities)
    current_position = 0.0
    for i, p in enumerate(probabilities):
        current_position += p
        if random_position < current_position:
            return i
    return None

def range_index(splice, v):
    for i in range(len(splice)) :
        if v <= splice[i] : return i
    return len(splice)-1
    