import os
import random
import time

import pygame
from classes import buttons, inputBox
class MainMenu:
    def __init__(self, app):
        self.app = app
        self.main_text_rect_center = (self.app.width//2, 130 * self.app.scale)
        self.score_text_rect_center = (self.app.width//2, 245)
        self.font = "fonts/second.ttf"
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
                                       'Player 1')

        if not os.path.isfile("scores.save"):
            t = open("scores.save", "x")
            t.close()

        if not os.path.isfile("lastplayer.save"):
            t = open("lastplayer.save", "x")
            t.close()

        r = open("lastplayer.save", "r")
        last_player = r.readline().strip()
        r.close()

        if self.app.last_player == '' and last_player != None:
            self.app.last_player = last_player

        exists = False
        f = open("scores.save", "r")
        for line in f:
            s = line.strip().split(";")
            if s[0].lower() == self.app.last_player.lower():
                exists = True
                self.displayed_score = int(s[1])
                self.displayed_player = s[0]
        if exists is False:
            self.displayed_score = 0
        f.close()

    def render(self):
        self.app.screen.fill((0, 0, 0))
        # Tetris preview
        # main menu
        for button in self.buttons:
            button.render()
        self.textBox.render()
        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        display_text = font.render("S T O R M  S U R V I V A L", True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center

        font2 = pygame.font.Font(self.font, int(48 * self.app.scale))
        score_text = font2.render(str(self.displayed_score), True, (0, 255, 0))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = self.score_text_rect_center

        self.app.screen.blit(display_text, display_text_rect)
        self.app.screen.blit(score_text, score_text_rect)


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

                self.textBox.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pass
            if not self.app.onLevel and event.type == pygame.KEYDOWN:
                self.app.ui.textBox.handle_event(event)