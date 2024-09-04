import pygame, random

class Particle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, color, direction, speed):
        super().__init__(groups)
        self.color = color
        self.direction = direction
        self.positon = pos
        self.speed = speed
        self.alpha = 255
        self.fade_speed = random.randint(265, 500)
        self.size = random.randint(4, 14)

        self.create_surface()

    def create_surface(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size))

        self.rect = self.image.get_rect(center=self.positon)

    def move(self, dt):
        self.positon += self.direction * self.speed * dt
        self.rect.center = self.positon

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        #self.check_pos()
        self.check_alpha()