import pygame

import DrumCommandTypes
import DrumCommands


class ValueSelectorFactory:
    def __init__(self, font, screen, serial_connection, console):
        self.font = font
        self.screen = screen
        self.serial_connection = serial_connection
        self.console = console

    def create_selector(self, header_message, initial_pos, current_value=0, max_value=1000,
                        command_type=DrumCommandTypes.NONE):
        return ValueSelector(header_message, initial_pos, self.font, self.screen, self.serial_connection, self.console,
                             current_value, max_value, command_type)


class ValueSelector:
    def __init__(self, header_message, initial_pos, font, screen, serial_connection, console,
                 current_value=0, max_value=1000, command_type=DrumCommandTypes.NONE):
        self.red = (163, 2, 2)
        self.white = (255, 255, 255)
        self.height = 100
        self.button_height = self.height / 2
        self.width = 300
        self.button_width = 300 / 4
        self.button_y = self.height / 2
        self.right_button_x = self.width - self.button_width

        self.screen = screen
        self.font = font
        self.serial_connection = serial_connection
        self.console = console

        self.position = initial_pos
        self.current_value = current_value
        self.max_value = max_value
        self.command_type = command_type

        self.main_surf = pygame.Surface((self.width, self.height))
        self.rect = self.main_surf.get_rect()

        self.left_button_surf = pygame.Surface((self.button_width, self.button_height))
        self.left_button_surf.fill(self.red)

        self.right_button_surf = pygame.Surface((self.button_width, self.button_height))
        self.right_button_surf.fill(self.red)

        self.header = self.font.render(header_message, True, (0, 0, 0))
        self.value = self.font.render(f"{self.current_value}", True, (0, 0, 0))

        self.render_to_screen()

    def process_mouse_click(self, mouse_pos):
        if self.position[0] <= mouse_pos[0] <= self.position[0] + self.button_width \
                and self.position[1] + self.button_y < mouse_pos[1] < self.position[1] + self.height:
            #self.console.log("left button clicked")
            self.on_left_button()
        elif self.position[0] + self.right_button_x <= mouse_pos[0] <= self.position[0] + self.width \
                and self.position[1] + self.button_y < mouse_pos[1] < self.position[1] + self.height:
            #self.console.log("right button clicked")
            self.on_right_button()

    def on_left_button(self):
        self.current_value -= 1
        self.render_to_screen()

    def on_right_button(self):
        self.current_value += 1
        self.render_to_screen()

    def send_command(self):
        if self.command_type == DrumCommandTypes.SCAN_TIME:
            DrumCommands.send_new_scan_time(self.value, self.serial_connection, self.console)
        elif self.command_type == DrumCommandTypes.THRESHOLD:
            return

    def render_to_screen(self):
        self.main_surf.fill(self.white)
        self.main_surf.blit(self.header, (0, self.button_y / 4))
        self.main_surf.blit(self.left_button_surf, (0, self.button_y))
        self.main_surf.blit(self.right_button_surf, (self.right_button_x, self.button_y))
        self.value = self.font.render(f"{self.current_value}", True, (0, 0, 0))
        self.main_surf.blit(self.value, (self.width / 2, self.button_y + (self.button_y / 4)))
        self.screen.blit(self.main_surf, self.position)
        pygame.display.update(self.rect)
