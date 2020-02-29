from pyglet.sprite import Sprite
from pyglet import image
from pyglet import clock
from pyglet.text import Label
from game.cardinal_direction import Direction
from game.item_type import Type
import random, math
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

    def __init__(self, given_name, backgroundX, backgroundY, darkness):
        super().__init__(img=Player.south_standing_img)
        self.name = given_name
        self.x = backgroundX + 480
        self.y = backgroundY + 480
        self.nextBoxCoord = 0
        self.level = 0
        self.room_number = 0
        self.life = Life(backX=backgroundX, backY=backgroundY)
        self.experience = Experience(backX=backgroundX, backY=backgroundY)
        self.next_up_stat = 0
        self.defense = 1
        self.speed = 240
        self.attack = 0
        self.player_inventory = Inventory(backX=backgroundX, backY=backgroundY, the_player=self)
        self.facing = Direction.SOUTH
        self.is_moving = False
        self.scheduled_moving = False
        self.is_attacking = False
        self.queued_direction = None
        self.selected_weapon = None
        self.selected_helmet = None
        self.selected_chestpiece = None
        self.selected_leggings = None
        self.selected_footwear = None
        self.selected_torch = None
        self.attack_sprite = Attack()
        self.visibility = darkness
        self.add_to_inventory(to_add=Type.Torch)
        
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
        if (not self.selected_footwear is None):
            result = self.selected_footwear.take_damage(damage=1/60.0)
            if (result):
                self.selected_footwear = None
        
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
        self.life.change_health(amount=change, defense=self.defense)
        if (change < 0):
            if (not self.selected_chestpiece is None):
                result = self.selected_chestpiece.take_damage(damage=(-1 * change))
                if (result):
                    self.selected_chestpiece = None
            if (not self.selected_helmet is None):
                result = self.selected_helmet.take_damage(damage=(-1 * change))
                if (result):
                    self.selected_helmet = None
            if (not self.selected_leggings is None):
                result = self.selected_leggings.take_damage(damage=(-1 * change))
                if (result):
                    self.selected_leggings = None
        return self.life.life_array[0].life == 0
    
    def increase_life_max(self):
        self.life.add_heart()
        
    def increase_inventory_max(self):
        self.player_inventory.add_slot()
        
    def add_experience(self, exp):
        result = self.experience.add_exp(amount=exp)
        for i in range(result):
            self.stat_boost()
            
    def stat_boost(self):
        if (self.next_up_stat == 0):
            self.next_up_stat = 1
            self.defense = self.defense + 0.1
        elif (self.next_up_stat == 1):
            self.next_up_stat = 2
            self.speed = self.speed + 10
        elif (self.next_up_stat == 2):
            self.next_up_stat = 3
            self.increase_inventory_max()
        else:
            self.next_up_stat = 0
            self.increase_life_max()
        
    def draw(self):
        Sprite.draw(self)
        self.life.draw()
        self.experience.draw()
        if (self.is_attacking):
            self.attack_sprite.update_self(player_x=self.x, player_y=self.y, direction=self.facing)
            self.attack_sprite.draw()
            
    def stop_attack(self, dt):
        self.is_attacking = False
    
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
        
    def discard_item(self):
        self.player_inventory.discard_item()

    def change_highlight(self, direc):
        self.player_inventory.update_highlight(direction=direc)

    def toggle_select_highlight(self):
        current_slot = self.player_inventory.get_curr_slot()
        slot_type = current_slot.get_item_type()
        if (not slot_type is None):
            if (slot_type == Type.Weapon):
                if (not self.selected_weapon is None):
                    self.selected_weapon.toggle_select()
                if (self.selected_weapon is None or not (current_slot.x == self.selected_weapon.x and current_slot.y == self.selected_weapon.y)):
                    self.selected_weapon = current_slot
                    self.attack = self.selected_weapon.item.attack_strength_defense
                    self.selected_weapon.toggle_select()
                else:
                    self.selected_weapon = None
                    self.attack = 0
            elif (slot_type == Type.Helmet):
                if (not self.selected_helmet is None):
                    self.defense = self.defense - self.selected_helmet.item.attack_strength_defense
                    self.selected_helmet.toggle_select()
                if (self.selected_helmet is None or not (current_slot.x == self.selected_helmet.x and current_slot.y == self.selected_helmet.y)):
                    self.selected_helmet = current_slot
                    self.defense = self.defense + self.selected_helmet.item.attack_strength_defense
                    self.selected_helmet.toggle_select()
                else:
                    self.selected_helmet = None
            elif (slot_type == Type.Chestpiece):
                if (not self.selected_chestpiece is None):
                    self.defense = self.defense - self.selected_chestpiece.item.attack_strength_defense
                    self.selected_chestpiece.toggle_select()
                if (self.selected_chestpiece is None or not (current_slot.x == self.selected_chestpiece.x and current_slot.y == self.selected_chestpiece.y)):
                    self.selected_chestpiece = current_slot
                    self.defense = self.defense + self.selected_chestpiece.item.attack_strength_defense
                    self.selected_chestpiece.toggle_select()
                else:
                    self.selected_chestpiece = None
            elif (slot_type == Type.Leggings):
                if (not self.selected_leggings is None):
                    self.defense = self.defense - self.selected_leggings.item.attack_strength_defense
                    self.selected_leggings.toggle_select()
                if (self.selected_leggings is None or not (current_slot.x == self.selected_leggings.x and current_slot.y == self.selected_leggings.y)):
                    self.selected_leggings = current_slot
                    self.defense = self.defense + self.selected_leggings.item.attack_strength_defense
                    self.selected_leggings.toggle_select()
                else:
                    self.selected_leggings = None
            elif (slot_type == Type.Footwear):
                if (not self.selected_footwear is None):
                    self.speed = self.speed - self.selected_footwear.item.attack_strength_defense
                    self.selected_footwear.toggle_select()
                if (self.selected_footwear is None or not (current_slot.x == self.selected_footwear.x and current_slot.y == self.selected_footwear.y)):
                    self.selected_footwear = current_slot
                    self.speed = self.speed + self.selected_footwear.item.attack_strength_defense
                    self.selected_footwear.toggle_select()
                else:
                    self.selected_footwear = None
            elif (slot_type == Type.Torch):
                if (not self.selected_torch is None):
                    self.visibility.scale = self.visibility.scale - self.selected_torch.item.attack_strength_defense
                    self.visibility.update_coords(aX=(self.x + 20), aY=(self.y + 20))
                    self.selected_torch.toggle_select()
                if (self.selected_torch is None or not (current_slot.x == self.selected_torch.x and current_slot.y == self.selected_torch.y)):
                    self.selected_torch = current_slot
                    self.visibility.scale = self.visibility.scale + self.selected_torch.item.attack_strength_defense
                    self.visibility.update_coords(aX=(self.x + 20), aY=(self.y + 20))
                    self.selected_torch.toggle_select()
                else:
                    self.selected_torch = None
            else:
                current_slot.toggle_select()
                
