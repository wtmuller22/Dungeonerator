from pyglet.sprite import Sprite
from pyglet import image
from pyglet import clock
from pyglet.text import Label
from game.cardinal_direction import Direction
from game.item_type import Type
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
        self.player_inventory = Inventory(backX=backgroundX, backY=backgroundY)
        self.facing = Direction.SOUTH
        self.is_moving = False
        self.queued_direction = None
        self.selected_weapon = None
        self.selected_helmet = None
        self.selected_chestpiece = None
        self.selected_leggings = None
        self.selected_footwear = None
        self.selected_torch = None
        
    def add_to_inventory(self, to_add) -> bool:
        return self.player_inventory.add(obj=to_add)
                
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
    
    def fade(self):
        clock.schedule_interval(self.decrease_opacity, 1/60)
        
    def decrease_opacity(self, dt):
        if (self.opacity >= 2):
            self.opacity = self.opacity - 2
        else:
            self.opacity = 0
            clock.unschedule(self.decrease_opacity)
            
    def draw_inventory(self):
        self.player_inventory.draw()

    def change_highlight(self, direc):
        self.player_inventory.update_highlight(direction=direc)

    def toggle_select_highlight(self):
        current_slot = self.player_inventory.get_curr_slot()
        slot_type = current_slot.get_item_type()
        if (not slot_type is None):
            if (slot_type == Type.Weapon):
                if (not self.selected_weapon is None):
                    self.selected_weapon.toggle_select()
                self.selected_weapon = current_slot
                self.selected_weapon.toggle_select()
            elif (slot_type == Type.Helmet):
                if (not self.selected_helmet is None):
                    self.selected_helmet.toggle_select()
                self.selected_helmet = current_slot
                self.selected_helmet.toggle_select()
            elif (slot_type == Type.Chestpiece):
                if (not self.selected_chestpiece is None):
                    self.selected_chestpiece.toggle_select()
                self.selected_chestpiece = current_slot
                self.selected_chestpiece.toggle_select()
            elif (slot_type == Type.Leggings):
                if (not self.selected_leggings is None):
                    self.selected_leggings.toggle_select()
                self.selected_leggings = current_slot
                self.selected_leggings.toggle_select()
            elif (slot_type == Type.Footwear):
                if (not self.selected_footwear is None):
                    self.selected_footwear.toggle_select()
                self.selected_footwear = current_slot
                self.selected_footwear.toggle_select()
            else:
                if (not self.selected_torch is None):
                    self.selected_torch.toggle_select()
                self.selected_torch = current_slot
                self.selected_torch.toggle_select()
        
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
        
class Inventory():
    
    def __init__(self, backX, backY):
        self.array = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.title = Label("Inventory",
                              font_name='Times New Roman',
                              font_size=56,
                              x=backX + 500,
                              y=backY + 750,
                              color=(135, 135, 135, 128),
                              align='center',
                              anchor_x='center',
                              anchor_y='center')
        self.startX = backX
        self.startY = backY
        self.fill_with_slots()
        self.highlighted_x = 0
        self.highlighted_y = 0
        self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
        
    def fill_with_slots(self):
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                self.array[i][j] = Slot(aX=(self.startX + 200 + (j * 120)), aY=(self.startY + 380 - (i * 120)))
        
    def add(self, obj) -> bool:
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                if (self.array[i][j].item is None):
                    self.array[i][j].item = obj
                    return True
        return False
    
    def update_highlight(self, direction):
        if (direction == Direction.NORTH):
            if (self.highlighted_y > 0):
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
                self.highlighted_y = self.highlighted_y - 1
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
        elif (direction == Direction.EAST):
            if (self.highlighted_x < 4):
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
                self.highlighted_x = self.highlighted_x + 1
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
        elif (direction == Direction.SOUTH):
            if (self.highlighted_y < (len(self.array) - 1)):
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
                self.highlighted_y = self.highlighted_y + 1
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
        else:
            if (self.highlighted_x > 0):
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
                self.highlighted_x = self.highlighted_x - 1
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
                
    def get_curr_slot(self):
        return self.array[self.highlighted_y][self.highlighted_x]
        
    def draw(self):
        self.title.draw()
        for row in self.array:
            for slot in row:
                slot.draw()
        
class Slot(Sprite):
    
    empty = image.load('images/EmptySlot.png')
    selected = image.load('images/SelectedSlot.png')
    highlighted = image.load('images/HighlightedSlot.png')
    highlighted_selected = image.load('images/HighlightedSelectedSlot.png')
    
    def __init__(self, aX, aY):
        super().__init__(img=Slot.empty)
        self.x = aX
        self.y = aY
        self.opacity = 192
        self.item = None
        self.is_selected = False
        self.is_highlighted = False
        
    def toggle_select(self):
        self.is_selected = not self.is_selected
        if (self.is_selected):
            self.image = Slot.highlighted_selected
        else:
            if (self.is_highlighted):
                self.image = Slot.highlighted
            else:
                self.image = Slot.empty
            
    def toggle_highlight(self):
        self.is_highlighted = not self.is_highlighted
        if (self.is_highlighted):
            if (self.is_selected):
                self.image = Slot.highlighted_selected
            else:
                self.image = Slot.highlighted
        else:
            if (self.is_selected):
                self.image = Slot.selected
            else:
                self.image = Slot.empty
                
    def break_item(self):
        self.item = None
        self.toggle_select()
        
    def get_item_type(self) -> Type:
        if (self.item is None):
            return None
            
    def draw(self):
        Sprite.draw(self)
        if (not self.item is None):
            self.item.draw()
        