def send_new_scan_time(new_scan_time, serial_connection, console):
    console.log(f"Sending new scan time: {new_scan_time}")
    serial_connection.send_data(f"scanTime:{new_scan_time}")
    wait_for_message("New Scan Time", serial_connection, console)


def send_new_threshold(new_threshold, channel_index, serial_connection, console):
    console.log(f"sending new threshold {new_threshold} for channel {channel_index}")
    serial_connection.send_data(f"threshold:{channel_index}:{new_threshold}")
    wait_for_message("New Threshold", serial_connection, console)


def wait_for_message(message, serial_connection, console):
    # wait for the command to execute
    command_processed = False
    while command_processed is False:
        startup_message = serial_connection.read_data()
        if startup_message is not None:
            startup_message = startup_message.decode('utf-8')[0:-2]
            console.log(startup_message)
            startup_split = startup_message.split(':')
            if startup_split[0] == message:
                command_processed = True
    console.log("")


def request_threshold(channel_index, serial_connection, console):
    console.log(f"requesting threshold for channel {channel_index}")
    serial_connection.send_data(f"requestThreshold:{channel_index}")
    response = wait_for_response(f"Channel {channel_index} Threshold", serial_connection, console)
    return int(response)


def wait_for_response(message, serial_connection, console):
    command_processed = False
    while command_processed is False:
        startup_message = serial_connection.read_data()
        if startup_message is not None:
            startup_message = startup_message.decode('utf-8')[0:-2]
            console.log(startup_message)
            startup_split = startup_message.split(':')
            if startup_split[0] == message:
                return startup_split[1]
            elif startup_split == "Invalid Channel Requested":
                return None
