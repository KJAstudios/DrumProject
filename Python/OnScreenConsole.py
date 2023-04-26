import pygame


class OnScreenConsole:

    def __init__(self, initial_pos, font, screen):
        self.screen = screen
        self.font = font
        self.text_surface = pygame.Surface((500, 480))
        self.rect = self.text_surface.get_rect()
        pygame.display.update(self.rect)
        self.x = initial_pos[0]
        self.y = initial_pos[1]
        self.next_line_pos = self.rect.height - 36
        self.log("Console Started")

    def log(self, message):
        print(message)
        message.strip()
        message_surface = self.font.render(message, True, (0, 0, 0))
        self.draw_text(message_surface)

    def draw_text(self, message_surface):
        # Render the message onto the
        copy_surface = self.text_surface.copy()
        self.text_surface.fill((255, 255, 255))
        self.text_surface.blit(copy_surface, (0, -36))
        self.text_surface.blit(message_surface, (0, self.next_line_pos))
        self.screen.blit(self.text_surface, (self.x, self.y))
        pygame.display.update(self.rect)
