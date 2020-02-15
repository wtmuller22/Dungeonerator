from game.cardinal_direction import Direction
from game.door import Door
import random
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