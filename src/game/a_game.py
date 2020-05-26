from game.map import Map
from game.cardinal_direction import Direction
from game.door import Door
import pyglet
'''
Created on May 25, 2020

@author: Wyatt Muller
'''

class Game():

    def __init__(self):
        self.room_map = Map(a_scale=1, backgroundX=0, backgroundY=0)
        self.players = []
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        pyglet.clock.schedule_interval(self.check_ground, 1/60.0)
        
    def update(self, dt):
        for player in self.players:
            current_room = self.room_map.change_to_room(player.room_number, player.level)
            if (player.is_moving):
                if (player.facing == Direction.NORTH or player.facing == Direction.SOUTH):
                    total_damage = current_room.update(dt, playerX=player.x, playerY=player.nextBoxCoord)
                    if (total_damage > 0):
                        is_dead = player.change_life(-1 * total_damage)
                        if (is_dead):
                            self.player_died(player)
                else:
                    total_damage = current_room.update(dt, playerX=player.nextBoxCoord, playerY=player.y)
                    if (total_damage > 0):
                        is_dead = player.change_life(-1 * total_damage)
                        if (is_dead):
                            self.player_died(player)
            else:
                total_damage = current_room.update(dt, playerX=player.x, playerY=player.y)
                if (total_damage > 0):
                        is_dead = player.change_life(-1 * total_damage)
                        if (is_dead):
                            self.player_died(player)
                            
    def check_ground(self, dt):
        for player in self.players:
            current_room = self.room_map.change_to_room(player.room_number, player.level)
            result = current_room.intersecting_item(playerX=player.x, playerY=player.y)
            player.visibility.update_coords(aX=(player.x + (40 / 2)), aY=(player.y + (40 / 2)))
            if (not result is None):
                ground_type = result.item_enum
                add_result = player.add_to_inventory(to_add=ground_type)
                if (add_result):
                    result.remove_self()
                            
    def player_died(self, player):
        player.stop_moving()
        player.fade()
        
    def start_moving_player(self, dt, p):
        self.players[p].scheduled_moving = False
        self.set_next_box_coords(p)
        valid = self.check_player_legal_movement(p)
        if (valid):
            self.players[p].start_moving()
            pyglet.clock.schedule_interval(self.moving_bounds_check, 1/100.0, p)
            
    def set_next_box_coords(self, p):
        if (self.players[p].facing == Direction.WEST):
            self.players[p].nextBoxCoord = self.players[p].x - ((self.players[p].x - 0) % 40)
        elif (self.players[p].facing == Direction.EAST):
            self.players[p].nextBoxCoord = self.players[p].x + (40 - ((self.players[p].x - 0) % 40))
        elif (self.players[p].facing == Direction.NORTH):
            self.players[p].nextBoxCoord = self.players[p].y + (40 - ((self.players[p].y - 0) % 40))
        else:
            self.players[p].nextBoxCoord = self.players[p].y - ((self.players[p].y - 0) % 40)
            
    def check_player_legal_movement(self, p) -> bool:
        curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
        if (self.players[p].facing == Direction.WEST):
            result = self.players[p].x > 0
            check_x = self.players[p].nextBoxCoord
            if (check_x == self.players[p].x):
                check_x = check_x - 40
            is_monster = curr_room.is_monster(aX=(check_x), aY=(self.players[p].y))
            if (not result):
                door = curr_room.intersecting_door(playerX=self.players[p].x, playerY=self.players[p].y)
                if (not door is None):
                    is_golden = door.is_level_up()
                    if (not is_golden):
                        self.change_player_room(p)
                    else:
                        self.change_player_level(p)
            return result and (not is_monster)
        elif (self.players[p].facing == Direction.EAST):
            result = self.players[p].x < 0 + 1000 - 40
            check_x = self.players[p].nextBoxCoord
            if (check_x == self.players[p].x):
                check_x = check_x + 40
            is_monster = curr_room.is_monster(aX=(check_x), aY=(self.players[p].y))
            if (not result):
                door = curr_room.intersecting_door(playerX=self.players[p].x, playerY=self.players[p].y)
                if (not door is None):
                    is_golden = door.is_level_up()
                    if (not is_golden):
                        self.change_player_room(p)
                    else:
                        self.change_player_level(p)
            return result and (not is_monster)
        elif (self.players[p].facing == Direction.NORTH):
            result = self.players[p].y < 0 + 1000 - 40
            check_y = self.players[p].nextBoxCoord
            if (check_y == self.players[p].y):
                check_y = check_y + 40
            is_monster = curr_room.is_monster(aX=(self.players[p].x), aY=(check_y))
            if (not result):
                door = curr_room.intersecting_door(playerX=self.players[p].x, playerY=self.players[p].y)
                if (not door is None):
                    is_golden = door.is_level_up()
                    if (not is_golden):
                        self.change_player_room(p)
                    else:
                        self.change_player_level(p)
            return result and (not is_monster)
        else:
            result = self.players[p].y > 0
            check_y = self.players[p].nextBoxCoord
            if (check_y == self.players[p].y):
                check_y = check_y - 40
            is_monster = curr_room.is_monster(aX=(self.players[p].x), aY=(check_y))
            if (not result):
                door = curr_room.intersecting_door(playerX=self.players[p].x, playerY=self.players[p].y)
                if (not door is None):
                    is_golden = door.is_level_up()
                    if (not is_golden):
                        self.change_player_room(p)
                    else:
                        self.change_player_level(p)
            return result and (not is_monster)
        
    def change_player_room(self, p):
        curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
        room_location = curr_room.location
        player_facing = self.players[p].facing
        if (room_location == Direction.NW):
            if (player_facing == Direction.EAST):
                self.players[p].room_number = self.players[p].room_number + 1
                self.players[p].x = self.players[p].x - (1000 - 40)
            elif (player_facing == Direction.SOUTH):
                num_rooms_per_side = (self.players[p].level * 2) + 1
                self.players[p].room_number = (num_rooms_per_side**2) - 1
                self.players[p].y = self.players[p].y + (1000 - 40)
        elif (room_location == Direction.NE):
            if (player_facing == Direction.WEST):
                self.players[p].room_number = self.players[p].room_number - 1
                self.players[p].x = self.players[p].x + (1000 - 40)
            elif (player_facing == Direction.SOUTH):
                self.players[p].room_number = self.players[p].room_number + 1
                self.players[p].y = self.players[p].y + (1000 - 40)
        elif (room_location == Direction.SE):
            if (player_facing == Direction.NORTH):
                self.players[p].room_number = self.players[p].room_number - 1
                self.players[p].y = self.players[p].y - (1000 - 40)
            elif (player_facing == Direction.WEST):
                self.players[p].room_number = self.players[p].room_number + 1
                self.players[p].x = self.players[p].x + (1000 - 40)
        elif (room_location == Direction.SW):
            if (player_facing == Direction.EAST):
                self.players[p].room_number = self.players[p].room_number - 1
                self.players[p].x = self.players[p].x - (1000 - 40)
            elif (player_facing == Direction.NORTH):
                self.players[p].room_number = self.players[p].room_number + 1
                self.players[p].y = self.players[p].y - (1000 - 40)
        elif (room_location == Direction.NORTH):
            if (player_facing == Direction.EAST):
                self.players[p].room_number = self.players[p].room_number + 1
                self.players[p].x = self.players[p].x - (1000 - 40)
            elif (player_facing == Direction.WEST):
                self.players[p].room_number = self.players[p].room_number - 1
                self.players[p].x = self.players[p].x + (1000 - 40)
        elif (room_location == Direction.EAST):
            if (player_facing == Direction.NORTH):
                self.players[p].room_number = self.players[p].room_number - 1
                self.players[p].y = self.players[p].y - (1000 - 40)
            elif (player_facing == Direction.SOUTH):
                self.players[p].room_number = self.players[p].room_number + 1
                self.players[p].y = self.players[p].y + (1000 - 40)
        elif (room_location == Direction.SOUTH):
            if (player_facing == Direction.EAST):
                self.players[p].room_number = self.players[p].room_number - 1
                self.players[p].x = self.players[p].x - (1000 - 40)
            elif (player_facing == Direction.WEST):
                self.players[p].room_number = self.players[p].room_number + 1
                self.players[p].x = self.players[p].x + (1000 - 40)
        else:
            if (player_facing == Direction.NORTH):
                num_rooms_per_side = (self.players[p].level * 2) + 1
                if (self.players[p].room_number == ((num_rooms_per_side**2) - 1)):
                    self.players[p].room_number = (((self.players[p].level - 1) * 2) + 1)**2
                else:
                    self.players[p].room_number = self.players[p].room_number + 1
                self.players[p].y = self.players[p].y - (1000 - 40)
            elif (player_facing == Direction.SOUTH):
                self.players[p].room_number = self.players[p].room_number - 1
                self.players[p].y = self.players[p].y + (1000 - 40)
                
    def change_player_level(self, p):
        curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
        room_location = curr_room.location
        player_facing = self.players[p].facing
        if ((room_location == Direction.NW or room_location == Direction.NORTH or room_location == Direction.NE) and (player_facing == Direction.NORTH)):
            result = self.room_map.level_prepared(level=(self.players[p].level + 1))
            door = None
            if (not result):
                self.players[p].add_experience(exp=(5 * (self.players[p].level + 1)))
                self.room_map.prepare_level(level_num=(self.players[p].level + 1))
                door = Door(game_scale=1, direct=Direction.SOUTH, backgroundX=0, backgroundY=0)
                door.make_golden()
            self.players[p].room_number = self.players[p].room_number + (8 * self.players[p].level) + 1
            self.players[p].level = self.players[p].level + 1
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].y = self.players[p].y - (1000 - 40)
            if (not door is None):
                curr_room.entities.append(door)
        elif ((room_location == Direction.NW or room_location == Direction.WEST or room_location == Direction.SW) and (player_facing == Direction.WEST)):
            result = self.room_map.level_prepared(level=(self.players[p].level + 1))
            door = None
            if (not result):
                self.players[p].add_experience(exp=(5 * (self.players[p].level + 1)))
                self.room_map.prepare_level(level_num=(self.players[p].level + 1))
                door = Door(game_scale=1, direct=Direction.EAST, backgroundX=0, backgroundY=0)
                door.make_golden()
            self.players[p].room_number = self.players[p].room_number + (8 * self.players[p].level) + 7
            self.players[p].level = self.players[p].level + 1
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].x = self.players[p].x + (1000 - 40)
            if (not door is None):
                curr_room.entities.append(door)
        elif ((room_location == Direction.SW or room_location == Direction.SOUTH or room_location == Direction.SE) and (player_facing == Direction.SOUTH)):
            result = self.room_map.level_prepared(level=(self.players[p].level + 1))
            door = None
            if (not result):
                self.players[p].add_experience(exp=(5 * (self.players[p].level + 1)))
                self.room_map.prepare_level(level_num=(self.players[p].level + 1))
                door = Door(game_scale=1, direct=Direction.NORTH, backgroundX=0, backgroundY=0)
                door.make_golden()
            self.players[p].room_number = self.players[p].room_number + (8 * self.players[p].level) + 5
            self.players[p].level = self.players[p].level + 1
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].y = self.players[p].y + (1000 - 40)
            if (not door is None):
                curr_room.entities.append(door)
        elif ((room_location == Direction.NE or room_location == Direction.EAST or room_location == Direction.SE) and (player_facing == Direction.EAST)):
            result = self.room_map.level_prepared(level=(self.players[p].level + 1))
            door = None
            if (not result):
                self.players[p].add_experience(exp=(5 * (self.players[p].level + 1)))
                self.room_map.prepare_level(level_num=(self.players[p].level + 1))
                door = Door(game_scale=1, direct=Direction.WEST, backgroundX=0, backgroundY=0)
                door.make_golden()
            self.players[p].room_number = self.players[p].room_number + (8 * self.players[p].level) + 3
            self.players[p].level = self.players[p].level + 1
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].x = self.players[p].x - (1000 - 40)
            if (not door is None):
                curr_room.entities.append(door)
        elif ((room_location == Direction.NORTH) and (player_facing == Direction.SOUTH)):
            self.players[p].level = self.players[p].level - 1
            self.players[p].room_number = self.players[p].room_number - ((8 * self.players[p].level) + 1)
            if (self.players[p].level == 0):
                self.players[p].room_number = 0
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].y = self.players[p].y + (1000 - 40)
        elif ((room_location == Direction.EAST) and (player_facing == Direction.WEST)):
            self.players[p].level = self.players[p].level - 1
            self.players[p].room_number = self.players[p].room_number - ((8 * self.players[p].level) + 3)
            if (self.players[p].level == 0):
                self.players[p].room_number = 0
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].x = self.players[p].x + (1000 - 40)
        elif ((room_location == Direction.SOUTH) and (player_facing == Direction.NORTH)):
            self.players[p].level = self.players[p].level - 1
            self.players[p].room_number = self.players[p].room_number - ((8 * self.players[p].level) + 5)
            if (self.players[p].level == 0):
                self.players[p].room_number = 0
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].y = self.players[p].y - (1000 - 40)
        elif ((room_location == Direction.WEST) and (player_facing == Direction.EAST)):
            self.players[p].level = self.players[p].level - 1
            self.players[p].room_number = self.players[p].room_number - ((8 * self.players[p].level) + 7)
            if (self.players[p].level == 0):
                self.players[p].room_number = 0
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].x = self.players[p].x - (1000 - 40)
        else:
            if (player_facing == Direction.NORTH):
                result = self.room_map.level_prepared(level=(self.players[p].level + 1))
                door = None
                if (not result):
                    self.players[p].add_experience(exp=(5 * (self.players[p].level + 1)))
                    self.room_map.prepare_level(level_num=(self.players[p].level + 1))
                    door = Door(game_scale=1, direct=Direction.SOUTH, backgroundX=0, backgroundY=0)
                    door.make_golden()
                self.players[p].room_number = self.players[p].room_number + 2
                self.players[p].level = self.players[p].level + 1
                curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
                self.players[p].y = self.players[p].y - (1000 - 40)
                if (not door is None):
                    curr_room.entities.append(door)
            elif (player_facing == Direction.EAST):
                result = self.room_map.level_prepared(level=(self.players[p].level + 1))
                door = None
                if (not result):
                    self.players[p].add_experience(exp=(5 * (self.players[p].level + 1)))
                    self.room_map.prepare_level(level_num=(self.players[p].level + 1))
                    door = Door(game_scale=1, direct=Direction.WEST, backgroundX=0, backgroundY=0)
                    door.make_golden()
                self.players[p].room_number = self.players[p].room_number + 4
                self.players[p].level = self.players[p].level + 1
                curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
                self.players[p].x = self.players[p].x - (1000 - 40)
                if (not door is None):
                    curr_room.entities.append(door)
            elif (player_facing == Direction.SOUTH):
                result = self.room_map.level_prepared(level=(self.players[p].level + 1))
                door = None
                if (not result):
                    self.players[p].add_experience(exp=(5 * (self.players[p].level + 1)))
                    self.room_map.prepare_level(level_num=(self.players[p].level + 1))
                    door = Door(game_scale=1, direct=Direction.NORTH, backgroundX=0, backgroundY=0)
                    door.make_golden()
                self.players[p].room_number = self.players[p].room_number + 6
                self.players[p].level = self.players[p].level + 1
                curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
                self.players[p].y = self.players[p].y + (1000 - 40)
                if (not door is None):
                    curr_room.entities.append(door)
            else:
                result = self.room_map.level_prepared(level=(self.players[p].level + 1))
                door = None
                if (not result):
                    self.players[p].add_experience(exp=(5 * (self.players[p].level + 1)))
                    self.room_map.prepare_level(level_num=(self.players[p].level + 1))
                    door = Door(game_scale=1, direct=Direction.EAST, backgroundX=0, backgroundY=0)
                    door.make_golden()
                self.players[p].room_number = self.players[p].room_number + 8
                self.players[p].level = self.players[p].level + 1
                curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
                self.players[p].x = self.players[p].x + (1000 - 40)
                if (not door is None):
                    curr_room.entities.append(door)
                    
    def moving_bounds_check(self, dt, p):
        self.set_next_box_coords()
        valid = self.check_player_legal_movement()
        if (not valid):
            self.players[p].stop_moving()
            self.set_player_last_valid(p)
            pyglet.clock.unschedule(self.moving_bounds_check)
            
    def set_player_last_valid(self, p):
        if (self.players[p].facing == Direction.WEST):
            if (self.players[p].x <= 0):
                self.players[p].x = 0
            else:
                if (self.players[p].x != self.players[p].nextBoxCoord):
                    self.players[p].x = self.players[p].nextBoxCoord + 40
        elif (self.players[p].facing == Direction.EAST):
            if (self.players[p].x >= 0 + 1000 - 40):
                self.players[p].x = 0 + 1000 - 40
            else:
                if (self.players[p].x != self.players[p].nextBoxCoord):
                    self.players[p].x = self.players[p].nextBoxCoord - 40
        elif (self.players[p].facing == Direction.NORTH):
            if (self.players[p].y >= 0 + 1000 - 40):
                self.players[p].y = 0 + 1000 - 40
            else:
                if (self.players[p].y != self.players[p].nextBoxCoord):
                    self.players[p].y = self.players[p].nextBoxCoord - 40
        else:
            if (self.players[p].y <= 0):
                self.players[p].y = 0
            else:
                if (self.players[p].y != self.players[p].nextBoxCoord):
                    self.players[p].y = self.players[p].nextBoxCoord + 40
                    
    def player_attack(self, p):
        if self.players[p].attack > 0 and not self.players[p].is_attacking:
            curr_room = self.room_map.change_to_room(number=self.players[p].room_number, level=self.players[p].level)
            self.players[p].is_attacking = True
            pyglet.clock.schedule_once(self.players[p].stop_attack, 0.75)
            self.players[p].attack_sprite.reset_animation()
            if self.players[p].facing == Direction.NORTH:
                check_y = self.players[p].nextBoxCoord
                if (check_y == self.players[p].y):
                    check_y = check_y + 40
                total_exp = curr_room.player_attack(damage=self.players[p].attack, playerX=self.players[p].x, playerY=check_y)
                result = self.players[p].selected_weapon.take_damage(damage=5)
                self.players[p].add_experience(exp=total_exp)
                if (result):
                    self.players[p].selected_weapon = None
            elif self.players[p].facing == Direction.EAST:
                check_x = self.players[p].nextBoxCoord
                if (check_x == self.players[p].x):
                    check_x = check_x + 40
                total_exp = curr_room.player_attack(damage=self.players[p].attack, playerX=check_x, playerY=self.players[p].y)
                result = self.players[p].selected_weapon.take_damage(damage=5)
                self.players[p].add_experience(exp=total_exp)
                if (result):
                    self.players[p].selected_weapon = None
            elif self.players[p].facing == Direction.SOUTH:
                check_y = self.players[p].nextBoxCoord
                if (check_y == self.players[p].y):
                    check_y = check_y - 40
                total_exp = curr_room.player_attack(damage=self.players[p].attack, playerX=self.players[p].x, playerY=check_y)
                result = self.players[p].selected_weapon.take_damage(damage=5)
                self.players[p].add_experience(exp=total_exp)
                if (result):
                    self.players[p].selected_weapon = None
            else:
                check_x = self.players[p].nextBoxCoord
                if (check_x == self.players[p].x):
                    check_x = check_x - 40
                total_exp = curr_room.player_attack(damage=self.players[p].attack, playerX=check_x, playerY=self.players[p].y)
                result = self.players[p].selected_weapon.take_damage(damage=5)
                self.players[p].add_experience(exp=total_exp)
                if (result):
                    self.players[p].selected_weapon = None

