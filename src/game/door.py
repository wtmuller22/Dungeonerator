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

    def __init__(self, game_scale, direct, backgroundX, backgroundY):
        super().__init__(img=Door.door_img)
        self.scale = game_scale
        self.is_gold = False
        if (direct == Direction.NORTH):
            self.rotation=90
            self.x=(480 * game_scale) + backgroundX
            self.y=(1000 * game_scale) + backgroundY
        elif (direct == Direction.EAST):
            self.rotation=180
            self.x=(1000 * game_scale) + backgroundX
            self.y=(520 * game_scale) + backgroundY
        elif (direct == Direction.SOUTH):
            self.rotation=270
            self.x=(520 * game_scale) + backgroundX
            self.y=0 + backgroundY
        else:
            self.x=0 + backgroundX
            self.y=(480 * game_scale) + backgroundY
            
    def scale_entity(self, game_scale, x_offset):
        self.scale = game_scale
        self.x = (self.x * game_scale) + x_offset
        self.y = (self.y * game_scale)
            
    def make_golden(self):
        self.image=Door.level_up
        self.is_gold = True
        
    def is_level_up(self) -> bool:
        return self.is_gold
    
    def check_intersection(self, playerX, playerY) -> bool:
        if (self.rotation == 90):
            return (round(playerX, 1) == round(self.x, 1)) and (round(playerY, 1) == round(self.y - (40 * self.scale), 1))
        elif (self.rotation == 180):
            return ((round(playerX, 1) == round(self.x - (40 * self.scale), 1)) and (round(playerY, 1) == round(self.y - (40 * self.scale), 1)))
        elif (self.rotation == 270):
            return ((round(playerX, 1) == round(self.x - (40 * self.scale), 1)) and (round(playerY, 1) == round(self.y, 1)))
        else:
            return ((round(playerX, 1) == round(self.x, 1)) and (round(playerY, 1) == round(self.y, 1)))