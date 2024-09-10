import pygame


class Particle:
    def __init__(self, x, y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape, damage):
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

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        if 0 <= self.x <= screen_width and 0 <= self.y <= screen_height:
            #aura, memory laggy, fine for now

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
            screen.blit(surface, (self.x - self.size, self.y - self.size))

class ParticleSystem:
    def __init__(self, movable=False):
        self.particles = []
        self.movable = movable

    def add_particle(self, x, y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape, damage):
        self.particles.append(Particle(x, y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape, damage))

    def apply_force_to_all(self, fx, fy):
        for particle in self.particles:
            particle.apply_force(fx, fy)

    def update(self, game):
        particle_x, particle_y = 0, 0
        if self.movable:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                particle_x = - 10
            if keys[pygame.K_LEFT]:
                particle_x = 10
            if keys[pygame.K_UP]:
                particle_y = 10
            if keys[pygame.K_DOWN]:
                particle_y = -10
            if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
                particle_x = 0
            if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
                particle_y = 0
        for particle in self.particles:
            particle.update(particle_x, particle_y)
            if particle.lifespan <= 0:
                self.particles.remove(particle)
        self.check_collisions(game)

    def check_collisions(self, game):
        for particle in self.particles:
            # Check collision with player
            if game.player.rect.colliderect(particle.x, particle.y, particle.size * 2, particle.size * 2):
                game.player.health -= particle.damage
                self.particles.remove(particle)
                continue

            # Check collision with zombies
            for zombie in game.enemies:
                if zombie.rect.colliderect(particle.x, particle.y, particle.size * 2, particle.size * 2):
                    zombie.health -= particle.damage
                    self.particles.remove(particle)
                    break

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)