import sink
import sys
import struct
from ctypes import *

INDEX_ADDRESS = 0
INDEX_MULTIPLIER = 1

MessageTypes = {
    sink.TYPE_RPM: (0x7D0, 1.0),
    sink.TYPE_SPEED: (0x7D1, 0.1),
    sink.TYPE_WATER_TEMP: (0x7D2, 0.1),
    sink.TYPE_OIL_TEMP: (0x7D3, 0.1),
    sink.TYPE_OIL_PRESSURE: (0x7D4, 0.01),
    sink.TYPE_VOLTAGE: (0x7D5, 0.01),
    sink.TYPE_MANIFOLD_PRESSURE: (0x7D6, 0.1),
    sink.TYPE_FUEL_LEVEL: (0x7D7, 1),
    sink.TYPE_LONG_ACCEL: (0x7D8, 0.01),
    sink.TYPE_LAT_ACCEL: (0x7D9, 0.01),
    sink.TYPE_THROTTLE: (0x7DA, 1),
    sink.TYPE_BRAKE: (0x7DB, 0.1)
}

# CANlib
MsgDataType = c_uint8 * 8


# Errors
class KvaserError(Exception):
    pass


class Kvaser(object):
    def __init__(self):
        if sys.platform.startswith('win'):
            self.dll = WinDLL('canlib32')
            self.dll.canInitializeLibrary()
        else:
            self.dll = CDLL('libcanlib.so')

        # Open CAN channel.
        self.handle = self.dll.canOpenChannel(c_int(0), c_int(0))
        res = self.dll.canBusOn(c_int(self.handle))
        if res < 0:
            raise KvaserError('Error initializing, {}'.format(res))

    def reset(self):
        pass

    def sink(self, telemetry):
        msg = struct.pack('hhh\0\0',
                          telemetry[sink.TYPE_RPM],
                          telemetry[sink.TYPE_THROTTLE] / 0.01,
                          telemetry[sink.TYPE_MANIFOLD_PRESSURE] / 0.1)
        res = self.dll.canWrite(c_int(self.handle), c_int(0x520), pointer(msg), c_int(8), c_int(0))
