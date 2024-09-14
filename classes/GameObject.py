import time

import pygame.image
import pygame
import random
import math
import images
import copy
from classes import weapon, gameover

class GameObject():
    def __init__(self,game,x,y,w,h,image,visible):
        self.game=game
        self.screen = self.game.screen
        self.x=x
        self.y=y
        self.w=w
        self.h = h
        self.image=image
        self.image= pygame.transform.scale(self.image,(self.w,self.h))
        self.rect=pygame.Rect(x,y,w,h)
        self.game.objects.append(self)
        self.collision = False

    def render(self):
        self.x -= self.game.dx
        self.y -= self.game.dy
        # if type(self) == Chest:
        #     print(self.x,self.y)
        if self.x+self.w>=0 and self.x<=self.game.app.width:

            self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
            self.screen.blit(self.image,self.rect)

class Zombie(GameObject):
    def __init__(self, game,x,y,w,h,image_path,visible):
        super().__init__(game,x,y,w,h,image_path,visible)

        self.angle = 0

        self.health = 50
        self.color = (255, 105, 55)
        self.weapon = weapon.M4A1(game, self)

        self.gun_image = images.m4a1
        self.speed = 4
        self.combat_range = 500
        self.distance_to_player = 10000000
        self.break_damage = 50
        self.break_cooldown = 2
        self.break_clock = time.time()


        self.shoot_interval = 1500
        self.last_shot_time = pygame.time.get_ticks()

    def render_health_bar(self):
        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = self.x + (self.w - health_bar_width) // 2
        health_bar_y = self.y - 20
        pygame.draw.rect(self.screen, (100, 100, 100), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        current_health_width = int(health_bar_width * (self.health / 100))
        pygame.draw.rect(self.screen, (0, 200, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_interval:
            self.weapon.shoot()
            self.last_shot_time = current_time

    def render(self):
        if self.health > 0:
            self.x -= self.game.dx
            self.y -= self.game.dy
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            self.screen.blit(rotated_image, rotated_rect.topleft)
            rotated_gun = pygame.transform.rotate(self.gun_image, -math.degrees(self.angle))
            gun_length = self.gun_image.get_width() // 2
            offset_x = gun_length * math.cos(self.angle) * 1.5
            offset_y = gun_length * math.sin(self.angle) * 1.5
            gun_rect = rotated_gun.get_rect(center=(self.x + self.w // 2 + offset_x, self.y + self.h // 2 + offset_y))
            self.screen.blit(rotated_gun, gun_rect)

            # Render the health bar
            self.render_health_bar()

            if self.distance_to_player < self.combat_range:
                self.shoot()

        else:
            self.game.score += self.game.wave ** 2
            self.rect = None


class Player(GameObject):
    def __init__(self, game, x, y, w, h, image_path, visible):
        super().__init__(game, x, y, w, h, image_path, visible)
        self.angle = 0
        self.health = 100
        self.size = 25
        self.color = (255, 105, 55)
        self.relative_position = [0, 0]
        self.gameObjectPos = [x, y]
        self.gun_image = images.gun
        self.canMoveRight = True
        self.canMoveLeft = True
        self.canMoveUp = True
        self.canMoveDown = True
        self.isMovingItem = False
        self.to_ui = None
        self.from_ui = None
        self.isShooting = False
        self.last_damage_time = 0
        self.hunger = 70
        self.thirst = 100
        self.delta_hunger = 3
        self.delta_health = 0

    # def render_health_bar(self):
    #     health_bar_width = 100
    #     health_bar_height = 10
    #     health_bar_x = self.x + (self.w - health_bar_width) // 2
    #     health_bar_y = self.y - 20
    #     pygame.draw.rect(self.screen, (100, 100, 100), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    #     current_health_width = int(health_bar_width * (self.health / 100))
    #     pygame.draw.rect(self.screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

    def rotate_towards_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - (self.y + self.h//2), mouse_x - (self.x + self.w//2))

    def render(self):
        if self.health > 100:
            self.health = 100
        if self.health > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_damage_time >= 1000:
                self.image = pygame.transform.scale(images.player, (self.w, self.h))

            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            self.screen.blit(rotated_image, rotated_rect.topleft)

            selected_item = self.game.hotbar.items[self.game.hotbar.selected_slot]
            if isinstance(selected_item, weapon.Weapon):
                rotated_gun = pygame.transform.rotate(selected_item.image, -math.degrees(self.angle))
                gun_length = selected_item.image.get_width() // 2
                offset_x = gun_length * math.cos(self.angle) * 2.5
                offset_y = gun_length * math.sin(self.angle) * 2.5
                gun_rect = rotated_gun.get_rect(
                    center=(self.x + self.w // 2 + offset_x, self.y + self.h // 2 + offset_y))
                self.screen.blit(rotated_gun, gun_rect)
            #
            # self.render_health_bar()
        else:
            self.game.app.ui = gameover.GameOver(self.game.app)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = pygame.mouse.get_pos()
            if self.game.chest_ui is not None:
                if self.isMovingItem is False:
                    selected_ui = False
                    slot_num = 0
                    for slot_rect in self.game.chest_ui.slot_rects:
                        if slot_rect.collidepoint(click_pos):
                            print("slot ", slot_num, " selected")
                            selected_ui = True
                            break
                        slot_num += 1
                    if selected_ui is False:
                        slot_num = 0
                        for slot_rect in self.game.hotbar.slot_rects:
                            if slot_rect.collidepoint(click_pos):
                                print("slot ", slot_num, " selected")
                                selected_ui = True
                                break
                            slot_num += 1
                        if selected_ui:
                            self.from_ui = self.game.hotbar
                    else:
                        self.from_ui = self.game.chest_ui
                    if selected_ui:
                        self.from_ui.moved_item = slot_num
                        self.isMovingItem = True

                else:
                    slot_num = 0

                    slot_selected = False
                    for slot_rect in self.game.hotbar.slot_rects:
                        if slot_rect.collidepoint(click_pos):
                            print("slot ", slot_num, " selected")
                            slot_selected = True
                            break
                        slot_num += 1

                    if slot_selected is False:
                        slot_num = 0
                        for slot_rect in self.game.chest_ui.slot_rects:
                            if slot_rect.collidepoint(click_pos):
                                print("slot ", slot_num, " selected")
                                slot_selected = True
                                break
                            slot_num += 1
                        if slot_selected:
                            self.to_ui = self.game.chest_ui
                    else:
                        self.to_ui = self.game.hotbar

                    if slot_selected:
                        if self.to_ui.items[slot_num] is None:
                            self.to_ui.add_item(self.from_ui.items[self.from_ui.moved_item], slot_num)
                            print(self.from_ui.items[self.from_ui.moved_item])
                            if self.from_ui == self.game.chest_ui:
                                self.game.selected_chest.Items[self.from_ui.moved_item] = None
                            if self.to_ui == self.game.chest_ui:
                                self.game.selected_chest.Items[self.from_ui.moved_item] = self.from_ui.items[self.from_ui.moved_item]
                            self.from_ui.remove_item(self.from_ui.moved_item)
                            self.from_ui.moved_item = None
                            self.isMovingItem = False
                        else:
                            temp_item = self.from_ui.items[self.from_ui.moved_item]
                            self.from_ui.remove_item(self.from_ui.moved_item)
                            if self.from_ui == self.game.chest_ui:
                                self.game.selected_chest.Items[self.from_ui.moved_item] = self.to_ui.items[slot_num]
                            if self.to_ui == self.game.chest_ui:
                                self.game.selected_chest.Items[self.from_ui.moved_item] = self.to_ui.items[slot_num]
                            self.from_ui.add_item(self.to_ui.items[slot_num], self.from_ui.moved_item)
                            self.from_ui.moved_item = None
                            self.to_ui.add_item(temp_item, slot_num)
                            print(self.to_ui.items[slot_num])
                            self.isMovingItem = False

            else:
                selected_item = self.game.hotbar.items[self.game.hotbar.selected_slot]
                if isinstance(selected_item, weapon.Weapon):
                    if self.game.hotbar.items[self.game.hotbar.selected_slot].firemode == 0:
                        self.game.hotbar.items[self.game.hotbar.selected_slot].shoot()
                    else:
                        self.isShooting = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.isShooting:
                self.isShooting = False
                self.game.burst_shots = 0

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.pick_up_item()
            elif event.key == pygame.K_q:
                self.drop_item()
            elif event.key == pygame.K_r:
                selected_item = self.game.hotbar.items[self.game.hotbar.selected_slot]
                if isinstance(selected_item, weapon.Weapon):
                    selected_item.reload()
            elif event.key == pygame.K_b:
                selected_item = self.game.hotbar.items[self.game.hotbar.selected_slot]
                if isinstance(selected_item, weapon.Weapon):
                    if selected_item.firemode == 1:
                        selected_item.firemode = 2
                    elif selected_item.firemode == 2:
                        selected_item.firemode = 1
                    else:
                        print("Weapon does not support extra fire modes")

    def drop_item(self):
        selected_item = self.game.hotbar.items[self.game.hotbar.selected_slot]
        if selected_item:
            DroppedItem(self.game, self.x, self.y, 50, 50, selected_item.image, True, selected_item)
            self.game.hotbar.items[self.game.hotbar.selected_slot] = None

    def pick_up_item(self):
        for obj in self.game.objects:
            if isinstance(obj, DroppedItem) and self.rect.colliderect(obj.rect):
                self.equip_item(obj.item_instance)
                self.game.objects.remove(obj)

    def equip_item(self, item_instance):
        self.game.hotbar.add_item(item_instance, self.game.hotbar.selected_slot)

    def shoot(self):
        selected_item = self.game.hotbar.items[self.game.hotbar.selected_slot]
        if isinstance(selected_item, weapon.Weapon):
            selected_item.shoot()

    def reload(self):
        selected_item = self.game.hotbar.items[self.game.hotbar.selected_slot]
        if isinstance(selected_item, weapon.Weapon):
            selected_item.reload()
class Storm(GameObject):
    def __init__(self, game,x,y,w,h,image,visible):

        super().__init__(game,x,y,w,h,image,visible)
        self.speed=1
        self.dmg=10
        self.last_damage_time = pygame.time.get_ticks()
        self.head_image=pygame.image.load('Assets/burza (2).png')
        self.head_image = pygame.transform.scale(self.head_image, (self.w, self.h))
        self.first_image=pygame.image.load('Assets/burza (1).png')
        self.first_image = pygame.transform.scale(self.first_image, (self.w, self.h))

        self.second_image = pygame.image.load('Assets/burza (1).png')
        self.second_image = pygame.transform.scale(self.second_image, (self.w, self.h))
        self.is_moving = False
    def distance(self):
        self.right=self.x+self.w
        return self.game.player.x-self.right
    def move(self):
        if self.is_moving:
            ddx = self.speed
            if self.distance() < 100:
                ddx += 0
            elif self.distance() < 0:
                ddx += 0
            else:
                ddx += math.sqrt(self.distance() - 100) / 100
            self.x += ddx

    def render(self):

        self.x-=2*self.game.dx
        self.y-=2*self.game.dy
        if self.y+self.h<0:
            self.y=self.game.app.height
        if self.y>self.game.app.height:

            self.y=0 -self.h
        num_images = 10

        total_width = (num_images+1) * self.w
        self.rect = pygame.Rect(self.x - (num_images)*self.w, self.y, total_width, self.h)

        for i in range(num_images):
            offset_x = self.x - i * self.w
            if i==0:
                self.screen.blit(self.head_image, (offset_x, self.y))
            else:
                if i%2==0:

                    self.screen.blit(self.first_image, (offset_x, self.y))
                else:
                    self.screen.blit(self.second_image, (offset_x, self.y))
        #draw rect
        pygame.draw.rect(self.screen,(255,255,255),self.rect,2)

        self.damage()


    def damage(self):
        current_time = pygame.time.get_ticks()
        if self.rect.colliderect(self.game.player.rect) and current_time - self.last_damage_time >= 250:
            self.game.player.health-=self.dmg
            self.last_damage_time = current_time
            self.game.player.last_damage_time = current_time
            self.game.player.image = pygame.transform.scale(images.damagedplayer, (self.game.player.w, self.game.player.h))


class Chest(GameObject):
    def __init__(self, game, x, y, w, h, image_path, visible):
        super().__init__(game, x, y, w, h, image_path, visible)

        self.Items = [None] * 5
        self.CommonDrops = ["Glock 17", "Pump Action Shotgun", "Ammo Box"]
        self.UncommonDrops = ["M4A1", "Bolt Action Sniper", "Ammo Crate"]
        self.EpicDrops = ["MAC-10", "M1911 .45"]
        self.LegendaryDrops = ["Scar-H", "Desert Eagle", ".44 Magnum"]

        self.opened_image = images.chest_open
        self.open_image = pygame.transform.scale(self.opened_image, (self.w, self.h))

        self.collision = True
        self.opened = not self.game.pay_for_chest
        self.generateRandomItems()

    def render(self):
        if self.opened:
            self.image = self.open_image
        super().render()

    def generateRandomItems(self):
        weapon_classes = {
            "Glock 17": weapon.Glock17,
            "Pump Action Shotgun": weapon.PumpActionShotgun,
            "Ammo Box": weapon.AmmoBox,
            "M4A1": weapon.M4A1,
            "Bolt Action Sniper": weapon.BoltActionSniper,
            "Ammo Crate": weapon.AmmoCrate,
            "MAC-10": weapon.MAC10,
            "M1911 .45": weapon.M1911,
            "Scar-H": weapon.ScarH,
            "Desert Eagle": weapon.DesertEagle,
            ".44 Magnum": weapon.Magnum44
        }

        for i in range(random.randint(1, 5)):
            rarity = random.randint(0, 100)
            if rarity > 90:
                weapon_name = random.choice(self.LegendaryDrops)
            elif rarity > 75:
                weapon_name = random.choice(self.EpicDrops)
            elif rarity > 35:
                weapon_name = random.choice(self.UncommonDrops)
            else:
                weapon_name = random.choice(self.CommonDrops)

            self.Items[i] = weapon_classes[weapon_name](self.game, self.game.player)

class Tile(GameObject):
    def __init__(self, game, x, y, image_path):
        super().__init__(game, x, y, 48, 48, image_path, True)


class DroppedItem(GameObject):
    def __init__(self, game, x, y, w, h, image_path, visible, item_instance):
        super().__init__(game, x, y, w, h, image_path, visible)
        self.item_instance = item_instance
        self.collision = True

    def render(self):
        self.x -= self.game.dx
        self.y -= self.game.dy
        super().render()
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.item_instance.__class__.__name__, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (self.x, self.y - 20))
class Resource_Manager():
    def __init__(self,x,y,game,resources,images):
        self.game=game
        self.resources=resources
        self.collision=False
        self.game.objects.append(self)
        self.images=images
        self.x=x
        self.y=y
        self.texts=[]
        self.image_objects=[]
        offsety=40
        image_width=35
        offsetx=70
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        for r in range(0, len(self.resources)):

            # text = font.render(self.resources[r], True, (0,0,0))
            text = self.font.render(str(self.resources[r][1]), True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = (self.x+offsetx,self.y+offsety*(r)+offsety//2)
            self.texts.append([text,textRect])
            rect = pygame.Rect(self.x, self.y+offsety*(r), offsety, offsety)
            self.images[r]=pygame.transform.scale(self.images[r],(image_width,image_width))
            self.image_objects.append([self.images[r],rect])
    def update(self):
        for r in range(0, len(self.resources)):

            self.texts[r][0]= self.font.render(str(self.resources[r][1]), True, (0,0,0))


    # def render(self):
    #     self.update()
    #     for x in range(len(self.texts)):
    #         self.game.screen.blit(self.texts[x][0],self.texts[x][1])
    #         self.game.screen.blit(self.image_objects[x][0], self.image_objects[x][1])
class Bar:
    def __init__(self,game,x,y,w,h,color,value,max_value):
        self.game=game
        self.x=x
        self.w=w
        self.y=y
        self.h=h
        self.color=color
        self.max_value=max_value
        self.value=value
        self.collision=False
        self.game.objects.append(self)
        self.outline=2
    def render(self):
        self.x-=2*self.game.dx
        self.y-=2*self.game.dy
        pygame.draw.rect(self.game.screen,(0,0,0),pygame.Rect(self.x,self.y,self.w,self.h))
        pygame.draw.rect(self.game.screen, self.color, pygame.Rect(self.x+self.outline, self.y+self.outline, self.w*self.value//self.max_value-self.outline*2, self.h-self.outline*2))

class Resource():
    def __init__(self,game,x,y,resource,image,time,max):
        self.game=game
        self.x=x
        self.y=y
        self.resource=resource
        self.image=image
        self.time=time
        self.max=max
        self.value=0
        self.game.resources[(x,y)]=self
        self.tick=0
        offsety = 40
        image_width = 35
        offsetx = 70
        self.font = pygame.font.Font('fonts/main_font.ttf', 36)
        self.text = self.font.render(str(self.value), True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x + offsetx, self.y + offsety  + offsety // 2)
        self.rect = pygame.Rect(self.x, self.y + offsety, offsety, offsety)
        self.image = pygame.transform.scale(self.image, (image_width, image_width))
        print(x,y)
        self.offset_modx=+8
        self.offset_mody = -10
    def render(self):
        self.update()
        self.new_rect=self.rect.copy()
        self.new_rect.x-=self.game.player_x2-self.offset_modx
        self.new_rect.y -= self.game.player_y2-self.offset_mody
        self.new_textRect=self.textRect.copy()
        self.new_textRect.x -= self.game.player_x2-self.offset_modx
        self.new_textRect.y -= self.game.player_y2-self.offset_mody

        self.game.screen.blit(self.image,self.new_rect)
        self.game.screen.blit(self.text, self.new_textRect)
    def update(self):
        self.tick+=1
        if self.tick>=self.time:
            self.value+=1
            self.tick=0
        if self.value>self.max:
            self.value=self.max
        self.text = self.font.render(str(self.value), True, (0, 0, 0))


class Block(GameObject):
    def __init__(self, game, x, y, w, h, image_path, visible):
        super().__init__(game, x, y, w, h, image_path, visible)

        self.collision = True
        self.durability = 200

    def render(self):
        super().render()
        if self.durability <= 0:
            self.collision = False
            self.rect = None
            self.game.objects.remove(self)


