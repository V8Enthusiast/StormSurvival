import pygame
from classes import mainmenu, buttons

class GameOver:
    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font("fonts/main_font.ttf", 64)
        self.text = self.font.render("Game Over", True, (255, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.app.width // 2, self.app.height // 2))
        self.buttons = [
            buttons.Button(200, 50, self.app.width // 2 - 100, self.app.height // 2 + 100, False, "fonts/main_font.ttf", "Main Menu", (0, 0, 0), (255, 255, 255), "back_to_menu", self.app)
        ]

    def render(self):
        self.app.screen.fill((0, 0, 0))
        self.app.screen.blit(self.text, self.text_rect)
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