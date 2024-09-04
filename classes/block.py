import pygame


class Block:
    def __init__(self, x, y, game, color, border_color):
        self.x = x
        self.y = y
        self.color = color
        self.border_color = border_color
        self.moving = True
        self.game = game
        self.game.map[self.y][self.x] = 1
    def render(self):
        if self.game.map[self.y][self.x] != 0 or self.moving:
            rect = pygame.Rect(self.game.x_offset + self.x * self.game.tile_size, self.game.y_offset + self.y * self.game.tile_size,
                               self.game.tile_size, self.game.tile_size)
            pygame.draw.rect(self.game.app.screen, self.color, rect)
            pygame.draw.rect(self.game.app.screen, self.border_color, rect, self.game.border)
    def preview(self, x, y):
        rect = pygame.Rect(x + self.x * self.game.tile_size,
                           y + self.y * self.game.tile_size,
                           self.game.tile_size, self.game.tile_size)
        pygame.draw.rect(self.game.app.screen, self.color, rect)
        pygame.draw.rect(self.game.app.screen, self.border_color, rect, self.game.border)