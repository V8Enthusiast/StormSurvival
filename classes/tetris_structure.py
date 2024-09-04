import random
from classes import block, particles
import settings_values
import pygame

colors = [(0,173,238), (27,116,187), (246,146,30), (255,241,0), (139,197,63), (101,45,144),(236,27,36)]
border_colors = [(105,206,244), (178,206,230), (248,187,117), (251,249,200), (213,234,188), (155,119,183), (242,109,114)]
def get_template():
    if settings_values.mode == 2:
        return [
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 1, 0]
            ],
            [
                [1, 1, 0],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [1, 0, 0, 0],
                [1, 1, 1, 1]
            ],
            [
                [0, 0, 0, 1],
                [1, 1, 1, 1]
            ],
            [
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0]
            ],
            [
                [1, 0, 1],
                [1, 1, 1]
            ],
            [
                [1, 1, 1],
                [1, 1, 0]
            ],
            [
                [1, 1, 0],
                [1, 1, 1]
            ],
            [
                [0, 0, 1],
                [0, 0, 1],
                [1, 1, 1]
            ],
            [
                [0, 0, 1],
                [0, 1, 1],
                [1, 1, 0]
            ],
            [
                [1, 1, 1, 0],
                [0, 0, 1, 1]
            ],
            [
                [0, 1, 1, 1],
                [1, 1, 0, 0]
            ],
            [
                [0, 0, 1, 0],
                [1, 1, 1, 1]
            ],
            [
                [0, 1, 0, 0],
                [1, 1, 1, 1]
            ],
            [
                [1, 1, 1, 1, 1]
            ],
            [
                [0, 1, 1],
                [0, 1, 0],
                [1, 1, 0]
            ],
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 1]
            ]
        ]

    elif settings_values.mode == 0:
        return [
            [
                [0, 1],
                [1, 1]
            ],
            [
                [1, 1, 1]
            ]
        ]
    else:
        return [
            [
                [0, 1, 0],
                [1, 1, 1]
            ],
            [
                [1, 0, 0],
                [1, 1, 1]
            ],
            [
                [0, 0, 1],
                [1, 1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 1, 1],
                [1, 1, 0]
            ],
            [
                [1, 1, 1, 1]
            ]
        ]

def get_centers():
    if settings_values.mode == 2:
        return [
            (1, 1),
            (1, 1),
            None,
            (1, 1),
            (2, 1),
            (1, 1),
            (1, 1),
            (1, 1),
            (1, 0),
            (1, 1),
            (1, 1),
            (2, 0),
            (1, 0),
            (2, 1),
            (1, 1),
            (2, 0),
            (1, 1),
            (1, 1)

        ]
    elif settings_values.mode == 0:
        return [
            (1, 1),
            (1, 0),
        ]
    else:
        return [
            (1, 1),
            (1, 1),
            (1, 1),
            None,
            (1, 1),
            (1, 1),
            (1, 0)

        ]
def generate_bag(x, y, game, random_x_coord=False):
    bag = []
    available_templates = [i for i in range(len(get_template()))]
    while len(available_templates) != 0:
        template_idx = random.randrange(len(get_template()))
        if template_idx in available_templates:
            if random_x_coord:
                bag.append(generate_random_structure(random.randint(0, game.COLUMNS - 4), y, game, template_idx=template_idx))
            else:
                bag.append(generate_random_structure(x, y, game, template_idx=template_idx))
            available_templates.remove(template_idx)
    return bag

def generate_random_structure(x, y, game, template_idx=None):
    blocks = []
    outline_blocks = []
    if settings_values.block_colors == 0:
        color_idx = random.randrange(len(colors))
        color = colors[color_idx]
        border_color = border_colors[color_idx]
    elif settings_values.block_colors == 1:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        border_color = (0, 0, 0)
        color_idx = None
    else:
        color = (40, 40, 40)
        border_color = (90, 90, 90)
        color_idx = None
    if template_idx is None:
        template_idx = random.randrange(len(get_template()))
    template = get_template()[template_idx]
    center = get_centers()[template_idx]
    for r, row in enumerate(template):
        for c, value in enumerate(row):
            if value == 1:
                if game.map[y + r][x + c] == 2:
                    game.game_over = True
                tetris_block = block.Block(x + c, y + r, game, color, border_color)
                blocks.append(tetris_block)
                game.blocks[(x + c, y + r)] = tetris_block
                outline_blocks.append(block.Block(x + c, y + r, game, game.tile_color, color))

    if center is not None:
        return Structure(game, blocks, outline_blocks, color_idx, (x + center[0], y + center[1]), template_idx, color, border_color)
    else:
        return Structure(game, blocks, outline_blocks, color_idx, None, template_idx, color, border_color)

