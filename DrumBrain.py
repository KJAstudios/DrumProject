import serial

class serialConnection:
    serConnection = None
    
    def __init__(self):
        print("Serial Connection Object Created")

    # create the serial connection
    def startSerial(self):
        print("Serial Connection Started")
        self.serConnection = serial.Serial(port='/dev/ttyACM0',
                                baudrate = 9000,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=None)
        print (self.serConnection.is_open)


    def readData(self):
        print(self.serConnection.is_open)
        if self.serConnection != None:
            print(self.serConnection.readline())

    # close the serial connection
    def closeSerial(self):
        print("Serial Connection Closing")
        if self.serConnection != None:
            self.serConnection.close()
