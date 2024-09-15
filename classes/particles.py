import math

import pygame
from classes import GameObject

class Particle:
    def __init__(self, x, y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape, damage, glowy = False, face_direction=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.speed = speed
        self.lifespan = lifespan
        self.size = size
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        self.shape = shape
        self.damage = damage
        self.glowy = glowy
        self.face_direction = face_direction

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def update(self, x, y):
        self.x += self.vx * self.speed
        self.x += x
        self.y += self.vy * self.speed
        self.y += y
        if self.alpha > 0 and self.lifespan > 0:
            self.alpha -= self.alpha // (1 / 2 * self.lifespan)
            self.lifespan -= 2

    def get_angle(self):
        return math.degrees(math.atan2(self.vy, self.vx))-90

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        if 0 <= self.x <= screen_width and 0 <= self.y <= screen_height:
            #aura, memory laggy, fine for now
            if self.glowy:
                aura_surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)

                for i in range(self.size * 2, 0, -1):
                    aura_alpha = max(self.alpha // 2 * (i / (self.size * 2)), 0)
                    pygame.draw.circle(aura_surface, (self.red, self.green, self.blue, int(aura_alpha)),
                                       (self.size * 2, self.size * 2), i)
                screen.blit(aura_surface, (self.x - self.size * 2, self.y - self.size * 2))

            surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            if self.shape == 'circle':
                pygame.draw.circle(surface, (self.red, self.green, self.blue, self.alpha), (self.size, self.size),
                                   self.size)
            elif self.shape == 'square':
                pygame.draw.rect(surface, (self.red, self.green, self.blue, self.alpha),
                                 pygame.Rect(0, 0, self.size * 2, self.size * 2))
            elif self.shape == 'triangle':
                pygame.draw.polygon(surface, (self.red, self.green, self.blue, self.alpha),
                                    [(self.size, 0), (0, self.size * 2), (self.size * 2, self.size * 2)])
            elif self.shape == 'deltoid':
                points = [
                    (self.size, 0),
                    (self.size * 1.5, self.size * 1.5),
                    (self.size, self.size * 2),
                    (self.size * 0.5, self.size * 1.5)
                ]
                pygame.draw.polygon(surface, (self.red, self.green, self.blue, self.alpha), points)

            elif self.shape == 'bullet':
                points = [
                    (self.size * 2, self.size),
                    (self.size * 1.3, self.size * 0.5),
                    (0, self.size * 0.5),
                    (0, self.size * 1.5),
                    (self.size * 1.3, self.size * 1.5)
                ]
                pygame.draw.polygon(surface, (self.red, self.green, self.blue, self.alpha), points)
            elif self.shape == 'water_drop':
                points = [(self.size, 0), (self.size * 1.5, self.size * 1.5), (self.size, self.size * 2), (self.size * 0.5, self.size * 1.5)]
                pygame.draw.polygon(surface, (self.red, self.green, self.blue, self.alpha), points)
                pygame.draw.circle(surface, (self.red, self.green, self.blue, self.alpha), (self.size, self.size * 1.5), self.size // 2)

            if self.face_direction:
                angle = self.get_angle()
                surface = pygame.transform.rotate(surface, -angle)

            screen.blit(surface, (self.x - self.size, self.y - self.size))

class ParticleSystem:
    def __init__(self, game, movable=False):
        self.particles = []
        self.movable = movable
        self.game = game

    def add_particle(self, x, y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape, damage, glowy = False, face_direction=False):
        self.particles.append(Particle(x, y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape, damage, glowy, face_direction))

    def apply_force_to_all(self, fx, fy):
        for particle in self.particles:
            particle.apply_force(fx, fy)

    def update(self, game):
        particle_x, particle_y = 0, 0
        if self.movable:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                particle_x = -self.game.dx
            if keys[pygame.K_a]:
                particle_x = -self.game.dx
            if keys[pygame.K_w]:
                particle_y = -self.game.dy
            if keys[pygame.K_s]:
                particle_y = -self.game.dy
            if keys[pygame.K_d] and keys[pygame.K_a]:
                particle_x = 0
            if keys[pygame.K_w] and keys[pygame.K_s]:
                particle_y = 0
        for particle in self.particles:
            particle.update(particle_x, particle_y)
            if particle.lifespan <= 0:
                self.particles.remove(particle)
        self.check_collisions(game)

    def check_collisions(self, game):
        for particle in self.particles:
            if particle.damage != 0:
                # Check collision with player
                if game.player.rect.colliderect(particle.x, particle.y, particle.size * 2, particle.size * 2):
                    game.player.health -= particle.damage
                    self.particles.remove(particle)
                    self.game.sound_mixer.play_sound('Assets/hit.mp3')
                    continue

                # Check collision with zombies
                for zombie in game.enemies:
                    if zombie.rect != None:
                        if zombie.rect.colliderect(particle.x, particle.y, particle.size * 2, particle.size * 2):
                            zombie.health -= particle.damage
                            self.particles.remove(particle)
                            self.game.sound_mixer.play_sound('Assets/hit.mp3')
                            break

                for object in game.objects:
                    if type(object) in [GameObject.Block, GameObject.Chest] and object.durability > 0:
                        if object.rect.colliderect(particle.x, particle.y, particle.size * 2, particle.size * 2):
                            self.particles.remove(particle)
                            object.durability -= particle.damage
                            print(object.durability)
                            break

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)