class Structure:
    def __init__(self, game, blocks, outline_blocks, color_idx, center, template_idx, color, border_color):
        self.game = game
        self.blocks = blocks
        self.color_idx = color_idx
        self.can_move = True
        self.can_move_left = True
        self.can_move_right = True
        self.center = center
        self.outline_blocks = outline_blocks
        self.template_idx = template_idx
        self.color = color
        self.border_color = border_color

    def render(self):
        if self.can_move:
            for block in self.outline_blocks:
                block.render()
        if self.game.debug is False:
            for block in self.blocks:
                block.render()

    def preview(self, x, y):
        for block in self.blocks:
            block.preview(x, y)

    def reset(self, x, y):
        self.blocks = []
        self.outline_blocks = []
        template = get_template()[self.template_idx]
        self.center = get_centers()[self.template_idx]
        if self.center is not None:
            self.center = (x + self.center[0], y + self.center[1])
        for r, row in enumerate(template):
            for c, value in enumerate(row):
                if value == 1:
                    if self.game.map[y + r][x + c] == 2:
                        self.game.game_over = True
                    tetris_block = block.Block(x + c, y + r, self.game, self.color, self.border_color)
                    self.blocks.append(tetris_block)
                    self.game.blocks[(x + c, y + r)] = tetris_block
                    self.outline_blocks.append(block.Block(x + c, y + r, self.game, self.game.tile_color, self.color))


    def move(self, p, q):
        if self.can_move and self.check_if_move_possible(p, q):
            for block in self.blocks:
                self.game.map[block.y][block.x] = 0
                self.game.blocks[(block.x, block.y)] = None
                block.x += q
                block.y += p
                self.game.blocks[(block.x, block.y)] = block
                self.game.map[block.y][block.x] = 1
                # self.game.map[block.y][block.x] = 0
                # if block.x + q in range(self.game.COLUMNS) and self.game.map[block.y][block.x + q] != 2:
                #     block.x += q
                # if block.y + p >= 0 and block.y + p < self.game.ROWS - 1 and self.game.map[block.y + p + 1][block.x] != 2:
                #     block.y += p
                # else:
                #     block.y += p
                #     self.can_move = False
                # self.game.map[block.y][block.x] = 1
            if self.center is not None:
                self.center = (self.center[0] + q, self.center[1] + p)
            self.calculate_outline()

    def calculate_outline(self):
        if self.can_move:
            y = 0
            while self.check_if_move_possible(y, 0, True):
                y += 1
            y -= 1

            if settings_values.mode == 0:
                block_num = 3
            elif settings_values.mode == 2:
                block_num = 5
            else:
                block_num = 4
            for block_idx in range(block_num):
                outline_y = self.blocks[block_idx].y + y
                if outline_y < self.game.ROWS:
                    self.outline_blocks[block_idx].y = outline_y
                    self.outline_blocks[block_idx].x = self.blocks[block_idx].x
    def check_if_move_possible(self, p, q, outline=False):
        possible = True
        for block in self.blocks:
            if block.x + q in range(self.game.COLUMNS) and self.game.map[block.y][block.x + q] == 2:
                possible = False
            elif block.x + q not in range(self.game.COLUMNS):
                possible = False

            if block.y + p in range(self.game.ROWS) and self.game.map[block.y + p][block.x] == 2:
                possible = False
                if outline is False:
                    self.can_move = False
            elif block.y + p not in range(self.game.ROWS):
                possible = False
                if outline is False:
                    self.can_move = False
        return possible

    def rotate(self):
        if self.center is not None and self.check_if_rotation_possible():
            for block in self.blocks:
                point = (block.x, block.y)
                rotated_x = self.center[0] + (point[1] - self.center[1])
                rotated_y = self.center[1] - (point[0] - self.center[0])

                self.game.map[block.y][block.x] = 0
                self.game.blocks[(block.x, block.y)] = None
                self.game.map[rotated_y][rotated_x] = 1
                block.x = rotated_x
                block.y = rotated_y
                self.game.blocks[(block.x, block.y)] = block
            self.calculate_outline()
    def check_if_rotation_possible(self):
        possible = True
        for block in self.blocks:
            point = (block.x, block.y)
            rotated_x = self.center[0] + (point[1] - self.center[1])
            rotated_y = self.center[1] - (point[0] - self.center[0])
            try: # checks if the rotated coordinates aren't outside the map or a placed block
                if rotated_y not in range(self.game.ROWS) or rotated_x not in range(self.game.COLUMNS) or self.game.map[rotated_y][rotated_x] == 2:
                    possible = False
            except:
                possible = False
                break
        return possible

    def place(self):
        for block in self.blocks:
            for _ in range(20):
                speed = random.randint(60, 300)
                direction = pygame.math.Vector2(0, -1)
                self.game.particles.add(particles.Particle(self.game.particles, (random.uniform(-self.game.tile_size/2, self.game.tile_size/2) + self.game.x_offset + block.x * self.game.tile_size + self.game.tile_size/2, random.uniform(-self.game.tile_size/2, self.game.tile_size/2) + block.y * self.game.tile_size + self.game.tile_size/2), self.color, direction, speed))

            self.game.map[block.y][block.x] = 2
            self.game.blocks[(block.x, block.y)] = block
            block.moving = False