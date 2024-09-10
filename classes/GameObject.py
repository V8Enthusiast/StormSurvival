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



    def rotate_towards_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - self.y, mouse_x - self.x)


    def render(self):
        if self.health > 0:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if self.game.hotbar.items[self.game.hotbar.selected_slot] == "Gun":
                rotated_gun = pygame.transform.rotate(self.gun_image, -math.degrees(self.angle))
                gun_rect = rotated_gun.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
                self.screen.blit(rotated_gun, gun_rect)
            self.screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game.hotbar.items[self.game.hotbar.selected_slot] == "Gun":
            self.shoot()

    def shoot(self):
        gun_length = self.gun_image.get_width() // 2
        tip_x = self.x + self.w // 2 + gun_length * math.cos(self.angle)
        tip_y = self.y + self.h // 2 + gun_length * math.sin(self.angle)

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


class Storm(GameObject):
    def __init__(self, game,x,y,w,h,image_path,visible):
        super().__init__(game,x,y,w,h,image_path,visible)
        self.speed=1
        self.dmg=20
        self.last_damage_time = pygame.time.get_ticks()
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
        num_images = 200

        total_width = (num_images+1) * self.w
        self.rect = pygame.Rect(self.x - num_images*self.w, self.y, total_width, self.h)

        for i in range(num_images):
            offset_x = self.x - i * self.w
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


