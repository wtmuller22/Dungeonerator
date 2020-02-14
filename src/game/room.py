from game.cardinal_direction import Direction
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Contains all the data to recreate a room.
'''

class Room():

    def __init__(self, direc):
        self.location = direc
        self.entities = []