from pyglet.sprite import Sprite
from pyglet import image
from pyglet import clock
from game.cardinal_direction import Direction
'''
Created on Feb 11, 2020

@author: Wyatt Muller

The player's sprite
'''

class Player(Sprite):
    
    north_standing_img = image.load('images/PlayerNorthStanding.png')
    east_standing_img = image.load('images/PlayerEastStanding.png')
    south_standing_img = image.load('images/PlayerSouthStanding.png')
    west_standing_img = image.load('images/PlayerWestStanding.png')
    
    north_animation = image.load_animation('images/PlayerNorth.gif', None, None)
    east_animation = image.load_animation('images/PlayerEast.gif', None, None)
    south_animation = image.load_animation('images/PlayerSouth.gif', None, None)
    west_animation = image.load_animation('images/PlayerWest.gif', None, None)

    def __init__(self, given_name, backgroundX, backgroundY):
        super().__init__(img=Player.south_standing_img)
        self.name = given_name
        self.x = backgroundX + 480
        self.y = backgroundY + 480
        self.nextBoxCoord = 0
        self.level = 0
        self.room_number = 0
        self.life = Life(backX=backgroundX, backY=backgroundY)
        self.defense = 0
        self.speed = 240
        self.visibility = 0
        self.player_inventory = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.inventory_rows = 2
        self.facing = Direction.SOUTH
        self.is_moving = False
        self.queued_direction = None
        
    def add_to_inventory(self, to_add):
        for i in range(Player.inventory_rows):
            for j in range(5):
                if (Player.player_inventory[i][j] == 0):
                    Player.player_inventory[i][j] = to_add
                    return
                
    def update(self, dt):
        if (self.facing == Direction.SOUTH):
            self.y = self.y - (self.speed * dt)
        elif (self.facing == Direction.WEST):
            self.x = self.x - (self.speed * dt)
        elif (self.facing == Direction.NORTH):
            self.y = self.y + (self.speed * dt)
        else:
            self.x = self.x + (self.speed * dt)
        
    def change_direction(self, direc):
        self.facing = direc
        if (direc == Direction.NORTH):
            self.image = Player.north_standing_img
        elif (direc == Direction.EAST):
            self.image = Player.east_standing_img
        elif (direc == Direction.SOUTH):
            self.image = Player.south_standing_img
        else:
            self.image = Player.west_standing_img
            
    def start_moving(self):
        clock.schedule_interval(self.update, 1/60.0)
        if (self.facing == Direction.SOUTH):
            self.image = Player.south_animation
        elif (self.facing == Direction.WEST):
            self.image = Player.west_animation
        elif (self.facing == Direction.NORTH):
            self.image = Player.north_animation
        else:
            self.image = Player.east_animation
        self.is_moving = True
        
    def stop_moving(self):
        clock.unschedule(self.update)
        if (self.facing == Direction.SOUTH):
            self.image = Player.south_standing_img
        elif (self.facing == Direction.WEST):
            self.image = Player.west_standing_img
        elif (self.facing == Direction.NORTH):
            self.image = Player.north_standing_img
        else:
            self.image = Player.east_standing_img
        self.is_moving = False
        
    #Returns if dead
    def change_life(self, change) -> bool:
        self.life.change_health(amount=change)
        return self.life.life_array[0].life == 0
    
    def increase_life_max(self):
        self.life.add_heart()
        
    def draw(self):
        Sprite.draw(self)
        self.life.draw()
        
class Life():
    
    def __init__(self, backX, backY):
        self.life_array = []
        self.startX = backX
        self.startY = backY
        for i in range(5):
            self.add_heart()
        
    def add_heart(self):
        to_add = Heart(backgroundX=self.startX, backgroundY=self.startY)
        num_hearts = len(self.life_array)
        to_add.x = to_add.x - (20 * num_hearts)
        to_add.decrease_scale(20)
        self.life_array.append(to_add)
        self.change_health(20)
        
    def change_health(self, amount):
        if (amount < 0):
            amount = -amount
            for i in range(len(self.life_array)):
                inverse = len(self.life_array) - (i + 1)
                curr_heart = self.life_array[inverse]
                amount = curr_heart.decrease_scale(change=amount)
        elif (amount > 0):
            for i in range(len(self.life_array)):
                curr_heart = self.life_array[i]
                amount = curr_heart.increase_scale(change=amount)
                
    def draw(self):
        for heart in self.life_array:
            heart.draw()
        
class Heart(Sprite):
        
    heart_img = image.load('images/Heart.png')
    heart_img.anchor_x = heart_img.width // 2
    heart_img.anchor_y = heart_img.height // 2
        
    def __init__(self, backgroundX, backgroundY):
        super().__init__(img=Heart.heart_img)
        self.x = backgroundX + 970
        self.y = backgroundY + 970
        self.life = 20
        
    def decrease_scale(self, change) -> int:
        if (change >= self.life):
            remainder = change - self.life
            self.life = 0
            self.scale = 0
            return remainder
        else:
            self.life = self.life - change
            self.scale = (self.life / 20)
            return 0
        
    def increase_scale(self, change) -> int:
        remainder = 20 - self.life
        if (change <= remainder):
            self.life = self.life + change
            self.scale = (self.life / 20)
            return 0
        else:
            self.life = 20
            self.scale = 1
            return change - remainder