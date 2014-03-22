import serial


class Exhub:

    def __init__(self, port):
        self.serial = serial.Serial(port, baudrate=19200)

    def send(self, address, value):
        self.serial.write('{} {}\n'.format(address, value))

    def blocking_read(self):
        """
        Read until a line has been received.
        If the remote Exhub follows protocol it will send the address of the sensor it wants to read, followed
        by a newline. '123\n' cast to int will become just 123.
        """
        return int(self.serial.readline())
