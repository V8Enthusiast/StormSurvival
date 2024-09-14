import pygame

class WeaponSelectionUI:
    def __init__(self, game, weapons):
        self.game = game
        self.weapons = weapons
        self.font = pygame.font.Font(None, 36)
        self.selected_weapon = None

    def render(self):
        ui_surface = pygame.Surface((self.game.app.width, self.game.app.height), pygame.SRCALPHA)
        ui_surface.fill((0, 0, 0, 150))

        for i, weapon in enumerate(self.weapons):
            weapon_text = self.font.render(weapon.__class__.__name__, True, (255, 255, 255))
            ui_surface.blit(weapon_text, (self.game.app.width // 2 - weapon_text.get_width() // 2, 50 + i * 40))

        self.game.screen.blit(ui_surface, (0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            for i, weapon in enumerate(self.weapons):
                weapon_text = self.font.render(weapon.__class__.__name__, True, (255, 255, 255))
                text_rect = weapon_text.get_rect()
                text_rect.topleft = (self.game.app.width // 2 - weapon_text.get_width() // 2, 50 + i * 40)
                if text_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_weapon = weapon
                    return weapon
        return None