from game.cardinal_direction import Direction
from game.door import Door
import random
from pyglet.sprite import Sprite
from pyglet import image
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Contains all the data to recreate a room.
'''

class Room():

    def __init__(self, direc, backgroundX, backgroundY):
        self.startX = backgroundX
        self.startY = backgroundY
        self.location = direc
        self.entities = []
        self.add_doors()
        
    def draw(self):
        for entity in self.entities:
            entity.draw()
            
    def add_doors(self):
        if (not self.location is None):
            if (self.location == Direction.NW):
                door1 = Door(direct=Direction.SOUTH, backgroundX=self.startX, backgroundY=self.startY)
                door2 = Door(direct=Direction.EAST, backgroundX=self.startX, backgroundY=self.startY)
                self.entities.append(door1)
                self.entities.append(door2)
            elif (self.location == Direction.NE):
                door1 = Door(direct=Direction.SOUTH, backgroundX=self.startX, backgroundY=self.startY)
                door2 = Door(direct=Direction.WEST, backgroundX=self.startX, backgroundY=self.startY)
                self.entities.append(door1)
                self.entities.append(door2)
            elif (self.location == Direction.SE):
                door1 = Door(direct=Direction.NORTH, backgroundX=self.startX, backgroundY=self.startY)
                door2 = Door(direct=Direction.WEST, backgroundX=self.startX, backgroundY=self.startY)
                self.entities.append(door1)
                self.entities.append(door2)
            elif (self.location == Direction.SW):
                door1 = Door(direct=Direction.NORTH, backgroundX=self.startX, backgroundY=self.startY)
                door2 = Door(direct=Direction.EAST, backgroundX=self.startX, backgroundY=self.startY)
                self.entities.append(door1)
                self.entities.append(door2)
            elif (self.location == Direction.NORTH):
                door1 = Door(direct=Direction.EAST, backgroundX=self.startX, backgroundY=self.startY)
                door2 = Door(direct=Direction.WEST, backgroundX=self.startX, backgroundY=self.startY)
                self.entities.append(door1)
                self.entities.append(door2)
            elif (self.location == Direction.EAST):
                door1 = Door(direct=Direction.SOUTH, backgroundX=self.startX, backgroundY=self.startY)
                door2 = Door(direct=Direction.NORTH, backgroundX=self.startX, backgroundY=self.startY)
                self.entities.append(door1)
                self.entities.append(door2)
            elif (self.location == Direction.SOUTH):
                door1 = Door(direct=Direction.EAST, backgroundX=self.startX, backgroundY=self.startY)
                door2 = Door(direct=Direction.WEST, backgroundX=self.startX, backgroundY=self.startY)
                self.entities.append(door1)
                self.entities.append(door2)
            elif (self.location == Direction.WEST):
                door1 = Door(direct=Direction.SOUTH, backgroundX=self.startX, backgroundY=self.startY)
                door2 = Door(direct=Direction.NORTH, backgroundX=self.startX, backgroundY=self.startY)
                self.entities.append(door1)
                self.entities.append(door2)
                
    def make_level_up(self):
        if (self.location == Direction.NW or self.location == Direction.NE or self.location == Direction.SE or self.location == Direction.SW):
            rand_num = random.randint(1, 2)
            if (self.location == Direction.NW):
                if (rand_num == 1):
                    door = Door(direct=Direction.NORTH, backgroundX=self.startX, backgroundY=self.startY)
                    door.make_golden()
                    self.entities.append(door)
                else:
                    door = Door(direct=Direction.WEST, backgroundX=self.startX, backgroundY=self.startY)
                    door.make_golden()
                    self.entities.append(door)
            elif (self.location == Direction.NE):
                if (rand_num == 1):
                    door = Door(direct=Direction.NORTH, backgroundX=self.startX, backgroundY=self.startY)
                    door.make_golden()
                    self.entities.append(door)
                else:
                    door = Door(direct=Direction.EAST, backgroundX=self.startX, backgroundY=self.startY)
                    door.make_golden()
                    self.entities.append(door)
            elif (self.location == Direction.SE):
                if (rand_num == 1):
                    door = Door(direct=Direction.SOUTH, backgroundX=self.startX, backgroundY=self.startY)
                    door.make_golden()
                    self.entities.append(door)
                else:
                    door = Door(direct=Direction.EAST, backgroundX=self.startX, backgroundY=self.startY)
                    door.make_golden()
                    self.entities.append(door)
            else:
                if (rand_num == 1):
                    door = Door(direct=Direction.SOUTH, backgroundX=self.startX, backgroundY=self.startY)
                    door.make_golden()
                    self.entities.append(door)
                else:
                    door = Door(direct=Direction.WEST, backgroundX=self.startX, backgroundY=self.startY)
                    door.make_golden()
                    self.entities.append(door)
        else:
            door = Door(direct=self.location, backgroundX=self.startX, backgroundY=self.startY)
            door.make_golden()
            self.entities.append(door)
            
    def intersecting_door(self, playerX, playerY) -> Door:
        for entity in self.entities:
            if (type(entity) is Door):
                result = entity.check_intersection(playerX, playerY)
                if (result):
                    return entity
        return None
    
    def is_entity(self, aX, aY) -> bool:
        for entity in self.entities:
            if (not type(entity) is Door):
                result = (entity.x == aX and entity.y == aY)
                if (result):
                    return True
        if (not self.intersecting_door(playerX=aX, playerY=aY) is None):
            return True
        return False
    
    def is_monster(self, aX, aY) -> bool:
        for entity in self.entities:
            if (type(entity) is Monster):
                result = (entity.x == aX and entity.y == aY)
                if (result):
                    return True
        return False
    
    def add_entities(self):
        rand_num = random.randint(0, 9)
        if (rand_num > 1):
            to_add = Monster(backgroundX=self.startX, backgroundY=self.startY, this_room=self)
            self.entities.append(to_add)
        if (rand_num > 5):
            to_add = Monster(backgroundX=self.startX, backgroundY=self.startY, this_room=self)
            self.entities.append(to_add)
        if (rand_num > 8):
            to_add = Monster(backgroundX=self.startX, backgroundY=self.startY, this_room=self)
            self.entities.append(to_add)
            
'''
Created on Feb 11, 2020

