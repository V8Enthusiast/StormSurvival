import random

import pygame
import colorsys

pygame.font.init()

colors = [(0,173,238), (27,116,187), (246,146,30), (255,241,0), (139,197,63), (101,45,144),(236,27,36)]
FONT = pygame.font.Font(None, 32)
BLACK = (0,0,0)
class TextBox:
    def __init__(self, x, y, w, h, app, font, text=''):
        self.app = app
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.color2 = random.choice(colors)
        if self.app.last_player != '':
            self.text = self.app.last_player
        else:
            self.text = text
        self.txt_surface = FONT.render(text, True, BLACK)
        self.active = False
        self.outline_color = (255, 255, 255)  # Initial outline color
        self.hue = 0  # Starting hue
        self.font_type = font
        self.max_length = 10

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color2 if self.active else BLACK
            if self.active:
                if self.text == 'Your nick':
                    self.text = ''
            else:
                if self.text == '':
                    self.text = 'Your nick'
                else:
                    self.app.last_player = self.text

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Print the text to console
                    self.text = ''  # Clear the input box
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.text.__len__() < self.max_length:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, BLACK)

    def render(self):
        # Update the outline color
        # self.hue = (self.hue - 0.001) % 1  # Increment hue and wrap around at 1
        # self.outline_color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(self.hue, 1, 1))

        self.font = pygame.font.Font(self.font_type, int(32 * self.app.scale))
        self.display_text = self.font.render(self.text, True, (255, 255, 255))
        self.display_text_rect = self.display_text.get_rect()
        self.display_text_rect.center = self.rect.center

        pygame.draw.rect(self.app.screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(self.app.screen, self.outline_color, self.rect, 5, border_radius=5)
        self.app.screen.blit(self.display_text, self.display_text_rect)



