import pygame
import images
from classes import weapon

class Hotbar:
    def __init__(self, game, x, y, num_slots=5):
        self.game = game
        self.num_slots = num_slots
        self.selected_slot = 0
        self.items = [None] * num_slots
        self.slot_width = 50
        self.slot_height = 50
        self.slot_rects = []
        self.margin = 10
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 20)
        self.moved_item = None
        for i in range(num_slots):
            x = self.x + self.margin + i * (self.slot_width + self.margin)
            y = self.y
            rect = pygame.Rect(x, y, self.slot_width, self.slot_height)
            self.slot_rects.append(rect)

    def render(self):
        for i in range(self.num_slots):
            x = self.x + self.margin + i * (self.slot_width + self.margin)
            y = self.y
            color = (255, 255, 255) if i == self.selected_slot else (100, 100, 100)
            rect = self.slot_rects[i]
            pygame.draw.rect(self.game.screen, color, rect, 2)
            if self.items[i]:
                if isinstance(self.items[i], weapon.Weapon):
                    weapon_image = self.items[i].image
                    if self.moved_item is not None and self.moved_item == i:
                        mouse_pos = pygame.mouse.get_pos()
                        weapon_image_scaled = pygame.transform.scale(weapon_image, (self.slot_width, self.slot_height))
                        self.game.screen.blit(weapon_image_scaled, (mouse_pos[0], mouse_pos[1]))
                    else:
                        weapon_image_scaled = pygame.transform.scale(weapon_image, (self.slot_width - 10, self.slot_height - 10))
                        self.game.screen.blit(weapon_image_scaled, (x + 5, y + 5))
                        ammo_text = self.font.render(f"{str(self.items[i].ammo)}/{str(self.items[i].total_ammo)}", True, (255, 255, 255))
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
    def remove_item(self, slot):
        if 0 <= slot < self.num_slots:
            self.items[slot] = None

    def remove_item_by_item(self, item):
        for i in range(len(self.items)):
            if self.items[i] == item:
                self.items[i] = None
                break