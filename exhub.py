import serial
import logging

class Exhub:

    def __init__(self, port):
        self.serial = serial.Serial(port, baudrate=38400)

    def reset(self):
        # Flush hub to avoid operating on large amounts of cached data which would overwhelm the hub
        self.flush()
        self.send_ack()

    def send(self, address, value):
        self.serial.write('{} {}'.format(address, value))

    def send_ack(self):
        self.serial.write('\n')

    def blocking_read(self):
        """
        Read until a line has been received.
        If the remote Exhub follows protocol it will send the address of the sensor it wants to read, followed
        by a newline. '123\n' cast to int will become just 123. The address is currently in decimal form, not in ASCII
        form. If the exhub wants to read a sensor with an id 10 it will send '\0x0A\n', not '10\n\. This will change.
        """
        res = self.serial.readline()
        return ord(res[0])

    def flush(self):
        self.serial.flushInput()
