import random
import time

import pygame
from classes import buttons, inputBox, GameObject
class Game:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.main_text_rect_center = (self.app.width//2, 150 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        self.screen=self.app.screen
        self.buttons = []
        self.speed = 10
        self.dx = 0
        self.dy = 0

        self.test_object=GameObject.GameObject(self,0,0,10,10,'Assets/test.png',True)



    def render(self):
        print(self.dx)
        self.app.screen.fill((0, 0, 0))
        # Tetris preview
        # main menu
        for button in self.buttons:
            button.render()
        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        for object in self.objects:
            object.render()


    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.dy = self.speed
                if event.key == pygame.K_s:
                    self.dy = -self.speed
                if event.key == pygame.K_a:
                    self.dx = -self.speed
                if event.key == pygame.K_d:
                    self.dx = self.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    if self.dy==self.speed:
                        self.dy = 0
                if event.key == pygame.K_s:
                    if self.dy == -self.speed:
                        self.dy = 0
                if event.key == pygame.K_a:
                    if self.dx == -self.speed:
                        self.dx = 0
                if event.key == pygame.K_d:
                    if self.dx==self.speed:
                        self.dx = 0






