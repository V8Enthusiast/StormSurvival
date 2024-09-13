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
        self.buttons = [
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 100 * self.app.scale,
                           self.app.height / 2 - 25 * self.app.scale / 2, False, self.font, "Start", (0, 0, 0),
                           self.font_color, 'start', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 100 * self.app.scale,
                           self.app.height / 2 + 200 * self.app.scale / 2, False, self.font, "Settings", (0, 0, 0),
                           self.font_color, 'settings', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 100 * self.app.scale,
                           self.app.height / 2 + 500 * self.app.scale / 2, False, self.font, "Exit", (0, 0, 0),
                           self.font_color, 'exit', self.app)
        ]
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.app.run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(click_pos[0], click_pos[1]):
                        self.app.fade(fade_in=False)
                        button.click()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pass
            if not self.app.onLevel and event.type == pygame.KEYDOWN:
                self.app.ui.textBox.handle_event(event)