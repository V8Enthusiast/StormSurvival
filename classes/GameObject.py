import pygame.image
import pygame

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
        pygame.transform.scale(self.image,(self.w,self.h))
        self.rect=pygame.Rect(x,y,w,h)
        self.game.objects.append(self)
    def render(self):
        self.x+=self.game.dx
        self.y+=self.game.dy
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

