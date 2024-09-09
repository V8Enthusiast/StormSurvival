import random
import time

import pygame
from classes import buttons, inputBox, GameObject
class Game:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.main_text_rect_center = (self.app.width//2, 150 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        self.screen=self.app.screen
        self.buttons = []
        self.speed = 10
        self.dx = 0
        self.dy = 0

        self.test_object=GameObject.Storm(self,-1000,0,500,1080,'Assets/Bez-nazwy (1).jpg',True)
        self.objects.append(GameObject.Chest(self, 300, 300, 150, 150, "Assets/Chest.jpeg", True))
        self.player = GameObject.Player(self, 400,400,100,100,'Assets/player.png',True)
        self.init_tiles()

    def init_tiles(self):
        tile_image_path = 'Assets/tile.png'  # Path to your tile image
        for y in range(0, self.app.height, 48):
            for x in range(0, self.app.width, 48):
                tile = GameObject.Tile(self, x, y, tile_image_path)
                self.objects.append(tile)



    def render(self):
        print(self.dx)
        self.app.screen.fill((0, 0, 0))
        # Tetris preview
        # main menu
        for button in self.buttons:
            button.render()
        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        # Render tiles first
        for object in self.objects:
            if isinstance(object, GameObject.Tile):
                object.render()

        # Render other game objects
        for object in self.objects:
            if not isinstance(object, (GameObject.Tile, GameObject.Player, GameObject.Storm)):
                object.render()

        # Render player
        for object in self.objects:
            if isinstance(object, GameObject.Player):
                object.render()

        # Render storm
        for object in self.objects:
            if isinstance(object, GameObject.Storm):
                object.move()
                object.render()


    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.dy = -self.speed
                if event.key == pygame.K_s:
                    self.dy = +self.speed
                if event.key == pygame.K_a:
                    self.dx = -self.speed
                if event.key == pygame.K_d:
                    self.dx = self.speed
            self.player.relative_position[0] += self.dx
            self.player.relative_position[1] += self.dy
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    if self.dy==-self.speed:
                        self.dy = 0
                if event.key == pygame.K_s:
                    if self.dy == +self.speed:
                        self.dy = 0
                if event.key == pygame.K_a:
                    if self.dx == -self.speed:
                        self.dx = 0
                if event.key == pygame.K_d:
                    if self.dx==+self.speed:
                        self.dx = 0






