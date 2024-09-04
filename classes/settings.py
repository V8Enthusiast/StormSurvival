import pygame
from classes import buttons
import settings_values
import json

resolutions = ["1000x800", "1200x900", "1920x1080", "2560x1440"]
gamemodes = ["3 Tetris", "Tetris", "5 Tetris"]
color_modes = ["Default", "Random", "Gray"]
class Settings:
    def __init__(self, app):
        self.app = app
        self.main_text_rect_center = (self.app.width//2, 75 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        settings = self.read_settings('settings.json')
        #print(settings)
        self.buttons = [buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 + 100 * self.app.scale, self.app.height/2 - 575 * self.app.scale/2, False, self.font, f"{resolutions[settings['Resolution']]}", (0, 0, 0), self.font_color, 'resolution', self.app),
                        buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 + 100 * self.app.scale, self.app.height/2 - 375 * self.app.scale/2, False, self.font, f"{settings['Fullscreen']}", (0, 0, 0), self.font_color, 'fullscreen', self.app),
                        buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 + 100 * self.app.scale, self.app.height/2 - 175 * self.app.scale/2, False, self.font, f"{gamemodes[settings['Gamemode']]}", (0, 0, 0), self.font_color, 'mode', self.app),
                        buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 + 100 * self.app.scale, self.app.height/2 + 25 * self.app.scale/2, False, self.font, f"{settings['Default level']}", (0, 0, 0), self.font_color, 'level', self.app),
                        buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 + 100 * self.app.scale, self.app.height/2 + 225 * self.app.scale/2, False, self.font, f"{color_modes[settings['Block colors']]}", (0, 0, 0), self.font_color, 'colors', self.app),
                        buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 + 100 * self.app.scale, self.app.height/2 + 425 * self.app.scale/2, False, self.font, f"{settings['Max fall speed']}", (0, 0, 0), self.font_color, 'speed', self.app),
                        buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 - 225 * self.app.scale, self.app.height/2 + 625 * self.app.scale/2, False, self.font, "Save", (0, 0, 0), self.font_color, 'save_settings', self.app),
                        buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 + 25 * self.app.scale, self.app.height/2 + 625 * self.app.scale/2, False, self.font, "Exit", (0, 0, 0), self.font_color, 'back_to_menu', self.app)]
        font = pygame.font.Font(self.font, int(48 * self.app.scale))
        self.texts = [font.render("Resolution", True, self.font_color),
                      font.render("Fullscreen", True, self.font_color),
                      font.render("Gamemode", True, self.font_color),
                      font.render("Default level", True, self.font_color),
                      font.render("Block colors", True, self.font_color),
                      font.render("Max fall speed", True, self.font_color)]

        self.current_resolution = settings['Resolution']
        self.current_fs = settings['Fullscreen']
        self.current_gamemode = settings['Gamemode']
        self.current_default_level = settings['Default level']
        self.current_colors = settings['Block colors']
        self.current_fall_speed = settings['Max fall speed']
    def render(self):
        self.app.screen.fill((0, 0, 0))
        for button in self.buttons:
            button.render()
        for i, text in enumerate(self.texts):
            rect = pygame.Rect(self.app.width/2 - 100 * self.app.scale, self.app.height/2 - (515 - 200 * i) * self.app.scale/2, 10, 10)
            text_rect = text.get_rect()
            text_rect.center = rect.center
            self.app.screen.blit(text, text_rect)


        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        display_text = font.render("S E T T I N G S", True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)

    def save(self):
        settings = {
            'Resolution': self.current_resolution,
            'Fullscreen': self.current_fs,
            'Gamemode': self.current_gamemode,
            'Default level': self.current_default_level,
            'Block colors': self.current_colors,
            'Max fall speed': self.current_fall_speed
        }
        with open('settings.json', 'w') as file:
            json.dump({'settings': settings}, file)
        self.apply_settings(settings)

    def apply_settings(self, settings):
        width = int(resolutions[self.current_resolution].split('x')[0])
        height = int(resolutions[self.current_resolution].split('x')[1])
        if self.current_fs == "True":
            self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN, vsync=int(self.app.is_vsync_enabled))
        else:
            self.screen = pygame.display.set_mode((width, height), vsync=int(self.app.is_vsync_enabled))
        self.app.width = width
        self.app.height = height
        settings_values.mode = settings['Gamemode']
        settings_values.default_level = settings['Default level']
        settings_values.block_colors = settings['Block colors']
        settings_values.max_fall_speed = settings['Max fall speed']
        self.main_text_rect_center = (self.app.width // 2, 75 * self.app.scale)
        self.buttons = [
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale,
                           self.app.height / 2 - 575 * self.app.scale / 2, False, self.font,
                           f"{resolutions[settings['Resolution']]}", (0, 0, 0), self.font_color, 'resolution',
                           self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale,
                           self.app.height / 2 - 375 * self.app.scale / 2, False, self.font,
                           f"{settings['Fullscreen']}", (0, 0, 0), self.font_color, 'fullscreen', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale,
                           self.app.height / 2 - 175 * self.app.scale / 2, False, self.font,
                           f"{gamemodes[settings['Gamemode']]}", (0, 0, 0), self.font_color, 'mode', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale,
                           self.app.height / 2 + 25 * self.app.scale / 2, False, self.font,
                           f"{settings['Default level']}", (0, 0, 0), self.font_color, 'level', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale,
                           self.app.height / 2 + 225 * self.app.scale / 2, False, self.font,
                           f"{color_modes[settings['Block colors']]}", (0, 0, 0), self.font_color, 'colors', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale,
                           self.app.height / 2 + 425 * self.app.scale / 2, False, self.font,
                           f"{settings['Max fall speed']}", (0, 0, 0), self.font_color, 'speed', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 225 * self.app.scale,
                           self.app.height / 2 + 625 * self.app.scale / 2, False, self.font, "Save", (0, 0, 0),
                           self.font_color, 'save_settings', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 25 * self.app.scale,
                           self.app.height / 2 + 625 * self.app.scale / 2, False, self.font, "Exit", (0, 0, 0),
                           self.font_color, 'back_to_menu', self.app)]

    def read_settings(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            settings = data['settings']
            return settings
    def events(self):
        pass