import platform
import serial


class SerialConnection:
    serConnection = None
    port = ""

    def __init__(self, console):
        self.console = console
        self.console.log("Serial Connection Object Created")

    def determine_environment(self):
        environment = platform.system()
        if environment == "Linux":
            self.port = "/dev/ttyACM0"
        elif environment == "Windows":
            self.port = "COM6"

    # create the serial connection
    def start_serial(self):
        self.determine_environment()
        self.console.log("Serial Connection Started")
        self.serConnection = serial.Serial(port=self.port,
                                           baudrate=9600,
                                           parity=serial.PARITY_NONE,
                                           stopbits=serial.STOPBITS_ONE,
                                           bytesize=serial.EIGHTBITS,
                                           timeout=None)
        self.console.log(f"{self.serConnection.is_open}")

    def send_data(self, data):
        self.console.log("sending data: " + data)
        data = data.encode('utf-8')
        self.serConnection.write(data)

    def read_data(self):
        # self.console.log(self.serConnection.is_open)
        if self.serConnection is not None:
            data = self.serConnection.readline()
            return data

    # close the serial connection
    def close_serial(self):
        self.console.log("Serial Connection Closing")
        if self.serConnection is not None:
            self.serConnection.close()
