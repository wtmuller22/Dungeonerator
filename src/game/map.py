from game.room import Room
from game.cardinal_direction import Direction
from game.door import Door
import random
'''
Created on Feb 11, 2020

@author: Wyatt Muller

Holds a dictionary of the explored rooms.
'''

class Map():

    def __init__(self, backgroundX, backgroundY):
        self.startX = backgroundX
        self.startY = backgroundY
        self.room_dict = {}
        self.corner_numbers = {}
        starting_room = Room(direc=None, backgroundX=self.startX, backgroundY=self.startY, this_level=0)
        num = random.randint(0, 3)
        if (num == 0):
            level_up = Door(direct=Direction.NORTH, backgroundX=self.startX, backgroundY=self.startY)
            level_up.make_golden()
            starting_room.entities.append(level_up)
        elif (num == 1):
            level_up = Door(direct=Direction.EAST, backgroundX=self.startX, backgroundY=self.startY)
            level_up.make_golden()
            starting_room.entities.append(level_up)
        elif (num == 2):
            level_up = Door(direct=Direction.SOUTH, backgroundX=self.startX, backgroundY=self.startY)
            level_up.make_golden()
            starting_room.entities.append(level_up)
        else:
            level_up = Door(direct=Direction.WEST, backgroundX=self.startX, backgroundY=self.startY)
            level_up.make_golden()
            starting_room.entities.append(level_up)
        self.room_dict[0] = starting_room
        self.corner_numbers[0] = None
        
    def prepare_level(self, level_num):
        num_rooms = 8 * level_num
        rand_num = random.randint(1, num_rooms)
        rand_room_num = rand_num + (8 * (level_num - 1))
        num_rooms_per_side_previous = 1 + ((level_num - 1) * 2)
        num_rooms_per_side_current = 1 + (level_num * 2)
        curr_NW_number = num_rooms_per_side_previous**2
        corners = [curr_NW_number, curr_NW_number + (num_rooms_per_side_current - 1), curr_NW_number + (2 * (num_rooms_per_side_current - 1)), curr_NW_number + (3 * (num_rooms_per_side_current - 1))]
        self.corner_numbers[level_num] = corners
        rand_room_direct = self.get_room_direction(number=rand_room_num, level=level_num)
        room_to_add = Room(direc=rand_room_direct, backgroundX=self.startX, backgroundY=self.startY, this_level=level_num)
        room_to_add.make_level_up()
        room_to_add.add_entities()
        self.room_dict[rand_room_num] = room_to_add
        
    def get_room_direction(self, number, level) -> Direction:
        corners = self.corner_numbers.get(level)
        if (number == corners[0]):
            return Direction.NW
        elif (number == corners[1]):
            return Direction.NE
        elif (number == corners[2]):
            return Direction.SE
        elif (number == corners[3]):
            return Direction.SW
        elif (number < corners[1]):
            return Direction.NORTH
        elif (number < corners[2]):
            return Direction.EAST
        elif (number < corners[3]):
            return Direction.SOUTH
        else:
            return Direction.WEST
        
    def change_to_room(self, number, level) -> Room:
        result = self.room_dict.get(number)
        if (result is None):
            room_direct = self.get_room_direction(number, level)
            room_to_add = Room(direc=room_direct, backgroundX=self.startX, backgroundY=self.startY, this_level=level)
            room_to_add.add_entities()
            self.room_dict[number] = room_to_add
        return self.room_dict.get(number)
    
    def level_prepared(self, level) -> bool:
        result = self.corner_numbers.get(level)
        return (not result is None)
