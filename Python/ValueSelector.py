import pygame


class ValueSelector:
    def __init__(self, header_message, initial_pos, font, screen):
        self.red = (163, 2, 2)
        self.white = (255, 255, 255)
        self.height = 100
        self.button_height = self.height / 2
        self.width = 300
        self.button_width = 300 / 4
        self.button_y = self.height / 2

        self.screen = screen
        self.position = initial_pos
        self.font = font

        self.main_surf = pygame.Surface((self.width, self.height))
        self.rect = self.main_surf.get_rect()

        self.left_button_surf = pygame.Surface((self.button_width, self.button_height))
        self.left_button_surf.fill(self.red)

        self.right_button_surf = pygame.Surface((self.button_width, self.button_height))
        self.right_button_surf.fill(self.red)

        self.header = self.font.render(header_message, True, (0, 0, 0))
        self.value = self.font.render('3', True, (0, 0, 0))

        self.render_to_screen()

    def check_input(self):
        return

    def on_left_button(self):
        return

    def on_right_button(self):
        return

    def render_to_screen(self):
        self.main_surf.fill(self.white)
        self.main_surf.blit(self.header, (0, self.button_y / 4))
        self.main_surf.blit(self.left_button_surf, (0, self.button_y))
        self.main_surf.blit(self.right_button_surf, (self.width - self.button_width, self.button_y))
        self.main_surf.blit(self.value, (self.width / 2, self.button_y + (self.button_y / 4)))
        self.screen.blit(self.main_surf, self.position)
        pygame.display.update(self.rect)
