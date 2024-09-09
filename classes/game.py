import random
import time

import pygame
from classes import buttons, inputBox, GameObject, particles
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

        self.player = GameObject.Player(self, self.app.width // 2 - 50, self.app.height // 2 - 50, 100, 100,
                                        'Assets/player.png', True)
        self.test_object = GameObject.Storm(self, -1000, 0, 500, 1080, 'Assets/Bez-nazwy (1).jpg', True)
        self.objects.append(GameObject.Chest(self, 300, 300, 150, 150, "Assets/Chest.jpeg", True))

        self.tiles = {}
        self.tile_image = pygame.image.load('Assets/tile.png').convert_alpha()  # Load and convert image
        self.tile_size = 48  # Assuming each tile is 48x48 pixels
        self.init_tiles()

        self.unityparticlesystem = particles.ParticleSystem()

    def init_tiles(self):
        for y in range(0, self.app.height, self.tile_size):
            for x in range(0, self.app.width, self.tile_size):
                self.add_tile(x, y)

    def add_tile(self, x, y, force=False):
        if force or (x, y) not in self.tiles:
            self.tiles[(x, y)] = self.tile_image

    def render(self):
        print(self.dx)
        self.app.screen.fill((0, 0, 0))

        player_x, player_y = self.player.relative_position

        max_x = max(x for x, y in self.tiles.keys())


        if player_x * 2 + self.app.width > max_x:
            for y in range(0, self.app.height, self.tile_size):
                self.add_tile(max_x + self.tile_size, y, force=True)

        for (x, y), tile_image in self.tiles.items():
            self.screen.blit(tile_image, (x - player_x * 2, y - player_y * 2))

        # Render other game objects
        for obj in self.objects:
            if not isinstance(obj, (GameObject.Tile, GameObject.Player, GameObject.Storm)):
                obj.render()
            elif isinstance(obj, GameObject.Player):
                obj.render()
            elif isinstance(obj, GameObject.Storm):
                obj.move()
                obj.render()


        self.unityparticlesystem.update()

        self.unityparticlesystem.draw(self.screen)


    def events(self):
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_w]:
            self.dy = -self.speed
        elif keys[pygame.K_s]:
            self.dy = self.speed
        else:
            self.dy = 0

        if keys[pygame.K_a]:
            self.dx = -self.speed
        elif keys[pygame.K_d]:
            self.dx = self.speed
        else:
            self.dx = 0

        # Update player position based on current dx and dy
        self.player.relative_position[0] += self.dx
        self.player.relative_position[1] += self.dy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
