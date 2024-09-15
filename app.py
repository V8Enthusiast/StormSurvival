import json

import pygame
from classes.particles import ParticleSystem
from Assets.mixer import Mixer
from classes import mainmenu
import settings_values

import time

from pypresence import Presence

resolutions = ["1000x800", "1200x900", "1920x1080", "2560x1440"]
class App:
    def __init__(self, width, height, fullscreen, vsync):
        try:
            client_id = '1282943400479559792'
            rpc = Presence(client_id)
            rpc.connect()
            rpc.update(state="In Game", start=time.time())
        except:
            # print("Couldn't connect to Discord RPC")
            pass

        self.width = width
        self.height = height
        self.old_ui = None
        self.clock = pygame.time.Clock()
        self.mixer = Mixer()
        self.mixer.load_music('sounds/perfect-beauty-not-copyrighted.mp3')
        self.mixer.play_music()
        # Save the data passed into the function to variables
        with open('settings.json', 'r') as file:
            data = json.load(file)
            settings = data['settings']
        self.resolution_number=settings['Resolution']
        self.fullscreen = settings['Fullscreen']

        # settings_values.mode = settings['Gamemode']
        # settings_values.default_level = settings['Default level']
        # settings_values.block_colors = settings['Block colors']
        # settings_values.max_fall_speed = settings['Max fall speed']

        settings_values.volume = settings['Volume']

        self.mixer.change_volume(settings_values.volume)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.width = int(resolutions[settings['Resolution']].split('x')[0])
        self.height = int(resolutions[settings['Resolution']].split('x')[1])
        self.is_FS_enabled = self.fullscreen
        self.is_vsync_enabled = vsync
        self.scale = 1
        self.screen = pygame.display.set_mode((width, height))
        self.last_player = ''
        self.ui = mainmenu.MainMenu(self)
        self.onLevel = False

        self.ui = mainmenu.MainMenu(self)
        # Window setup
        if str(self.fullscreen) == "True":
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=int(vsync))
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), vsync=int(vsync))

        pygame.display.set_caption("Storm Survival")
        icon = pygame.image.load('Assets/Weapons/Colt45.png')
        pygame.display.set_icon(icon)

    def fade(self, fade_in=True, duration=0.5):
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(0)
        fade_alpha = 255 if fade_in else 0
        fade_step = 255 / (self.fps * duration)

        for _ in range(int(self.fps * duration)):
            if fade_in:
                fade_alpha -= fade_step
            else:
                fade_alpha += fade_step

            fade_surface.set_alpha(int(fade_alpha))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = pygame.mouse.get_pos()
                for button in self.ui.buttons:
                    if button.rect.collidepoint(click_pos[0], click_pos[1]):
                        button.click()
                if type(self.ui) == mainmenu.MainMenu and self.onLevel is False:
                    self.ui.textBox.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pass
                # print(pygame.mouse.get_pos())
            if not self.onLevel and event.type == pygame.KEYDOWN:
                #self.ui.textBox.handle_event(event)
                pass





    def run(self):
        while True:
            self.clock.tick(60)

            self.screen.fill((0, 0, 0))

            self.ui.render()

            pygame.display.flip()
            self.ui.events()

            self.events()