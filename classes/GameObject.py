import pygame.image
import pygame
import random
import math
import images

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


class Player(GameObject):
    def __init__(self, game,x,y,w,h,image_path,visible):
        super().__init__(game,x,y,w,h,image_path,visible)

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

        self.ammo = 10
        self.max_ammo = 10

    def render_health_bar(self):
        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = self.x + (self.w - health_bar_width) // 2
        health_bar_y = self.y - 20

        pygame.draw.rect(self.screen, (100, 100, 100), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        current_health_width = int(health_bar_width * (self.health / 100))
        pygame.draw.rect(self.screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))


    def rotate_towards_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - self.y, mouse_x - self.x)


    def render(self):
        if self.health > 0:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            self.screen.blit(rotated_image, rotated_rect.topleft)
            if self.game.hotbar.items[self.game.hotbar.selected_slot] == "Gun":
                rotated_gun = pygame.transform.rotate(self.gun_image, -math.degrees(self.angle))
                gun_length = self.gun_image.get_width() // 2
                offset_x = gun_length * math.cos(self.angle) * 1.5
                offset_y = gun_length * math.sin(self.angle) * 1.5
                gun_rect = rotated_gun.get_rect(center=(self.x + self.w // 2 + offset_x, self.y + self.h // 2 + offset_y))
                self.screen.blit(rotated_gun, gun_rect)
            self.render_health_bar()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = pygame.mouse.get_pos()
            if self.game.chest_ui is not None:
                slot_num = 0
                print(self.game.chest_ui.slot_rects)
                for slot_rect in self.game.chest_ui.slot_rects:
                    if slot_rect.collidepoint(click_pos):
                        print("slot " , slot_num , " selected")
                        break
                    slot_num += 1
                self.game.chest_ui.moved_item = slot_num
            if self.game.hotbar.items[self.game.hotbar.selected_slot] == "Gun":
                self.shoot()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.pick_up_item()
            elif event.key == pygame.K_q:
                self.drop_item()
            elif event.key == pygame.K_r:
                self.reload()

    def drop_item(self):
        item_name = self.game.hotbar.items[self.game.hotbar.selected_slot]
        if item_name:
            DroppedItem(self.game, self.x, self.y, 50, 50, images.gun, True, item_name)
            self.game.hotbar.items[self.game.hotbar.selected_slot] = None

    def pick_up_item(self):
        for obj in self.game.objects:
            if isinstance(obj, DroppedItem) and self.rect.colliderect(obj.rect):
                self.equip_item(obj.item_name)
                self.game.objects.remove(obj)

    def equip_item(self, item_name):
        self.game.hotbar.add_item(item_name, self.game.hotbar.selected_slot)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.gun_image.get_width() // 2
            tip_x = self.x + self.w // 2 + gun_length * math.cos(self.angle) *2.2
            tip_y = self.y + self.h // 2 + gun_length * math.sin(self.angle) *2.2

            for _ in range(100):
                vx = 5 * math.cos(self.angle)
                vy = 5 * math.sin(self.angle)
                speed = random.uniform(1, 3)
                lifespan = random.randint(20, 50)
                size = random.randint(2, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'circle'
                self.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape)

    def reload(self):
        self.ammo = self.max_ammo

class Storm(GameObject):
    def __init__(self, game,x,y,w,h,image_path,visible):
        super().__init__(game,x,y,w,h,image_path,visible)
        self.speed=1
        self.dmg=20
        self.last_damage_time = pygame.time.get_ticks()
        self.first_image=pygame.image.load('Assets/burza (1).jpg')
        self.first_image = pygame.transform.scale(self.first_image, (self.w, self.h))
    def distance(self):
        self.right=self.x+self.w
        return self.game.player.x-self.right
    def move(self):
        ddx=self.speed
        if self.distance()<100:
            ddx+=0
        elif self.distance()<0:
            ddx+=0
        else:
            ddx+=math.sqrt(self.distance()-100)/100
        self.x+=ddx

    def render(self):

        self.x-=2*self.game.dx
        self.y-=2*self.game.dy
        if self.y+self.h<0:
            self.y=self.game.app.height
        if self.y>self.game.app.height:

            self.y=0 -self.h
        num_images = 10

        total_width = (num_images+1) * self.w
        self.rect = pygame.Rect(self.x - num_images*self.w, self.y, total_width, self.h)

        for i in range(num_images):
            offset_x = self.x - i * self.w
            if i==0:
                self.screen.blit(self.first_image, (offset_x, self.y))
            else:

                self.screen.blit(self.image, (offset_x, self.y))

    def damage(self):
        current_time = pygame.time.get_ticks()
        if self.rect.colliderect(self.game.player.rect) and current_time - self.last_damage_time >= 500:
            self.game.player.health-=self.dmg
            self.last_damage_time = current_time
            self.game.player.image = pygame.transform.scale(images.damagedplayer, (self.game.player.w, self.game.player.h))

class Chest(GameObject):
    def __init__(self, game,x,y,w,h,image_path,visible):
        super().__init__(game,x,y,w,h,image_path,visible)

        self.Items = []
        self.CommonDrops = ["Glock 17", "Pump Action Shotgun", "Ammo Box"]
        self.UncommonDrops = ["M4A1", "Bolt Action Sniper", "Ammo Crate"]
        self.EpicDrops = ["MAC-10", "M1911 .45"]
        self.LegendaryDrops = ["Scar-H", "Desert Eagle", ".44 Magnum"]

        self.collision = True

        self.generateRandomItems()


    def generateRandomItems(self):
        for i in range(random.randint(1, 5)):
            rarity = random.randint(0, 100)
            if rarity > 35:
                self.Items.append(random.choice(self.UncommonDrops))
            elif rarity > 75:
                self.Items.append(random.choice(self.EpicDrops))
            elif rarity > 90:
                self.Items.append(random.choice(self.LegendaryDrops))
            else:
                self.Items.append(random.choice(self.CommonDrops))

class Tile(GameObject):
    def __init__(self, game, x, y, image_path):
        super().__init__(game, x, y, 48, 48, image_path, True)


class DroppedItem(GameObject):
    def __init__(self, game, x, y, w, h, image_path, visible, item_name):
        super().__init__(game, x, y, w, h, image_path, visible)
        self.item_name = item_name
        self.collision = True

    def render(self):
        self.x -= self.game.dx
        self.y -= self.game.dy
        super().render()
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.item_name, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (self.x, self.y - 20))