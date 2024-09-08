import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, app):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.app = app
        self.dragging = False

    def return_rect(self):
        return self.rect

    def render(self):
        pygame.draw.rect(self.app.screen, (200, 200, 200), self.rect)
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        pygame.draw.circle(self.app.screen, (100, 100, 100), (int(handle_x), self.rect.centery), self.rect.height // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            self.value = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
            self.value = max(self.min_val, min(self.max_val, self.value))