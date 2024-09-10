import json

import pygame
from classes.particles import ParticleSystem
from mixer import Mixer
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
            print("Couldn't connect to Discord RPC")

        self.width = width
        self.height = height

        self.clock = pygame.time.Clock()
        self.mixer = Mixer()
        self.mixer.load_music('sounds/Jim Yosef - Link [NCS Release].mp3')
        self.mixer.play_music()
        self.unityparticlesystem = ParticleSystem()

        # Save the data passed into the function to variables
        with open('settings.json', 'r') as file:
            data = json.load(file)
            settings = data['settings']

        settings_values.mode = settings['Gamemode']
        settings_values.default_level = settings['Default level']
        settings_values.block_colors = settings['Block colors']
        settings_values.max_fall_speed = settings['Max fall speed']

        settings_values.volume = settings['Volume']

        self.mixer.change_volume(settings_values.volume)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.width = int(resolutions[settings['Resolution']].split('x')[0])
        self.height = int(resolutions[settings['Resolution']].split('x')[1])
        self.is_FS_enabled = fullscreen
        self.is_vsync_enabled = vsync
        self.scale = 1
        self.screen = pygame.display.set_mode((width, height))
        self.last_player = ''
        self.ui = mainmenu.MainMenu(self)
        self.onLevel = False

        self.ui = mainmenu.MainMenu(self)

        # Window setup
        if fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, vsync=int(vsync))
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), vsync=int(vsync))

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