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
        dataSplit = data.decode('utf-8')[0:-2]
        print(dataSplit)
        if dataSplit == "snare":
            mixer.music.load("DrumSamples/CyCdh_K3Snr-01.wav")
            mixer.music.play()

        if dataSplit == "bass":
            mixer.music.load("DrumSamples/CyCdh_K3Kick-01.wav")
            mixer.music.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
