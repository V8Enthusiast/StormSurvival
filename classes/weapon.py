import pygame
import random
import math
import images
from classes import particles, weapon_selection_ui

class Weapon:
    def __init__(self, game, player, image, ammo, max_ammo, total_ammo, fire_rate, firemode, damage, zombie):
        self.player = player
        self.image = pygame.transform.scale(image,[60, 60])
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.total_ammo = total_ammo
        self.game = game
        self.fire_rate = fire_rate # cannot be 0
        self.firemode = firemode # 0 - Semi Auto, 1 - Full Auto, 2 - Burst
        self.damage = damage
        self.zombie = zombie

    def get_firemode_text(self):
        firemodes = ["Semi Auto", "Full Auto", "Burst"]
        return firemodes[self.firemode]

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

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
    #
    def reload(self):
        while self.ammo < self.max_ammo and self.total_ammo > 0:
            self.ammo += 1
            self.total_ammo -= 1
        self.game.sound_mixer.play_sound('Assets/reload.mp3')


class Glock17(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.glock17, 17, 17, 50, 3, 0, 10, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(15, 17)
                lifespan = random.randint(80, 160)
                size = random.randint(2, 4)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class PumpActionShotgun(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.pump_action_shotgun, 5, 5, 20, 2, 0, 2, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(20):
                vx = random.uniform(math.cos(self.player.angle - 0.4), math.cos(self.player.angle + 0.4))
                vy = random.uniform(math.sin(self.player.angle - 0.4), math.sin(self.player.angle + 0.4))
                speed = random.uniform(8, 12)
                lifespan = random.randint(60, 100)
                size = random.randint(2, 4)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')


class AmmoBox(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.ammo_box, 0, 10, random.randint(30, 50), 1, 1, 0, zombie)

    def shoot(self):
        weapons = [item for item in self.game.hotbar.items if isinstance(item, Weapon)]
        self.game.weapon_selection_ui = weapon_selection_ui.WeaponSelectionUI(self.game, weapons, self)
    #
    def reload(self):
        pass

class M4A1(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.m4a1, 30, 30, 150, 6, 1, 20, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(16, 18)
                lifespan = random.randint(80, 140)
                size = random.randint(3, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class BoltActionSniper(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.bolt_action_sniper, 5, 5, 20, 1, 0, 100, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(25, 30)
                lifespan = random.randint(200, 1000)
                size = random.randint(2, 4)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')


class AmmoCrate(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.ammo_crate, 0, 10, random.randint(60, 99), 1, 1, 0, zombie)

    def shoot(self):
        weapons = [item for item in self.game.hotbar.items if isinstance(item, Weapon)]
        self.game.weapon_selection_ui = weapon_selection_ui.WeaponSelectionUI(self.game, weapons, self)
    #
    def reload(self):
        pass

class MAC10(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.mac10, 30, 30, 90, 14, 1, 10, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(12, 14)
                lifespan = random.randint(60, 120)
                size = random.randint(3, 5)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class M1911(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.m1911, 7, 7, 50, 4, 0, 15, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(14, 16)
                lifespan = random.randint(70, 130)
                size = random.randint(2, 4)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class ScarH(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.scarh, 20, 20, 140, 5, 1, 25, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(15, 18)
                lifespan = random.randint(80, 200)
                size = random.randint(2, 4)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class DesertEagle(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.desert_eagle, 7, 7, 60, 3, 0, 30, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(14, 16)
                lifespan = random.randint(100, 160)
                size = random.randint(2, 4)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class Magnum44(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.magnum44, 6, 6, 50, 2, 0, 30, zombie)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(1):
                vx = math.cos(self.player.angle)
                vy = math.sin(self.player.angle)
                speed = random.uniform(14, 16)
                lifespan = random.randint(100, 160)
                size = random.randint(2, 4)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'bullet'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')

class FlameThrower(Weapon):
    def __init__(self, game, player, zombie):
        super().__init__(game, player, images.flamethrower, 100, 100, 500, 1, 1, 0.5, zombie)
        self.fire_rate = 30

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            gun_length = self.image.get_width() // 2
            tip_x = self.player.x + self.player.w // 2 + gun_length * math.cos(self.player.angle) * 3.00
            tip_y = self.player.y + self.player.h // 2 + gun_length * math.sin(self.player.angle) * 3.00

            for _ in range(30):
                vx = math.cos(self.player.angle) + random.uniform(-0.2, 0.2)
                vy = math.sin(self.player.angle) + random.uniform(-0.2, 0.2)
                speed = random.uniform(4, 7)
                lifespan = random.randint(20, 60)
                size = random.randint(1, 6)
                red, green, blue = 255, 255, 0
                alpha = 255
                shape = 'circle'
                self.player.game.weaponparticlesystem.add_particle(tip_x, tip_y, vx, vy, speed, lifespan, size, red,
                                                                   green, blue, alpha, shape, self.damage, glowy=True)
            self.game.sound_mixer.play_sound('Assets/shoot.mp3')