class Experience():
    
    experience_bar = image.load('images/ExperienceBar.png')
    experience_bar.anchor_x = experience_bar.width // 2
    experience_bar.anchor_y = experience_bar.height // 2
    experience_green = image.load('images/Experience.png')
    experience_green.anchor_x = experience_green.width // 2
    experience_green.anchor_y = experience_green.height // 2
    
    def __init__(self, backX, backY):
        self.startX = backX
        self.startY = backY
        self.bar = Sprite(img=Experience.experience_bar, x=backX + 930, y=backY + 940)
        self.exp = Sprite(img=Experience.experience_green, x=backX + 930, y=backY + 940)
        self.exp.scale = 0
        self.total_exp = 0
        
    def draw(self):
        self.exp.draw()
        self.bar.draw()
        
    def add_exp(self, amount) -> int:
        self.total_exp = self.total_exp + amount
        amount_ups = 0
        while (self.total_exp >= 100):
            self.total_exp = self.total_exp - 100
            amount_ups = amount_ups + 1
        self.exp.scale = (self.total_exp / 100)
        return amount_ups

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
        self.change_health(20, 0)
        
    def change_health(self, amount, defense):
        if (amount < 0):
            amount = -amount
            amount = amount / defense
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
    
    def __init__(self, backX, backY, the_player):
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
        self.this_player = the_player
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
                    self.array[i][j].item = Item(item_enum=obj, aX=(self.startX + 210 + (j * 120)), aY=(self.startY + 390 - (i * 120)), frame=self.array[i][j], a_player=self.this_player)
                    return True
        return False
    
    def add_slot(self):
        if (len(self.array[len(self.array) - 1]) == 5):
            self.array.append([])
        self.array[len(self.array) - 1].append(Slot(aX=(self.startX + 200 + (len(self.array[len(self.array) - 1]) * 120)), aY =(self.startY + 380 - ((len(self.array) - 1) * 120))))
    
    def update_highlight(self, direction):
        if (direction == Direction.NORTH):
            if (self.highlighted_y > 0):
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
                self.highlighted_y = self.highlighted_y - 1
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
        elif (direction == Direction.EAST):
            if (self.highlighted_x < len(self.array[self.highlighted_y]) - 1):
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
                self.highlighted_x = self.highlighted_x + 1
                self.array[self.highlighted_y][self.highlighted_x].toggle_highlight()
        elif (direction == Direction.SOUTH):
            if (self.highlighted_y < (len(self.array) - 1) and self.highlighted_x < len(self.array[self.highlighted_y + 1])):
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
    
    def discard_item(self):
        this_slot = self.get_curr_slot()
        if (not this_slot.item is None):
            if (this_slot.is_selected):
                this_slot.item.remove_effect()
            this_slot.break_item()
        
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
            if (self.item.type == Type.Torch):
                clock.schedule_interval(self.item.lose_light, 1)
            elif (self.item.type == Type.Potion):
                self.item.heal()
        else:
            if (self.is_highlighted):
                self.image = Slot.highlighted
            else:
                self.image = Slot.empty
            if ((not self.item is None) and self.item.type == Type.Torch):
                    clock.unschedule(self.item.lose_light)
            
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
        self.item.delete()
        self.item = None
        if (self.is_selected):
            self.toggle_select()
        
    def get_item_type(self) -> Type:
        if (self.item is None):
            return None
        else:
            return self.item.type
        
    def take_damage(self, damage) -> bool:
        return self.item.take_damage(dmg=damage)
            
    def draw(self):
        Sprite.draw(self)
        if (not self.item is None):
            self.item.draw()
        
