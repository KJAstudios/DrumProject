import DrumCommands


class ThresholdUpdateManager:
    def __init__(self, initial_pos, selector_factory, serial_connection, console):
        self.position = initial_pos

        self.serial_connection = serial_connection
        self.console = console

        self.height = 200
        self.current_channel = 0

        self.channel_threshold = DrumCommands.request_threshold(0, serial_connection, console)

        self.channel_selector = selector_factory.create_channel_selector(initial_pos, current_value=0, max_value=5)
        self.channel_selector.on_value_changed = self.on_channel_change
        self.threshold_selector = selector_factory.create_threshold_selector((initial_pos[0], initial_pos[1] + 100),
                                                                             current_value=int(self.channel_threshold))

    def process_mouse_click(self, mouse_pos):
        self.channel_selector.process_mouse_click(mouse_pos)
        self.threshold_selector.process_mouse_click(mouse_pos)

    def on_channel_change(self, new_channel):
        if new_channel != self.current_channel:
            self.channel_threshold = DrumCommands.request_threshold(new_channel, self.serial_connection, self.console)
            self.current_channel = new_channel
            self.threshold_selector.update_threshold(self.current_channel, self.channel_threshold)
