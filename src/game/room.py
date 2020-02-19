from game.cardinal_direction import Direction
from game.item_type import Type
from game.door import Door
import random, math
from pyglet.sprite import Sprite
from pyglet import image
from pyglet import clock
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
    
    def intersecting_item(self, playerX, playerY):
        for entity in self.entities:
            if (type(entity) is Item):
                result = (math.floor(math.fabs(entity.x - playerX)) == 0 and math.floor(math.fabs(entity.y - playerY)) == 0)
                if (result):
                    return entity
        return None
    
    def add_entities(self):
        rand_num = random.randint(1, 100)
        if (rand_num > 40):
            to_add = Item(backX=self.startX, backY=self.startY, this_room=self)
            self.entities.append(to_add)
        if (rand_num > 60):
            to_add = Item(backX=self.startX, backY=self.startY, this_room=self)
            self.entities.append(to_add)
        if (rand_num > 80):
            to_add = Item(backX=self.startX, backY=self.startY, this_room=self)
            self.entities.append(to_add)
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
            
    def update(self, dt, playerX, playerY) -> int:
        total_damage = 0
        for entity in self.entities:
            if (type(entity) is Monster):
                total_damage = total_damage + entity.update(dt, player_x=playerX, player_y=playerY)
        return total_damage
    
    def player_attack(self, damage, playerX, playerY):
        for entity in self.entities:
            if (type(entity) is Monster):
                result = math.floor(math.fabs(entity.x - playerX)) == 0 and math.floor(math.fabs(entity.y - playerY)) == 0
                if (result):
                    entity.take_damage(dmg=damage)
            
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
    
    slime_standing = image.load('images/SlimeNSStanding.png')
    slime_NS_moving = image.load_animation('images/SlimeNS.gif')
    slime_east_moving = image.load_animation('images/SlimeEast.gif')
    slime_west_moving = image.load_animation('images/SlimeWest.gif')
    
    skeleton_east_standing = image.load('images/SkeletonEastStanding.png')
    skeleton_north_standing = image.load('images/SkeletonNorthStanding.png')
    skeleton_south_standing = image.load('images/SkeletonSouthStanding.png')
    skeleton_west_standing = image.load('images/SkeletonWestStanding.png')
    skeletont_east_moving = image.load_animation('images/SkeletonEast.gif', None, None)
    skeleton_north_moving = image.load_animation('images/SkeletonNorth.gif', None, None)
    skeleton_south_moving = image.load_animation('images/SkeletonSouth.gif', None, None)
    skeleton_west_moving = image.load_animation('images/SkeletonWest.gif', None, None)
    skeletont_east_attack = image.load_animation('images/SkeletonAEast.gif', None, None)
    skeleton_north_attack = image.load_animation('images/SkeletonANorth.gif', None, None)
    skeleton_south_attack = image.load_animation('images/SkeletonASouth.gif', None, None)
    skeleton_west_attack = image.load_animation('images/SkeletonAWest.gif', None, None)

    def __init__(self, backgroundX, backgroundY, this_room):
        super().__init__(img=Monster.bat_south_standing)
        self.startX = backgroundX
        self.startY = backgroundY
        self.next_coord = None
        self.curr_room = this_room
        self.standing_img_east = None
        self.standing_img_north = None
        self.standing_img_south = None
        self.standing_img_west = None
        self.moving_img_east = None
        self.moving_img_north = None
        self.moving_img_south = None
        self.moving_img_west = None
        self.attacking_img_east = None
        self.attacking_img_north = None
        self.attacking_img_south = None
        self.attacking_img_west = None
        self.health = None
        self.speed = None
        self.attack = None
        self.sight = None
        self.is_moving = False
        self.is_transfer_moving = False
        self.is_attacking = False
        self.is_dead = False
        self.facing = Direction.SOUTH
        self.pick_random_monster()
        self.pick_random_location()
        
    def pick_random_monster(self):
        rand_num = random.randint(0, 4)
        if (rand_num <= 1):
            self.standing_img_south = Monster.bat_south_standing
            self.moving_img_south = Monster.bat_south_moving
            self.standing_img_east = Monster.bat_east_standing
            self.moving_img_east = Monster.bat_east_moving
            self.standing_img_north = Monster.bat_north_standing
            self.moving_img_north = Monster.bat_north_moving
            self.standing_img_west = Monster.bat_west_standing
            self.moving_img_west = Monster.bat_west_moving
            self.attacking_img_east = Monster.bat_east_moving
            self.attacking_img_north = Monster.bat_north_moving
            self.attacking_img_south = Monster.bat_south_moving
            self.attacking_img_west = Monster.bat_west_moving
            self.health = 10
            self.speed = 240
            self.attack = 5
            self.sight = 4
        elif (rand_num <= 3):
            self.standing_img_south = Monster.slime_standing
            self.moving_img_south = Monster.slime_NS_moving
            self.standing_img_east = Monster.slime_standing
            self.moving_img_east = Monster.slime_east_moving
            self.standing_img_north = Monster.slime_standing
            self.moving_img_north = Monster.slime_NS_moving
            self.standing_img_west = Monster.slime_standing
            self.moving_img_west = Monster.slime_west_moving
            self.attacking_img_east = Monster.slime_east_moving
            self.attacking_img_north = Monster.slime_NS_moving
            self.attacking_img_south = Monster.slime_NS_moving
            self.attacking_img_west = Monster.slime_west_moving
            self.health = 20
            self.speed = 80
            self.attack = 10
            self.sight = 3
        else:
            self.standing_img_south = Monster.skeleton_south_standing
            self.moving_img_south = Monster.skeleton_south_moving
            self.standing_img_east = Monster.skeleton_east_standing
            self.moving_img_east = Monster.skeletont_east_moving
            self.standing_img_north = Monster.skeleton_north_standing
            self.moving_img_north = Monster.skeleton_north_moving
            self.standing_img_west = Monster.skeleton_west_standing
            self.moving_img_west = Monster.skeleton_west_moving
            self.attacking_img_east = Monster.skeletont_east_attack
            self.attacking_img_north = Monster.skeleton_north_attack
            self.attacking_img_south = Monster.skeleton_south_attack
            self.attacking_img_west = Monster.skeleton_west_attack
            self.health = 50
            self.speed = 120
            self.attack = 20
            self.sight = 6
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
        
    def take_damage(self, dmg):
        self.color = (128, 0, 0)
        clock.schedule_once(self.revert_color, 0.25)
        self.health = self.health - dmg
        if (self.health <= 0):
            self.is_dead = True
            
    def revert_color(self, dt):
        self.color = (255, 255, 255)
            
    def move_east(self, dt):
        if (self.x < self.next_coord):
            self.x = self.x + (self.speed * dt)
        else:
            self.x = self.next_coord
            clock.unschedule(self.move_east)
            self.is_moving = False
            self.is_transfer_moving = True

    def move_west(self, dt):
        if (self.x > self.next_coord):
            self.x = self.x - (self.speed * dt)
        else:
            self.x = self.next_coord
            clock.unschedule(self.move_west)
            self.is_moving = False
            self.is_transfer_moving = True

    def move_south(self, dt):
        if (self.y > self.next_coord):
            self.y = self.y - (self.speed * dt)
        else:
            self.y = self.next_coord
            clock.unschedule(self.move_south)
            self.is_moving = False
            self.is_transfer_moving = True

    def move_north(self, dt):
        if (self.y < self.next_coord):
            self.y = self.y + (self.speed * dt)
        else:
            self.y = self.next_coord
            clock.unschedule(self.move_north)
            self.is_moving = False
            self.is_transfer_moving = True
            
    def move_block(self, playerX, playerY):
        dif_x = self.x - playerX
        dif_y = self.y - playerY
        if (math.fabs(dif_x) >= math.fabs(dif_y)):
            if (dif_x < 0):
                if ((not self.is_transfer_moving) or self.facing != Direction.EAST):
                    self.image = self.moving_img_east
                self.facing = Direction.EAST
                self.next_coord = self.x + 40
                clock.schedule_interval(self.move_east, 1/60.0)
            else:
                if ((not self.is_transfer_moving) or self.facing != Direction.WEST):
                    self.image = self.moving_img_west
                self.facing = Direction.WEST
                self.next_coord = self.x - 40
                clock.schedule_interval(self.move_west, 1/60.0)
        else:
            if (dif_y < 0):
                if ((not self.is_transfer_moving) or self.facing != Direction.NORTH):
                    self.image = self.moving_img_north
                self.facing = Direction.NORTH
                self.next_coord = self.y + 40
                clock.schedule_interval(self.move_north, 1/60.0)
            else:
                if ((not self.is_transfer_moving) or self.facing != Direction.SOUTH):
                    self.image = self.moving_img_south
                self.facing = Direction.SOUTH
                self.next_coord = self.y - 40
                clock.schedule_interval(self.move_south, 1/60.0)
                
    def return_to_standing(self, dt):
        if (self.facing == Direction.EAST):
            self.image = self.standing_img_east
        elif (self.facing == Direction.WEST):
            self.image = self.standing_img_west
        elif (self.facing == Direction.NORTH):
            self.image = self.standing_img_north
        else:
            self.image = self.standing_img_south
            
    def set_attacking_img(self):
        if (self.facing == Direction.EAST):
            self.image = self.attacking_img_east
        elif (self.facing == Direction.WEST):
            self.image = self.attacking_img_west
        elif (self.facing == Direction.NORTH):
            self.image = self.attacking_img_north
        else:
            self.image = self.attacking_img_south
            
    def face_player(self, playerX, playerY):
        dif_x = self.x - playerX
        dif_y = self.y - playerY
        if (dif_x < 0):
            self.facing = Direction.EAST
        elif (dif_x > 0):
            self.facing = Direction.WEST
        elif (dif_y > 0):
            self.facing = Direction.SOUTH
        else:
            self.facing = Direction.NORTH
            
    def done_attacking(self, dt):
        self.is_attacking = False

    def update(self, dt, player_x, player_y) -> int:
        dif_x = math.fabs(self.x - player_x) / 40
        dif_y = math.fabs(self.y - player_y) / 40
        distance = dif_x + dif_y
        if ((distance <= self.sight) and (not self.is_moving) and (distance > 1)):
            self.is_transfer_moving = False
            self.is_moving = True
            self.move_block(playerX=player_x, playerY=player_y)
            if (self.is_dead):
                clock.unschedule(self.return_to_standing)
                clock.unschedule(self.done_attacking)
                clock.unschedule(self.revert_color)
                self.remove_self()
            return 0
        elif (distance <= 1 and (not self.is_attacking)):
            self.is_transfer_moving = False
            self.return_to_standing(dt=0)
            self.face_player(playerX=player_x, playerY=player_y)
            self.is_attacking = True
            self.set_attacking_img()
            clock.schedule_once(self.return_to_standing, self.image.get_duration())
            clock.schedule_once(self.done_attacking, 1)
            if (self.is_dead):
                clock.unschedule(self.return_to_standing)
                clock.unschedule(self.done_attacking)
                clock.unschedule(self.revert_color)
                self.remove_self()
            return self.attack
        else:
            if (self.is_transfer_moving):
                self.is_transfer_moving = False
                self.return_to_standing(dt=0)
            if (self.is_dead):
                clock.unschedule(self.return_to_standing)
                clock.unschedule(self.done_attacking)
                clock.unschedule(self.revert_color)
                self.remove_self()
            return 0
        
