import random
import time

import pygame
from classes import buttons, inputBox
class Game:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.main_text_rect_center = (self.app.width//2, 150 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        self.buttons = []
        self.speed = 10
        self.dx = 0
        self.dy = 0



    def render(self):
        self.app.screen.fill((0, 0, 0))
        # Tetris preview
        # main menu
        for button in self.buttons:
            button.render()
        font = pygame.font.Font(self.font, int(72 * self.app.scale))


    def events(self):
        for event in pygame.event.get():
            if type(event) == pygame.K_w:
                self.dy = self.speed
            if type(event) == pygame.K_s:
                self.dx = -self.speed
            if type(event) == pygame.K_a:
                self.dx = -self.speed
            if type(event) == pygame.K_d:
                self.dx = self.speed



