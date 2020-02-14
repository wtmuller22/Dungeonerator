from pyglet.sprite import Sprite
from game.cardinal_direction import Direction
from pyglet import image
'''
Created on Feb 13, 2020

@author: Wyatt Muller

A doorway which the player can move between rooms through.
'''

class Door(Sprite):
    
    door_img = image.load('images/Doorway.png')
    level_up = image.load('images/DoorwayLevelUp.png')

    def __init__(self, direct, backgroundX, backgroundY):
        super().__init__(img=Door.door_img)
        self.is_gold = False
        if (direct == Direction.NORTH):
            self.rotation=90
            self.x=480 + backgroundX
            self.y=1000 + backgroundY
        elif (direct == Direction.EAST):
            self.rotation=180
            self.x=1000 + backgroundX
            self.y=520 + backgroundY
        elif (direct == Direction.SOUTH):
            self.rotation=270
            self.x=520 + backgroundX
            self.y=0 + backgroundY
        else:
            self.x=0 + backgroundX
            self.y=480 + backgroundY
            
    def make_golden(self):
        self.image=Door.level_up
        self.is_gold = True
        
    def is_level_up(self) -> bool:
        return self.is_gold