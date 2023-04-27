import DrumCommandTypes
import DrumCommands
from ValueSelector import ValueSelector


class ThresholdSelector(ValueSelector):
    def __init__(self, initial_pos, font, screen, serial_connection, console,
                 current_value=0, max_value=1000):
        super().__init__("Threshold", initial_pos, font, screen, serial_connection, console,
                         current_value, max_value, command_type=DrumCommandTypes.THRESHOLD)
        self.channel = 0

    def update_threshold(self, channel, threshold):
        self.channel = channel
        self.current_value = threshold
        self.render_to_screen()

    def send_command(self):
        if self.command_type == DrumCommandTypes.THRESHOLD:
            DrumCommands.send_new_threshold(self.current_value, self.channel, self.serial_connection, self.console)