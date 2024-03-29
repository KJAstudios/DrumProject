import pygame
from pygame import mixer

import DrumCommandTypes
import DrumCommands
import DrumSettings
import SerialConnection
from OnScreenConsole import OnScreenConsole
from ThresholdUpdateManager import ThresholdUpdateManager
from ValueSelectorFactory import ValueSelectorFactory


def wait_for_startup(serial_connection):
    connection_started = False

    while connection_started is False:
        startup_message = serial_connection.read_data()
        if startup_message is not None:
            startup_message = startup_message.decode('utf-8')[0:-2]
            get_console().log(startup_message)
            if startup_message == "Serial started":
                connection_started = True


def settings_setup(serial_connection):
    DrumCommands.send_new_scan_time(DrumSettings.scan_time, serial_connection, get_console())
    channel = 0
    for threshold in DrumSettings.channel_thresholds:
        DrumCommands.send_new_threshold(threshold, channel, serial_connection, get_console())
        channel += 1


def main():
    mixer.music.set_volume(1)

    # variable to control the main loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                process_mouse_click(event)
            if event.type == pygame.MOUSEBUTTONUP:
                continue
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

        data = serial_connection.read_data()
        if data is not None:
            process_serial_message(data)

        pygame.display.flip()

    get_console().log("main loop left")
    # close the serial connection
    serial_connection.close_serial()

    # close pygame
    pygame.display.quit()


def process_serial_message(data):
    data = data.decode('utf-8')[0:-2]
    get_console().log(data)
    dataSplit = data.split(" ")[0]
    if dataSplit == "snare":
        mixer.Channel(0).play(mixer.Sound("DrumSamples/CyCdh_K3Snr-01.wav"))
        # get_console().log("snare playing at time " + str(time.time_ns() / 1000000))

    if dataSplit == "bass":
        mixer.Channel(1).play(mixer.Sound("DrumSamples/CyCdh_K3Kick-01.wav"))
        # get_console().log("bass drum playing at time " +str(time.time_ns() / 1000000))

    if dataSplit == "c4":
        mixer.Channel(2).play(mixer.Sound("DrumSamples/CyCdh_K3ClHat-01.wav"))
        # get_console().log("hihat playing at time " + str(time.time_ns() / 1000000))


def process_mouse_click(event):
    for listener in input_listeners:
        listener.process_mouse_click(event.pos)


def get_console():
    global console
    return console


# run the init outside of a function so that variables are declared globally
# init pygame
pygame.init()

# set the window name
pygame.display.set_caption("minimal program")

# create the screen
screen = pygame.display.set_mode((800, 480))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 20)
# create the program modules
console = OnScreenConsole((0, 0), font, screen)

# start the serial connection
serial_connection = SerialConnection.SerialConnection(get_console())
serial_connection.start_serial()

wait_for_startup(serial_connection)
settings_setup(serial_connection)

selector_factory = ValueSelectorFactory(font, screen, serial_connection, console)
channel_selector = ThresholdUpdateManager((500, 0), selector_factory, serial_connection, console)
scan_time_selector = selector_factory.create_selector("Scan Time",
                                                      (500, channel_selector.height),
                                                      current_value=51, command_type=DrumCommandTypes.SCAN_TIME)

input_listeners = (channel_selector, scan_time_selector)

# start the mixer
mixer.init()

main()
