import DrumCommandTypes
from ValueSelector import ValueSelector


# TODO add channel names
class ChannelSelector(ValueSelector):
    def __init__(self, initial_pos, font, screen, serial_connection, console,
                 current_value=0, max_value=1000, command_type=DrumCommandTypes.NONE):
        super().__init__("Channel", initial_pos, font, screen, serial_connection, console,
                         current_value, max_value, command_type)
        self.on_value_changed = None

    def on_left_button(self):
        super().on_left_button()
        if self.on_value_changed is not None:
            self.on_value_changed(self.current_value)

    def on_right_button(self):
        super().on_right_button()
        if self.on_value_changed is not None:
            self.on_value_changed(self.current_value)
