import platform
import serial
import main


class SerialConnection:
    serConnection = None
    port = ""

    def __init__(self):
        main.console.log("Serial Connection Object Created")

    def determine_environment(self):
        environment = platform.system()
        if environment == "Linux":
            self.port = "/dev/ttyACM0"
        elif environment == "Windows":
            self.port = "COM6"

    # create the serial connection
    def start_serial(self):
        self.determine_environment()
        main.console.log("Serial Connection Started")
        self.serConnection = serial.Serial(port=self.port,
                                           baudrate=9600,
                                           parity=serial.PARITY_NONE,
                                           stopbits=serial.STOPBITS_ONE,
                                           bytesize=serial.EIGHTBITS,
                                           timeout=None)
        main.console.log(f"{self.serConnection.is_open}")

    def send_data(self, data):
        main.console.log("sending data: " + data)
        data = data.encode('utf-8')
        self.serConnection.write(data)

    def read_data(self):
        # main.console.log(self.serConnection.is_open)
        if self.serConnection is not None:
            data = self.serConnection.readline()
            return data

    # close the serial connection
    def close_serial(self):
        main.console.log("Serial Connection Closing")
        if self.serConnection is not None:
            self.serConnection.close()
