import DrumCommandTypes
from ChannelSelector import ChannelSelector
from ThresholdSelector import ThresholdSelector
from ValueSelector import ValueSelector


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

    def create_channel_selector(self, initial_pos, current_value=0, max_value=5):
        return ChannelSelector(initial_pos, self.font, self.screen, self.serial_connection,
                               self.console,
                               current_value, max_value)

    def create_threshold_selector(self, initial_pos, current_value, max_value=1000):
        return ThresholdSelector(initial_pos, self.font, self.screen, self.serial_connection,
                                 self.console, current_value, max_value)
