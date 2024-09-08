import random
import time

import pygame
from classes import buttons, inputBox
class MainMenu:
    def __init__(self, app):
        self.app = app
        self.main_text_rect_center = (self.app.width//2, 150 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        self.buttons = [buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 - 100 * self.app.scale, self.app.height/2 - 75 * self.app.scale/2, False, self.font, "Start", (0, 0, 0), self.font_color, 'start', self.app), buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 - 100 * self.app.scale, self.app.height/2 + 150 * self.app.scale/2, False, self.font, "Settings", (0, 0, 0), self.font_color, 'settings', self.app)]
        self.textBox = inputBox.TextBox(self.app.width/2 - 100 * self.app.scale,
                                       self.app.height/2 - 300 * self.app.scale/2,
                                       200 * self.app.scale,
                                       75 * self.app.scale,
                                       app,
                                       self.font,
                                       'Your nick')


    def render(self):
        self.app.screen.fill((0, 0, 0))
        # Tetris preview
        # main menu
        for button in self.buttons:
            button.render()
        self.textBox.render()
        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        display_text = font.render("G A M E  J A M", True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)


    def events(self):
        pass