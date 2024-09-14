import pygame

class WeaponSelectionUI:
    def __init__(self, game, weapons, ammothing):
        self.ammothing = ammothing
        self.ammo = self.ammothing.ammo
        self.game = game
        self.weapons = weapons
        self.font = pygame.font.Font(None, 36)
        self.selected_weapon = None
        self.margin_x = 100
        self.margin_y = 50
        self.start_x = (self.game.app.width - self.calculate_total_width()) // 2

    def calculate_total_width(self):
        return sum(weapon.image.get_width() for weapon in self.weapons if weapon != self.ammothing) + self.margin_x * (len(self.weapons) - 1)

    def render(self):
        ui_surface = pygame.Surface((self.game.app.width, self.game.app.height), pygame.SRCALPHA)
        ui_surface.fill((0, 0, 0, 150))

        for i, weapon in enumerate(self.weapons):
            if weapon == self.ammothing:
                continue

            weapon_image = weapon.image
            image_x = self.start_x + i * (weapon_image.get_width() + self.margin_x)
            image_y = self.game.app.height // 2 - weapon_image.get_height() // 2 - self.margin_y
            ui_surface.blit(weapon_image, (image_x, image_y))

            weapon_text = self.font.render(weapon.__class__.__name__, True, (255, 255, 255))
            text_x = image_x + weapon_image.get_width() // 2 - weapon_text.get_width() // 2
            text_y = image_y + weapon_image.get_height() + 10
            ui_surface.blit(weapon_text, (text_x, text_y))

        self.game.screen.blit(ui_surface, (0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            for i, weapon in enumerate(self.weapons):
                if weapon == self.ammothing:
                    continue

                weapon_image = weapon.image
                image_x = self.start_x + i * (weapon_image.get_width() + self.margin_x)
                image_y = self.game.app.height // 2 - weapon_image.get_height() // 2 - self.margin_y
                image_rect = pygame.Rect(image_x, image_y, weapon_image.get_width(), weapon_image.get_height())
                if image_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_weapon = weapon
                    self.game.hotbar.remove_item_by_item(self.ammothing)
                    return weapon
        return None

    def return_ammothing_ammo(self):
        return self.ammo