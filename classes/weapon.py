import pygame
import random
import math
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

            self.game.sound_mixer.play_sound('Assets/shoot.wav')

    def reload(self):
        self.ammo = self.max_ammo

    def render(self):
        if self.player.game.hotbar.items[self.player.game.hotbar.selected_slot] == "Gun":
            rotated_gun = pygame.transform.rotate(self.image, -math.degrees(self.player.angle))
            gun_length = self.image.get_width() // 2
            offset_x = gun_length * math.cos(self.player.angle) * 1.5
            offset_y = gun_length * math.sin(self.player.angle) * 1.5
            gun_rect = rotated_gun.get_rect(center=(self.player.x + self.player.w // 2 + offset_x, self.player.y + self.player.h // 2 + offset_y))
            self.player.screen.blit(rotated_gun, gun_rect)