@author: Wyatt Muller

A dungeon monster to attack player.
'''

class Monster(Sprite):
    
    bat_east_standing = image.load('images/BatEastStanding.png')
    bat_north_standing = image.load('images/BatNorthStanding.png')
    bat_south_standing = image.load('images/BatSouthStanding.png')
    bat_west_standing = image.load('images/BatWestStanding.png')
    bat_east_moving = image.load_animation('images/BatEast.gif', None, None)
    bat_north_moving = image.load_animation('images/BatNorth.gif', None, None)
    bat_south_moving = image.load_animation('images/BatSouth.gif', None, None)
    bat_west_moving = image.load_animation('images/BatWest.gif', None, None)

    def __init__(self, backgroundX, backgroundY, this_room):
        super().__init__(img=Monster.bat_south_standing)
        self.startX = backgroundX
        self.startY = backgroundY
        self.curr_room = this_room
        self.standing_img_east = None
        self.standing_img_north = None
        self.standing_img_south = None
        self.standing_img_west = None
        self.moving_img_east = None
        self.moving_img_north = None
        self.moving_img_south = None
        self.moving_img_west = None
        self.health = None
        self.speed = None
        self.attack = None
        self.pick_random_monster()
        self.pick_random_location()
        
    def pick_random_monster(self):
        rand_num = random.randint(0, 0)
        if (rand_num == 0):
            self.standing_img_south = Monster.bat_south_standing
            self.moving_img_south = Monster.bat_south_moving
            self.standing_img_east = Monster.bat_east_standing
            self.moving_img_east = Monster.bat_east_moving
            self.standing_img_north = Monster.bat_north_standing
            self.moving_img_north = Monster.bat_north_moving
            self.standing_img_west = Monster.bat_west_standing
            self.moving_img_west = Monster.bat_west_moving
            self.health = 10
            self.speed = 240
            self.attack = 5
        self.image = self.standing_img_south
            
    def pick_random_location(self):
            rand_x = (random.randint(0, 24) * 40) + self.startX
            rand_y = (random.randint(0, 24) * 40) + self.startY
            while (self.curr_room.is_entity(aX=rand_x, aY=rand_y)):
                rand_x = (random.randint(0, 24) * 40) + self.startX
                rand_y = (random.randint(0, 24) * 40) + self.startY
            self.x = rand_x
            self.y = rand_y
            
    def remove_self(self):
        self.delete()
        self.curr_room.entities.remove(self)
        
    def take_damage(self, damage):
        self.health = self.health - damage
        if (self.health <= 0):
            self.remove_self()