import pygame
from particleł import ParticleSystem
import random

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.unityparticlesystem = ParticleSystem()

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.unityparticlesystem.add_particle(400, 300, random.uniform(-1, 1), -5, 1, 1000, 10, 255, 255, 255, 100, 'deltoid')
            self.unityparticlesystem.apply_force_to_all(0, 0.1)

            self.unityparticlesystem.update()

            self.unityparticlesystem.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)