class Item(Sprite):
    
    sword = image.load('images/IronSwordInventory.png')
    helmet = image.load('images/IronHelmetInventory.png')
    chestpiece = image.load('images/IronChestpieceInventory.png')
    leggings = image.load('images/IronLeggingsInventory.png')
    hermes = image.load('images/HermesBootsInventory.png')
    torch = image.load('images/TorchInventory.png')
    potion = image.load('images/PotionInventory.png')
    
    def __init__(self, item_enum, aX, aY, frame, a_player):
        super().__init__(img=Item.sword)
        self.attack_strength_defense = None
        self.durability_max = 100
        self.durability = 100
        self.type = item_enum
        self.x = aX
        self.y = aY
        self.slot = frame
        self.this_player = a_player
        self.cracks = Crack(aX=self.x, aY=self.y)
        self.rarity_img = Rarity(aX=self.x, aY=self.y)
        self.rarity = 0
        self.set_rarity()
        self.make_item(item_id=item_enum)
        
    def set_rarity(self):
        curr_level = self.this_player.level
        if (curr_level != 0):
            expansion_factor = 10.60683865
            phase_shift = -42.42735461
            first_threshold = (-50)*(math.atan(expansion_factor*curr_level + phase_shift) / (math.pi / 2)) + 50
            phase_shift = phase_shift - 4
            second_threshold = (-50)*(math.atan(expansion_factor*curr_level + phase_shift) / (math.pi / 2)) + 50
            phase_shift = phase_shift - 4
            third_threshold = (-50)*(math.atan(expansion_factor*curr_level + phase_shift) / (math.pi / 2)) + 50
            phase_shift = phase_shift - 4
            fourth_threshold = (-50)*(math.atan(expansion_factor*curr_level + phase_shift) / (math.pi / 2)) + 50
            rand_num = random.randint(1, 10000) / 100
            if (rand_num > fourth_threshold):
                self.rarity = 4
                self.rarity_img.image = Rarity.mythical
            elif (rand_num > third_threshold):
                self.rarity = 3
                self.rarity_img.image = Rarity.epic
            elif (rand_num > second_threshold):
                self.rarity = 2
                self.rarity_img.image = Rarity.rare
            elif (rand_num > first_threshold):
                self.rarity = 1
                self.rarity_img.image = Rarity.uncommon
        
    def make_item(self, item_id):
        if (self.rarity == 0):
            if (item_id == Type.Weapon):
                self.attack_strength_defense = random.randint(5, 10)
                self.image = Item.sword
            elif (item_id == Type.Helmet):
                self.attack_strength_defense = random.randint(3, 7) / 10
                self.image = Item.helmet
            elif (item_id == Type.Chestpiece):
                self.attack_strength_defense = random.randint(8, 12) / 10
                self.image = Item.chestpiece
            elif (item_id == Type.Leggings):
                self.attack_strength_defense = random.randint(3, 7) / 10
                self.image = Item.leggings
            elif (item_id == Type.Footwear):
                self.attack_strength_defense = random.randint(25, 50)
                self.image = Item.hermes
            elif (item_id == Type.Torch):
                self.attack_strength_defense = 3
                self.image = Item.torch
            else:
                self.attack_strength_defense = random.randint(15, 35)
                self.image = Item.potion
        elif (self.rarity == 1):
            if (item_id == Type.Weapon):
                self.attack_strength_defense = random.randint(15, 20)
                self.image = Item.sword
            elif (item_id == Type.Helmet):
                self.attack_strength_defense = random.randint(5, 9) / 10
                self.image = Item.helmet
            elif (item_id == Type.Chestpiece):
                self.attack_strength_defense = random.randint(10, 14) / 10
                self.image = Item.chestpiece
            elif (item_id == Type.Leggings):
                self.attack_strength_defense = random.randint(5, 9) / 10
                self.image = Item.leggings
            elif (item_id == Type.Footwear):
                self.attack_strength_defense = random.randint(50, 75)
                self.image = Item.hermes
            elif (item_id == Type.Torch):
                self.attack_strength_defense = 4
                self.image = Item.torch
            else:
                self.attack_strength_defense = random.randint(32, 52)
                self.image = Item.potion
            self.durability = 120
            self.durability_max = 120
        elif (self.rarity == 2):
            if (item_id == Type.Weapon):
                self.attack_strength_defense = random.randint(25, 30)
                self.image = Item.sword
            elif (item_id == Type.Helmet):
                self.attack_strength_defense = random.randint(7, 11) / 10
                self.image = Item.helmet
            elif (item_id == Type.Chestpiece):
                self.attack_strength_defense = random.randint(12, 16) / 10
                self.image = Item.chestpiece
            elif (item_id == Type.Leggings):
                self.attack_strength_defense = random.randint(7, 11) / 10
                self.image = Item.leggings
            elif (item_id == Type.Footwear):
                self.attack_strength_defense = random.randint(75, 100)
                self.image = Item.hermes
            elif (item_id == Type.Torch):
                self.attack_strength_defense = 5
                self.image = Item.torch
            else:
                self.attack_strength_defense = random.randint(49, 69)
                self.image = Item.potion
            self.durability = 140
            self.durability_max = 140
        elif (self.rarity == 3):
            if (item_id == Type.Weapon):
                self.attack_strength_defense = random.randint(35, 40)
                self.image = Item.sword
            elif (item_id == Type.Helmet):
                self.attack_strength_defense = random.randint(9, 13) / 10
                self.image = Item.helmet
            elif (item_id == Type.Chestpiece):
                self.attack_strength_defense = random.randint(14, 18) / 10
                self.image = Item.chestpiece
            elif (item_id == Type.Leggings):
                self.attack_strength_defense = random.randint(9, 13) / 10
                self.image = Item.leggings
            elif (item_id == Type.Footwear):
                self.attack_strength_defense = random.randint(100, 125)
                self.image = Item.hermes
            elif (item_id == Type.Torch):
                self.attack_strength_defense = 6.5
                self.image = Item.torch
            else:
                self.attack_strength_defense = random.randint(66, 86)
                self.image = Item.potion
            self.durability = 160
            self.durability_max = 160
        else:
            if (item_id == Type.Weapon):
                self.attack_strength_defense = random.randint(45, 50)
                self.image = Item.sword
            elif (item_id == Type.Helmet):
                self.attack_strength_defense = random.randint(11, 15) / 10
                self.image = Item.helmet
            elif (item_id == Type.Chestpiece):
                self.attack_strength_defense = random.randint(16, 20) / 10
                self.image = Item.chestpiece
            elif (item_id == Type.Leggings):
                self.attack_strength_defense = random.randint(11, 15) / 10
                self.image = Item.leggings
            elif (item_id == Type.Footwear):
                self.attack_strength_defense = random.randint(125, 150)
                self.image = Item.hermes
            elif (item_id == Type.Torch):
                self.attack_strength_defense = 8
                self.image = Item.torch
            else:
                self.attack_strength_defense = random.randint(83, 100)
                self.image = Item.potion
            self.durability = 180
            self.durability_max = 180
            
    def heal(self):
        self.this_player.change_life(change=self.attack_strength_defense)
        self.slot.break_item()
            
    def lose_light(self, dt):
        self.durability = self.durability - 1
        self.change_cracks()
        if (self.durability <= 0):
            clock.unschedule(self.lose_light)
            self.remove_effect()
            self.slot.break_item()
            
    def take_damage(self, dmg) -> bool:
        self.durability = self.durability - dmg
        self.change_cracks()
        if (self.durability <= 0):
            self.remove_effect()
            self.slot.break_item()
            return True
        return False
    
    def remove_effect(self):
        if (self.type == Type.Footwear):
            self.this_player.speed = self.this_player.speed - self.attack_strength_defense
            self.this_player.selected_footwear = None
        elif (self.type == Type.Torch):
            self.this_player.visibility.scale = self.this_player.visibility.scale - self.attack_strength_defense
            self.this_player.visibility.update_coords(aX=(self.this_player.x + 20), aY=(self.this_player.y + 20))
            self.this_player.selected_torch = None
        elif (self.type == Type.Chestpiece):
            self.this_player.defense = self.this_player.defense - self.attack_strength_defense
            self.this_player.selected_chestpiece = None
        elif (self.type == Type.Leggings):
            self.this_player.defense = self.this_player.defense - self.attack_strength_defense
            self.this_player.selected_leggings = None
        elif (self.type == Type.Helmet):
            self.this_player.defense = self.this_player.defense - self.attack_strength_defense
            self.this_player.selected_helmet = None
        elif (self.type == Type.Weapon):
            self.this_player.attack = 0
            self.this_player.selected_weapon = None
    
    def change_cracks(self):
        if (self.durability < (self.durability_max // 5)):
            self.cracks.image = Crack.stage_5
        elif (self.durability < 2 * (self.durability_max // 5)):
            self.cracks.image = Crack.stage_4
        elif (self.durability < 3 * (self.durability_max // 5)):
            self.cracks.image = Crack.stage_3
        elif (self.durability < 4 * (self.durability_max // 5)):
            self.cracks.image = Crack.stage_2
        else:
            self.cracks.image = Crack.stage_1
    
    def draw(self):
        self.rarity_img.draw()
        Sprite.draw(self)
        if (self.durability != self.durability_max):
            self.cracks.draw()
    
class Crack(Sprite):
    
    stage_1 = image.load('images/Crack1.png')
    stage_2 = image.load('images/Crack2.png')
    stage_3 = image.load('images/Crack3.png')
    stage_4 = image.load('images/Crack4.png')
    stage_5 = image.load('images/Crack5.png')
    
    def __init__(self, aX, aY):
        super().__init__(img=Crack.stage_1)
        self.x = aX
        self.y = aY
        self.opacity = 128
        
class Rarity(Sprite):
    
    common = image.load('images/Common.png')
    uncommon = image.load('images/Uncommon.png')
    rare = image.load('images/Rare.png')
    epic = image.load('images/Epic.png')
    mythical = image.load('images/Mythical.png')
    
    def __init__(self, aX, aY):
        super().__init__(img=Rarity.common)
        self.x = aX
        self.y = aY
        self.opacity = 64
    
class Attack(Sprite):
    
    attack_animation = image.load_animation('images/Attack.gif', None, None)
    
    def __init__(self):
        super().__init__(img=Attack.attack_animation)
        self.opacity = 128
        
    def update_self(self, player_x, player_y, direction):
        if (direction == Direction.NORTH):
            this_x = player_x
            this_y = player_y + 40
            self.update(x=this_x, y=this_y, rotation=0)
        elif (direction == Direction.EAST):
            this_x = player_x + 40
            this_y = player_y + 40
            self.update(x=this_x, y=this_y, rotation=90)
        elif (direction == Direction.SOUTH):
            this_x = player_x + 40
            this_y = player_y
            self.update(x=this_x, y=this_y, rotation=180)
        else:
            this_x = player_x
            this_y = player_y
            self.update(x=this_x, y=this_y, rotation=270)   
            
    def reset_animation(self):
        self.image = Attack.attack_animation     
