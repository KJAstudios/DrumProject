import time

import pygame
from pygame import mixer
import DrumBrain


def main():
    pygameSetup()
    mixer.music.set_volume(1)

    # start the serial connection
    serial_connection = DrumBrain.serialConnection()
    serial_connection.startSerial()

    # variable to control the main loop
    running = True

    while running:
        data = serial_connection.readData()
        #print(data)
        dataSplit = data.decode('utf-8')[0:-2]
        print(dataSplit)
        if dataSplit == "snare":
            mixer.Channel(0).play(mixer.Sound("DrumSamples/CyCdh_K3Snr-01.wav"))
            #print("snare playing at time " + str(time.time_ns() / 1000000))

        if dataSplit == "bass":
            mixer.Channel(1).play(mixer.Sound("DrumSamples/CyCdh_K3Kick-01.wav"))
           # print("bass drum playing at time " +str(time.time_ns() / 1000000))

        if dataSplit == "c4":
            mixer.Channel(2).play(mixer.Sound("DrumSamples/CyCdh_K3ClHat-01.wav"))
            #print("hihat playing at time " + str(time.time_ns() / 1000000))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    print("main loop left")
    # close the serial connection
    serial_connection.closeSerial()

    # close pygame
    pygame.display.quit()


def pygameSetup():
    # init pygame
    pygame.init()

    # set the window name
    pygame.display.set_caption("minimal program")

    # create a surface on the screen
    screen = pygame.display.set_mode((500, 500))

    # start the mixer
    mixer.init()


# run the main function only if this module is executed as the main screen
if __name__ == "__main__":
    main()
