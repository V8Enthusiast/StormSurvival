import pygame
import random
import math
import images
from classes import particles

class Weapon:
    def __init__(self, game, player, image, ammo, max_ammo, fire_rate, firemode, damage):
        self.player = player
        self.image = image
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.game = game
        self.fire_rate = fire_rate # cannot be 0
        self.firemode = firemode # 0 - Semi Auto, 1 - Full Auto, 2 - Burst
        self.damage = damage

    def get_firemode_text(self):
        firemodes = ["Semi Auto", "Full Auto", "Burst"]
        return firemodes[self.firemode]

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
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red, green, blue, alpha, shape, self.damage, glowy=True)

            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

    def reload(self):
        self.ammo = self.max_ammo
        self.game.sound_mixer.play_sound('Assets/reload.mp3')


class Glock17(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.glock17, 17, 17, 3, 0, 10)

class PumpActionShotgun(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.pump_action_shotgun, 5, 5, 2, 0, 1)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(100):
                vx = random.uniform(math.cos(self.player.angle - 0.6), math.cos(self.player.angle + 0.6))
                vy = random.uniform(math.sin(self.player.angle - 0.6), math.sin(self.player.angle + 0.6))
                speed = random.uniform(7, 13)
                lifespan = random.randint(20, 500)
                size = random.randint(2, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')


class AmmoBox(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.ammo_box, 0, 0, 1, 1, 0)

    def shoot(self):
        pass

    def reload(self):
        pass

class M4A1(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.m4a1, 30, 30, 6, 1, 20)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(18, 19)
                lifespan = random.randint(20, 500)
                size = random.randint(5, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class BoltActionSniper(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.bolt_action_sniper, 5, 5, 1, 0, 200)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(20, 20)
                lifespan = random.randint(20, 500)
                size = random.randint(5, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')


class AmmoCrate(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.ammo_crate, 0, 0, 1, 1, 0)

    def shoot(self):
        pass

    def reload(self):
        pass

class MAC10(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.mac10, 30, 30, 14, 1, 10)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(14, 17)
                lifespan = random.randint(20, 500)
                size = random.randint(2, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class M1911(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.m1911, 7, 7, 4, 0, 15)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(14, 18)
                lifespan = random.randint(20, 500)
                size = random.randint(2, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class ScarH(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.scarh, 20, 20, 5, 1, 27)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(15, 20)
                lifespan = random.randint(20, 500)
                size = random.randint(2, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class DesertEagle(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.desert_eagle, 7, 7, 3, 0, 34)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(16, 18)
                lifespan = random.randint(20, 500)
                size = random.randint(2, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class Magnum44(Weapon):
    def __init__(self, game, player):
        super().__init__(game, player, images.magnum44, 6, 6, 2, 0, 69)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 2.2
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 2.2

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(14, 17)
                lifespan = random.randint(20, 500)
                size = random.randint(2, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')