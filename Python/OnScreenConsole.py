import pygame


class OnScreenConsole:

    def __init__(self, game_screen, initial_pos):
        self.screen = game_screen
        self.font = pygame.font.SysFont("Helvetica", 20)
        self.text_surface = pygame.Surface((200, 500))
        self.x = initial_pos[0]
        self.y = initial_pos[1]
        self.next_line_pos = initial_pos[1]
        self.log("Console Started")

    def log(self, message):
        print(message)
        message_surface = self.font.render(message, True, (0, 0, 0), (255, 255, 255))
        self.draw_text(message_surface)

    def draw_text(self, message_surface):
        # Render the message onto the
        self.text_surface.blit(message_surface, (0, self.next_line_pos))
        self.next_line_pos += 36
        self.update_console()

    def update_console(self):
        self.screen.blit(self.text_surface, (self.x, self.y))
        pygame.display.update()
