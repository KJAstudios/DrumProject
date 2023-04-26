import pygame
from pygame import mixer

import DrumCommands
import SerialConnection
from OnScreenConsole import OnScreenConsole
from ValueSelector import ValueSelector

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
channel_selector = ValueSelector("Selected Channel", (500, 0), font, screen)
threshold_selector = ValueSelector("Threshold", (500, channel_selector.height), font, screen)
scan_time_selector = ValueSelector("Scan Time", (500, channel_selector.height + threshold_selector.height), font,
                                   screen)

# start the mixer
mixer.init()


def main():
    mixer.music.set_volume(1)

    # start the serial connection
    serial_connection = SerialConnection.SerialConnection(get_console())
    serial_connection.start_serial()

    wait_for_startup(serial_connection)
    settings_setup(serial_connection)

    # variable to control the main loop
    running = True

    while running:
        pygame.display.flip()
        data = serial_connection.read_data()
        dataSplit = data.decode('utf-8')[0:-2]
        get_console().log(dataSplit)
        if dataSplit == "snare":
            mixer.Channel(0).play(mixer.Sound("DrumSamples/CyCdh_K3Snr-01.wav"))
            # get_console().log("snare playing at time " + str(time.time_ns() / 1000000))

        if dataSplit == "bass":
            mixer.Channel(1).play(mixer.Sound("DrumSamples/CyCdh_K3Kick-01.wav"))
            # get_console().log("bass drum playing at time " +str(time.time_ns() / 1000000))

        if dataSplit == "c4":
            mixer.Channel(2).play(mixer.Sound("DrumSamples/CyCdh_K3ClHat-01.wav"))
            # get_console().log("hihat playing at time " + str(time.time_ns() / 1000000))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    get_console().log("main loop left")
    # close the serial connection
    serial_connection.close_serial()

    # close pygame
    pygame.display.quit()


def wait_for_startup(serial_connection):
    connection_started = False

    while connection_started is False:
        startup_message = serial_connection.read_data()
        startup_message = startup_message.decode('utf-8')[0:-2]
        get_console().log(startup_message)
        if startup_message == "Serial started":
            connection_started = True


def settings_setup(serial_connection):
    DrumCommands.send_new_scan_time(51, serial_connection, get_console())
    DrumCommands.send_new_threshold(45, 3, serial_connection, get_console())


def get_console():
    global console
    return console


# run the main function only if this module is executed as the main screen
if __name__ == "__main__":
    main()
