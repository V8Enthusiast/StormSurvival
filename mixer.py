import pygame

class Mixer:
    def __init__(self):
        pygame.mixer.init()

    def load_music(self, file_path):
        pygame.mixer.music.load(file_path)

    def play_music(self):
        pygame.mixer.music.play(-1)

    def change_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def stop_music(self):
        pygame.mixer.music.stop()