import pygame, DrumBrain

def main():
    #init pygame
    pygame.init()
    
    # set the window name
    pygame.display.set_caption("minimal program")
    
    # create a surface on the screen
    screen = pygame.display.set_mode((500,500))
    
    # start the serial connection
    serial_connection = DrumBrain.serialConnection()
    serial_connection.startSerial()
    
    #variable to control the main loop
    running = True
    
    while running:
        serial_connection.readData()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    # close the serial connection
    serial_connection.closeSerial()
    
    # close pygame
    pygame.display.quit()
    
#run the main function only if this module is executed as the main screen
if __name__=="__main__":
    main()