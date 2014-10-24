from abc import abstractmethod

TYPE_RPM = 0
TYPE_SPEED = 1
TYPE_WATER_TEMP = 2
TYPE_OIL_TEMP = 3
TYPE_OIL_PRESSURE = 4
TYPE_VOLTAGE = 5
TYPE_MANIFOLD_PRESSURE = 6
TYPE_FUEL_LEVEL = 7
TYPE_LONG_ACCEL = 8
TYPE_LAT_ACCEL = 9
TYPE_THROTTLE = 10
TYPE_BRAKE = 11

class Sink(object):
    @abstractmethod
    def sink(self, key, value):
        pass

