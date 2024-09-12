import random
from classes import settings, mainmenu, game
import pygame

import pygame
import colorsys

colors = [(0,173,238), (27,116,187), (246,146,30), (255,241,0), (139,197,63), (101,45,144),(236,27,36)]
resolutions = ["1000x800", "1200x900", "1920x1080", "2560x1440"]
gamemodes = ["3 Tetris", "Tetris", "5 Tetris"]
color_modes = ["Default", "Random", "Gray"]
class Button:
    def __init__(self, width, height, x, y, translucent, font, text, bgcolor, fgcolor, function, app, random_color=True):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font_type = font
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.app = app
        self.text = text
        self.function = function
        self.outline_color = (255, 255, 255)  # Initial outline color
        self.hue = 0  # Starting hue
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(self.font_type, int(32 * self.app.scale))
        self.display_text = self.font.render(self.text, True, self.fgcolor)
        self.display_text_rect = self.display_text.get_rect()
        self.display_text_rect.center = self.rect.center
        self.random_color = random_color
        if self.random_color:
            self.hover_color = random.choice(colors)
        else:
            self.hover_color = (40, 40, 40)
        pygame.font.init()

    def render(self):
        self.display_text = self.font.render(self.text, True, self.fgcolor)
        self.display_text_rect = self.display_text.get_rect()
        self.display_text_rect.center = self.rect.center
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            current_bg_color = self.hover_color
        else:
            current_bg_color = self.bgcolor

        # Update the outline color
        self.hue = (self.hue + 0.001) % 1  # Increment hue and wrap around at 1
        self.outline_color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(self.hue, 1, 1))

        # Draw the button
        pygame.draw.rect(self.app.screen, current_bg_color, self.rect, border_radius=5)
        pygame.draw.rect(self.app.screen, self.outline_color, self.rect, 5, border_radius=5)
        self.app.screen.blit(self.display_text, self.display_text_rect)
    def click(self):
        if self.function == 'start':
            self.app.last_player = self.app.ui.textBox.text
            self.app.ui = game.Game(self.app)
            #self.app.ui = tetris.TetrisGame(self.app, 20, 10) # Change the displayed ui to the simulation
        elif self.function == 'start_game':
            level = self.app.ui.selected_level
            self.app.ui = tetris.TetrisGame(self.app, 20, 10, level)  # Change the displayed ui to the simulation
        elif self.function == 'settings':
            self.app.last_player = self.app.ui.textBox.text
            self.app.ui = settings.Settings(self.app)
        elif self.function == 'exit':
            pygame.quit()
            self.app.run = False
        elif self.function == 'save_score':
            playernick.Playernick.SaveScore(self.app.ui.score)
        elif self.function == 'plus':
            self.app.ui.add()
        elif self.function == 'minus':
            self.app.ui.subtract()
        elif self.function == 'resolution':
            if self.app.ui.current_resolution < len(resolutions) - 1:
                self.app.ui.current_resolution += 1
            else:
                self.app.ui.current_resolution = 0
            self.text = resolutions[self.app.ui.current_resolution]
        elif self.function == 'fullscreen':
            if self.app.ui.current_fs == "False":
                self.app.ui.current_fs = "True"
            else:
                self.app.ui.current_fs = "False"
            self.text = self.app.ui.current_fs
        elif self.function == 'mode':
            if self.app.ui.current_gamemode < len(gamemodes) - 1:
                self.app.ui.current_gamemode += 1
            else:
                self.app.ui.current_gamemode = 0
            self.text = gamemodes[self.app.ui.current_gamemode]
        elif self.function == 'level':
            if self.app.ui.current_default_level < 15:
                self.app.ui.current_default_level += 1
            else:
                self.app.ui.current_default_level = 1
            self.text = str(self.app.ui.current_default_level)
        elif self.function == 'colors':
            if self.app.ui.current_colors < len(color_modes) - 1:
                self.app.ui.current_colors += 1
            else:
                self.app.ui.current_colors = 0
            self.text = color_modes[self.app.ui.current_colors]
        elif self.function == 'speed':
            if self.app.ui.current_fall_speed < 15:
                self.app.ui.current_fall_speed += 1
            else:
                self.app.ui.current_fall_speed = 5
            self.text = str(self.app.ui.current_fall_speed)
        elif self.function == 'save_settings':
            self.app.ui.save()
        elif self.function == 'back_to_menu':
            self.app.ui = mainmenu.MainMenu(self.app)
            self.app.onLevel = False
        else:
            self.bgcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))