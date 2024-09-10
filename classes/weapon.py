import pygame
import random
import math
import images
from classes import particles

class Weapon:
    def __init__(self, game, player, image, ammo, max_ammo):
        self.player = player
        self.image = image
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.game = game

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(100):
                vx = 5 * math.cos(self.player.angle)
                vy = 5 * math.sin(self.player.angle)
                speed = random.uniform(1, 3)
                lifespan = random.randint(20, 50)
                size = random.randint(2, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'circle'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape)

            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

    def reload(self):
        self.ammo = self.max_ammo
        self.game.sound_mixer.play_sound('Assets/reload.mp3')


class Glock17(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.glock17, 17, 17)

class PumpActionShotgun(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.pump_action_shotgun, 5, 5)

class AmmoBox(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.ammo_box, 0, 0)

class M4A1(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.m4a1, 30, 30)

class BoltActionSniper(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.bolt_action_sniper, 5, 5)

class AmmoCrate(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.ammo_crate, 0, 0)

class MAC10(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.mac10, 30, 30)

class M1911(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.m1911, 7, 7)

class ScarH(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.scarh, 20, 20)

class DesertEagle(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.desert_eagle, 7, 7)

class Magnum44(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.magnum44, 6, 6)