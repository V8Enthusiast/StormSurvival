import random
import time

import pygame

import images
from classes import buttons, inputBox, GameObject, particles, hotbar

import images

class Game:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.main_text_rect_center = (self.app.width//2, 150 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.helpText = ""
        self.font_color = (255, 255, 255)
        self.screen = self.app.screen
        self.buttons = []
        self.chests = []
        self.selected_chest = None
        self.chest_ui = None
        self.speed = 10
        self.dx = 0
        self.dy = 0

        self.player = GameObject.Player(self, self.app.width // 2 - 50, self.app.height // 2 - 50, 100, 100,
                                        images.player, True)
        self.test_object = GameObject.Storm(self, -1000, 0, 500, 1080, images.storm, True)
        chest = GameObject.Chest(self, 300, 300, 100, 100, images.chest, True)
        self.chests.append(chest)
        self.objects.append(chest)

        self.tiles = {}
        self.tile_size = 96
        #self.init_tiles()

        self.weaponparticlesystem = particles.ParticleSystem()
        self.current_max_x=0
        self.current_max_y=0
        self.current_min_x=0
        self.current_min_y=0
        self.tile_width=96

        self.hotbar = hotbar.Hotbar(self, 10, self.app.height-100, 5)
        self.hotbar.add_item("Gun", 0)


    # def init_tiles(self):
    #     for y in range(0, self.app.height, self.tile_size):
    #         for x in range(0, self.app.width, self.tile_size):
    #             tile_image = random.choice([images.grass, images.grass, images.grass, images.water])
    #             self.add_tile(x, y, tile_image)
    #
    # def add_tile(self, x, y, tile_image, force=False):
    #     if force or (x, y) not in self.tiles:
    #         self.tiles[(x, y)] = tile_image
    def generate_tiles(self):
        if self.current_max_x*self.tile_width<self.player.relative_position[0]+self.app.width/2:
            self.current_max_x+=1
            print(self.current_max_x,'a')
            for y in range(self.current_min_y,self.current_max_y):
                GameObject.GameObject(self,self.current_max_x*self.tile_width,y*self.tile_width,self.tile_width,self.tile_width,images.water,True)

        if self.current_min_y*self.tile_width>self.player.relative_position[1]-self.app.height/2:
            self.current_min_y-=1
            for x in range(self.current_min_x,self.current_max_x):
                GameObject.GameObject(self,x*self.tile_width,self.current_min_y*self.tile_width,self.tile_width,self.tile_width,images.water,True)
            print(self.current_min_y,'b')

    def render(self):
        self.generate_tiles()
        # print(self.dx)
        self.app.screen.fill((0, 0, 0))

        player_x, player_y = self.player.relative_position

        # max_x = max(x for x, y in self.tiles.keys())

        self.test_object.damage()

        # if player_x * 2 + self.app.width > max_x:
        #     for y in range(0, self.app.height, self.tile_size):
        #         self.add_tile(max_x + self.tile_size, y, random.choice([images.grass, images.grass, images.water]), force=True)
        #
        # for (x, y), tile_image in self.tiles.items():
        #     self.screen.blit(tile_image, (x - player_x * 2, y - player_y * 2))

        # Render other game objects
        for obj in self.objects:
            if not isinstance(obj, (GameObject.Tile, GameObject.Player, GameObject.Storm)):
                obj.render()
            elif isinstance(obj, GameObject.Player):
                obj.rotate_towards_cursor()
                obj.render()
            elif isinstance(obj, GameObject.Storm):
                obj.move()
                obj.render()
            if isinstance(obj, GameObject.Chest):
                if obj.rect.colliderect(self.player.rect) and self.chest_ui is None:
                    self.helpText = "Press E to open"
                    self.selected_chest = obj
                elif self.helpText == "Press E to open" or (self.chest_ui is not None and obj.rect.colliderect(self.player.rect) is False):
                    self.helpText = ""
                    self.selected_chest = None
                    self.chest_ui = None


        for p in self.weaponparticlesystem.particles:
            p.apply_force(random.uniform(-1, 1), random.uniform(-1, 1))

        self.weaponparticlesystem.update()

        self.weaponparticlesystem.draw(self.screen)

        self.hotbar.render()
        if self.chest_ui is not None:
            self.chest_ui.render()

        font = pygame.font.Font(self.font, int(48 * self.app.scale))
        display_text = font.render(self.helpText, True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)



    def events(self):
        keys = pygame.key.get_pressed()

        collidesWithAnything = False
        for obj in self.objects:
            if obj.collision is True:
                if obj.x - obj.w <= self.player.gameObjectPos[0] + self.player.w <= obj.x + obj.w // 2 and obj.y - obj.h <= self.player.gameObjectPos[1] + self.player.h//2 <= obj.y + obj.h: # Left
                    collidesWithAnything = True
                    self.player.canMoveRight = False
                elif obj.x - obj.w <= self.player.gameObjectPos[0] <= obj.x + obj.w // 2 and obj.y - obj.h <= self.player.gameObjectPos[1] + self.player.h//2 <= obj.y + obj.h: # Right
                    collidesWithAnything = True
                    self.player.canMoveLeft = False
                elif (obj.x - obj.w <= self.player.gameObjectPos[0] <= obj.x + obj.w // 2 or obj.x - obj.w <= self.player.gameObjectPos[0] + self.player.w <= obj.x + obj.w // 2) and obj.y - obj.h <= self.player.gameObjectPos[1] <= obj.y + obj.h:  # Up
                    collidesWithAnything = True
                    self.player.canMoveUp = False
                elif (obj.x - obj.w <= self.player.gameObjectPos[0] <= obj.x + obj.w // 2 or obj.x - obj.w <= self.player.gameObjectPos[0] + self.player.w <= obj.x + obj.w // 2) and obj.y - obj.h <= self.player.gameObjectPos[1] + self.player.h <= obj.y + obj.h:  # Down
                    collidesWithAnything = True
                    self.player.canMoveDown = False


        if collidesWithAnything is False:
            self.player.canMoveRight = True
            self.player.canMoveLeft = True
            self.player.canMoveUp = True
            self.player.canMoveDown = True

        if keys[pygame.K_w] and self.player.canMoveUp:
            self.dy = -self.speed
        elif keys[pygame.K_s] and self.player.canMoveDown:
            self.dy = self.speed
        else:
            self.dy = 0

        if keys[pygame.K_a] and self.player.canMoveLeft:
            self.dx = -self.speed
        elif keys[pygame.K_d] and self.player.canMoveRight:
            self.dx = self.speed
        else:
            self.dx = 0

        # Update player position based on current dx and dy
        self.player.relative_position[0] += self.dx
        self.player.relative_position[1] += self.dy
        # print(self.player.relative_position)

        self.player.gameObjectPos[0] += self.dx
        self.player.gameObjectPos[1] += self.dy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
            self.player.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.hotbar.select_slot(0)
                elif event.key == pygame.K_2:
                    self.hotbar.select_slot(1)
                elif event.key == pygame.K_3:
                    self.hotbar.select_slot(2)
                elif event.key == pygame.K_4:
                    self.hotbar.select_slot(3)
                elif event.key == pygame.K_5:
                    self.hotbar.select_slot(4)

                elif event.key == pygame.K_e:
                    if self.selected_chest is not None:
                        print(self.selected_chest.Items)

                        if self.chest_ui is not None:
                            self.chest_ui = None
                        else:
                            self.chest_ui = hotbar.Hotbar(self, self.selected_chest.x - 100,
                                                          self.selected_chest.y - 100, 5)
                            self.helpText = ""
