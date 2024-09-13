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

    def get_volume(self):
        return pygame.mixer.music.get_volume()

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sound(self, file_path):
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(self.get_volume())
        sound.play()