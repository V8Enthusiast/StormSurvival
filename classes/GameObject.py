import pygame.image
import pygame
import math

class GameObject():
    def __init__(self,game,x,y,w,h,image_path,visible):
        self.game=game
        self.screen = self.game.screen
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.image_path=image_path
        self.image=pygame.image.load(image_path)
        self.image= pygame.transform.scale(self.image,(self.w,self.h))
        self.rect=pygame.Rect(x,y,w,h)
        self.game.objects.append(self)
    def render(self):
        self.x-=self.game.dx
        self.y-=self.game.dy
        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.screen.blit(self.image,self.rect)

class Player(GameObject):
    def __init__(self, game,x,y,w,h,image_path,visible):
        super().__init__(game,x,y,w,h,image_path,visible)

        self.health = 100
        self.size = 25
        self.color = (255, 105, 55)
    def render(self):
        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.screen.blit(self.image,self.rect)

class Storm(GameObject):
    def __init__(self, game,x,y,w,h,image_path,visible):
        super().__init__(game,x,y,w,h,image_path,visible)
        self.speed=1
        self.dmg=3
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
        print(ddx)
class Chest(GameObject):
    def __init__(self, game,x,y,w,h,image_path,visible):
        super().__init__(game,x,y,w,h,image_path,visible)

        self.Items = []
        self.CommonDrops = ["Glock 17", "Pump Action Shotgun", "Ammo Box"]
        self.UncommonDrops = ["M4A1", "Bolt Action Sniper", "Ammo Crate"]
        self.EpicDrops = ["MAC-10", "M1911 .45"]
        self.LegendaryDrops = ["Scar-H", "Desert Eagle", ".44 Magnum"]

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
