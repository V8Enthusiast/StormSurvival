import os

import pygame
from classes import mainmenu, buttons

class GameOver:
    def __init__(self, app, score):
        self.app = app
        self.font = pygame.font.Font("fonts/main_font.ttf", 64)
        self.font2 = pygame.font.Font("fonts/main_font.ttf", 42)
        self.text = self.font.render("Game Over", True, (255, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.app.width // 2, self.app.height // 2 - 300 * self.app.scale))
        self.buttons = [
            buttons.Button(200, 50, self.app.width // 2 - 100, self.app.height // 2 + 100, False, "fonts/main_font.ttf", "Main Menu", (0, 0, 0), (255, 255, 255), "back_to_menu", self.app)
        ]
        self.score = score

        if not os.path.isfile("scores.save"):
            t = open("scores.save", "x")
            t.close()

        f = open("scores.save", "r")
        player_scores = {}
        for line in f:
            s = line.strip().split(";")
            player_scores[s[0]] = int(s[1])
        f.close()

        if self.app.last_player not in player_scores.keys() or score > player_scores[self.app.last_player]:
            w = open("scores.save", "w")
            player_scores[self.app.last_player] = self.score
            for key, value in player_scores.items():
                w.write(key + ";" + str(value) + "\n")

        self.score_text = self.font2.render("Score  " + str(self.score), True, (0, 255, 0))
        self.score_text_rect = self.text.get_rect(center=(self.app.width // 2 + 50, self.app.height // 2 - 100 * self.app.scale))

    def render(self):
        self.app.screen.fill((0, 0, 0))
        self.app.screen.blit(self.text, self.text_rect)
        self.app.screen.blit(self.score_text, self.score_text_rect)
        for button in self.buttons:
            button.render()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.app.run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(click_pos):
                        button.click()