'''
Created on Feb 18, 2020

@author: Wyatt Muller

A random dungeon item.
'''
class Item(Sprite):
    
    sword = image.load('images/IronSwordGround.png')
    helmet = image.load('images/IronHelmetGround.png')
    chestpiece = image.load('images/IronChestpieceGround.png')
    leggings = image.load('images/IronLeggingsGround.png')
    hermes = image.load('images/HermesBootsGround.png')
    torch = image.load('images/TorchGround.png')
    potion = image.load('images/PotionGround.png')
    
    def __init__(self, backX, backY, this_room):
        super().__init__(img=Item.sword)
        self.startX = backX
        self.startY = backY
        self.curr_room = this_room
        self.pick_random_location()
        self.item_enum = None
        self.pick_random_item()
        
    def pick_random_location(self):
            rand_x = (random.randint(0, 24) * 40) + self.startX
            rand_y = (random.randint(0, 24) * 40) + self.startY
            while (self.curr_room.is_entity(aX=rand_x, aY=rand_y)):
                rand_x = (random.randint(0, 24) * 40) + self.startX
                rand_y = (random.randint(0, 24) * 40) + self.startY
            self.x = rand_x
            self.y = rand_y
            
    def pick_random_item(self):
        rand_num = random.randint(1, 15)
        if (rand_num <= 3):
            self.item_enum = Type.Weapon
            self.image = Item.sword
        elif (rand_num <= 6):
            self.item_enum = Type.Helmet
            self.image = Item.helmet
        elif (rand_num <= 9):
            self.item_enum = Type.Chestpiece
            self.image = Item.chestpiece
        elif (rand_num <= 12):
            self.item_enum = Type.Leggings
            self.image = Item.leggings
        elif (rand_num == 13):
            self.item_enum = Type.Footwear
            self.image = Item.hermes
        elif (rand_num == 14):
            self.item_enum = Type.Torch
            self.image = Item.torch
        else:
            self.item_enum = Type.Potion
            self.image = Item.potion
            
    def remove_self(self):
        self.delete()
        self.curr_room.entities.remove(self)
