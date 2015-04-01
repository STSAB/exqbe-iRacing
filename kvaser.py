import sink
import sys
import struct
from ctypes import *

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

    def _transmit(self, address, data):
        ctypes_data = (c_ubyte * 8).from_buffer_copy(data)
        res = self.dll.canWrite(
            c_int(self.handle),
            c_int(address),
            pointer(ctypes_data),
            c_int(8),
            c_int(0))

    def sink(self, telemetry):
        msg = struct.pack('hhhh',
                          telemetry[sink.TYPE_RPM],
                          telemetry[sink.TYPE_THROTTLE] / 0.001,
                          telemetry[sink.TYPE_MANIFOLD_PRESSURE] / 0.1,
                          0)
        self._transmit(0x520, msg)

        msg = struct.pack('hhhh',
                          0,
                          0,
                          0,
                          telemetry[sink.TYPE_SPEED] / 0.1)
        self._transmit(0x522, msg)

        msg = struct.pack('hhhh',
                          0,
                          0,
                          0,
                          telemetry[sink.TYPE_BRAKE] / 0.0001)
        self._transmit(0x524, msg)

        msg = struct.pack('hhhh',
                          telemetry[sink.TYPE_VOLTAGE] / 0.01,
                          telemetry[sink.TYPE_OIL_PRESSURE] / 0.1,
                          telemetry[sink.TYPE_OIL_TEMP] / 0.1,
                          telemetry[sink.TYPE_WATER_TEMP] / 0.1)
        self._transmit(0x530, msg)

        msg = struct.pack('hhhh',
                          0,
                          telemetry[sink.TYPE_LONG_ACCEL] / 0.1,
                          telemetry[sink.TYPE_LAT_ACCEL] / 0.1,
                          0)
        self._transmit(0x531, msg)