import pygame
from classes import buttons, slider
import settings_values
import json

resolutions = ["1000x800", "1200x900", "1920x1080", "2560x1440"]
gamemodes = ["3 Tetris", "Tetris", "5 Tetris"]
color_modes = ["Default", "Random", "Gray"]

class Settings:
    def __init__(self, app):
        self.app = app
        self.main_text_rect_center = (self.app.width // 2, 55 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        settings = self.read_settings('settings.json')
        self.buttons = [
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 - 575 * self.app.scale / 2, False, self.font, f"{resolutions[settings['Resolution']]}", (0, 0, 0), self.font_color, 'resolution', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 - 375 * self.app.scale / 2, False, self.font, f"{settings['Fullscreen']}", (0, 0, 0), self.font_color, 'fullscreen', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 - 175 * self.app.scale / 2, False, self.font, f"{settings['Pay for chest']}", (0, 0, 0), self.font_color, 'pay_for_chest', self.app),
            # buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 + 25 * self.app.scale / 2, False, self.font, f"{settings['Default level']}", (0, 0, 0), self.font_color, 'level', self.app),
            # buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 + 225 * self.app.scale / 2, False, self.font, f"{color_modes[settings['Block colors']]}", (0, 0, 0), self.font_color, 'colors', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 225 * self.app.scale, self.app.height / 2 + 625 * self.app.scale / 2, False, self.font, "Save", (0, 0, 0), self.font_color, 'save_settings', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 25 * self.app.scale, self.app.height / 2 + 625 * self.app.scale / 2, False, self.font, "Exit", (0, 0, 0), self.font_color, 'back_to_menu', self.app)
        ]
        font = pygame.font.Font(self.font, int(48 * self.app.scale))
        self.texts = [
            font.render("Resolution", True, self.font_color),
            font.render("Fullscreen", True, self.font_color),
            font.render("Pay for chest", True, self.font_color),
            # font.render("Default level", True, self.font_color),
            # font.render("Block colors", True, self.font_color),
            font.render("Music volume", True, self.font_color)
        ]

        self.current_resolution = settings['Resolution']
        self.current_fs = settings['Fullscreen']
        self.current_pay = settings['Pay for chest']
        # self.current_default_level = settings['Default level']
        # self.current_colors = settings['Block colors']
        # self.current_fall_speed = settings['Max fall speed']
        self.current_volume = settings.get('Volume', 0.5)

        self.volume_slider = slider.Slider(
            self.app.width / 2 + 100 * self.app.scale,
            self.app.height / 2 + 25 * self.app.scale / 2,
            200 * self.app.scale,
            20 * self.app.scale,
            0, 1, self.current_volume, self.app
        )

    def render(self):
        self.app.screen.fill((0, 0, 0))
        for button in self.buttons:
            button.render()
        for i, text in enumerate(self.texts):
            rect = pygame.Rect(self.app.width / 2 - 100 * self.app.scale, self.app.height / 2 - (515 - 200 * i) * self.app.scale / 2, 10, 10)
            text_rect = text.get_rect()
            text_rect.center = rect.center
            self.app.screen.blit(text, text_rect)

        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        display_text = font.render("S E T T I N G S", True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center

        self.volume_slider.render()

        self.app.screen.blit(display_text, display_text_rect)

    def save(self):
        settings = {
            'Resolution': self.current_resolution,
            'Fullscreen': self.current_fs,
            'Pay for chest': settings_values.pay_for_chest,
            # 'Default level': self.current_default_level,
            # 'Block colors': self.current_colors,
            # 'Max fall speed': self.current_fall_speed,
            'Volume': self.volume_slider.value
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
        settings_values.pay_for_chest = settings['Pay for chest']
        # settings_values.default_level = settings['Default level']
        # settings_values.block_colors = settings['Block colors']
        # settings_values.max_fall_speed = settings['Max fall speed']
        self.main_text_rect_center = (self.app.width // 2, 75 * self.app.scale)
        self.buttons = [
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 - 575 * self.app.scale / 2, False, self.font, f"{resolutions[settings['Resolution']]}", (0, 0, 0), self.font_color, 'resolution', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 - 375 * self.app.scale / 2, False, self.font, f"{settings['Fullscreen']}", (0, 0, 0), self.font_color, 'fullscreen', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 - 175 * self.app.scale / 2, False, self.font, f"{settings['Pay for chest']}", (0, 0, 0), self.font_color, 'pay_for_chest', self.app),
            # buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 + 25 * self.app.scale / 2, False, self.font, f"{settings['Default level']}", (0, 0, 0), self.font_color, 'level', self.app),
            # buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 100 * self.app.scale, self.app.height / 2 + 225 * self.app.scale / 2, False, self.font, f"{color_modes[settings['Block colors']]}", (0, 0, 0), self.font_color, 'colors', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 225 * self.app.scale, self.app.height / 2 + 625 * self.app.scale / 2, False, self.font, "Save", (0, 0, 0), self.font_color, 'save_settings', self.app),
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 + 25 * self.app.scale, self.app.height / 2 + 625 * self.app.scale / 2, False, self.font, "Exit", (0, 0, 0), self.font_color, 'back_to_menu', self.app)
        ]

        self.volume_slider = slider.Slider(
            self.app.width / 2 + 100 * self.app.scale,
            self.app.height / 2 + 25 * self.app.scale / 2,
            200 * self.app.scale,
            20 * self.app.scale,
            0, 1, settings.get('Volume', 0.5), self.app
        )

    def read_settings(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            settings = data['settings']
            return settings
    def events(self):
        for event in pygame.event.get():
            self.volume_slider.handle_event(event)
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
        self.app.mixer.change_volume(self.volume_slider.value)