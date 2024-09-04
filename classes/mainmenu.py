import random
import time

import pygame
from classes import buttons, inputBox, tetris_widget, tetris_structure
class MainMenu:
    def __init__(self, app):
        self.app = app
        self.main_text_rect_center = (self.app.width//2, 150 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        self.buttons = [buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 - 100 * self.app.scale, self.app.height/2 - 75 * self.app.scale/2, False, self.font, "Start", (0, 0, 0), self.font_color, 'start', self.app), buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 - 100 * self.app.scale, self.app.height/2 + 150 * self.app.scale/2, False, self.font, "Settings", (0, 0, 0), self.font_color, 'settings', self.app)]
        self.textBox = inputBox.TextBox(self.app.width/2 - 100 * self.app.scale,
                                       self.app.height/2 - 300 * self.app.scale/2,
                                       200 * self.app.scale,
                                       75 * self.app.scale,
                                       app,
                                       self.font,
                                       'Your nick')

        # Tetris preview
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.tile_color = (0, 0, 0)
        self.tile_outline_color = (40, 40, 40)
        self.ROWS = 20
        self.COLUMNS = int(self.app.width // (self.app.height/self.ROWS)) + 1
        self.blocks = {}
        self.map = [[0 for _ in range(self.COLUMNS)] for i in range(self.ROWS + 7)]
        self.tile_size = self.app.height/self.ROWS
        self.ROWS += 7

        self.border = 1
        self.x_offset = (self.app.width - self.tile_size * self.COLUMNS) / 2
        self.y_offset = (self.app.height - self.tile_size * self.ROWS) / 2
        self.block_spawner_x = self.COLUMNS // 2 - 2
        self.placed_structures = []
        self.structure_amount = 4
        self.clock = time.time()
        self.direction_clock = time.time()
        self.move_down_faster = False
        self.move_left = False
        self.move_right = False
        self.moving_speed = 40
        self.fps = 6
        self.game_over = False
        self.debug = False
        self.next_structures = tetris_structure.generate_bag(0, 0, self, random_x_coord=True)
        self.current_structures = [self.next_structures[0]]
        self.next_structures.pop(0)
        self.held_structure = None
        self.delay_between_blocks = 5
        self.current_delay = 0


    def render(self):
        self.app.screen.fill((127, 127, 127))
        # Tetris preview
        self.draw_tiles()
        current_time = time.time()
        moved = False
        for structure in self.current_structures:
            if current_time > self.clock + 1 / self.fps:
                structure.move(1, 0)
                moved = True
            if structure.can_move is False:
                self.current_structures.remove(structure)
                self.current_structures.append(self.next_structures[0])
                self.can_swap = True
                self.next_structures.pop(0)
                if len(self.next_structures) <= 3:
                    self.next_structures += tetris_structure.generate_bag(0, 0, self, random_x_coord=True)
        if moved:
            self.clock = current_time
            if self.current_delay >= self.delay_between_blocks:
                if len(self.current_structures) < self.structure_amount:
                    self.current_structures.append(self.next_structures[0])
                    self.next_structures.pop(0)
                    if len(self.next_structures) <= 3:
                        self.next_structures += tetris_structure.generate_bag(0, 0, self, random_x_coord=True)
                self.current_delay = 0
            else:
                self.current_delay += 1

        # main menu
        for button in self.buttons:
            button.render()
        self.textBox.render()
        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        display_text = font.render("G A M E  J A M", True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)
    def draw_tiles(self):
        self.app.screen.fill((40, 40, 40))
        for r_idx, r in enumerate(self.map):
            for c_idx, c in enumerate(r):
                rect = pygame.Rect(self.x_offset + c_idx * self.tile_size, self.y_offset + r_idx * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.app.screen, self.tile_color, rect)
                pygame.draw.rect(self.app.screen, self.tile_outline_color, rect, self.border)

        for structure in self.placed_structures:
            structure.render()
        for structure in self.current_structures:
            structure.render()

    def events(self):
        pass