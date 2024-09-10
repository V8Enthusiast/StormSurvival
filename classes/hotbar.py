import pygame
import images

class Hotbar:
    def __init__(self, game, num_slots=5):
        self.game = game
        self.num_slots = num_slots
        self.selected_slot = 0
        self.items = [None] * num_slots
        self.slot_width = 50
        self.slot_height = 50
        self.margin = 10
        self.font = pygame.font.Font(None, 36)

    def render(self):
        for i in range(self.num_slots):
            x = self.margin + i * (self.slot_width + self.margin)
            y = self.game.app.height - self.slot_height - self.margin
            color = (255, 255, 255) if i == self.selected_slot else (100, 100, 100)
            pygame.draw.rect(self.game.screen, color, (x, y, self.slot_width, self.slot_height), 2)
            if self.items[i]:
                if self.items[i] == "Gun":
                    gun_image_scaled = pygame.transform.scale(images.gun, (self.slot_width - 10, self.slot_height - 10))
                    self.game.screen.blit(gun_image_scaled, (x + 5, y + 5))
                    ammo_text = self.font.render(str(self.game.player.ammo), True, (255, 255, 255))
                    self.game.screen.blit(ammo_text, (x + 5, y + 5))
                else:
                    item_text = self.font.render(self.items[i], True, (255, 255, 255))
                    self.game.screen.blit(item_text, (x + 5, y + 5))

    def select_slot(self, slot):
        if 0 <= slot < self.num_slots:
            self.selected_slot = slot

    def add_item(self, item, slot):
        if 0 <= slot < self.num_slots:
            self.items[slot] = item