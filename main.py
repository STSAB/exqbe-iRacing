import kvaser
from api import api

import logging
import platform
import os
import mmap
import sink
import time
import sched

Sensors = {
    sink.TYPE_RPM: {'name': 'RPM', 'frequency': 10},
    sink.TYPE_SPEED: {'name': 'Speed', 'frequency': 5},
    sink.TYPE_WATER_TEMP: {'name': 'WaterTemp', 'frequency': 1},
    sink.TYPE_OIL_TEMP: {'name': 'OilTemp', 'frequency': 1},
    sink.TYPE_OIL_PRESSURE: {'name': 'OilPress', 'frequency': 5},
    sink.TYPE_VOLTAGE: {'name': 'Voltage', 'frequency': 1},
    sink.TYPE_MANIFOLD_PRESSURE: {'name': 'ManifoldPress', 'frequency': 5},
    sink.TYPE_LONG_ACCEL: {'name': 'LongAccel', 'frequency': 2},
    sink.TYPE_LAT_ACCEL: {'name': 'LatAccel', 'frequency': 2},
    sink.TYPE_THROTTLE: {'name': 'Throttle', 'frequency': 5},
    sink.TYPE_BRAKE: {'name': 'Brake', 'frequency': 5}
}


class iRacingBridge(object):
    def __init__(self):
        # iRacing memory mapped files only works on Windows systems. In case of a non-Windows system we can simulate
        # the behavior by mapping against a memory dump instead.
        mmap_item = None
        if platform.system() != 'Windows':
            mmap_file = os.path.join('api', 'tests', 'memorydump.dmp')
            mmap_f = open(mmap_file, 'r+b')
            mmap_item = mmap.mmap(mmap_f.fileno(), api.MEMMAPFILESIZE)
        self.client_api = api.API(mmap_item)
        logging.debug('Initializing...')
        for key in self.client_api.keys():
            value = self.client_api[key]

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.sensor_sink = kvaser.Kvaser()

    def run(self):
        # Setup sensor reading schedule.
        self.scheduler.enter(0, 1, self.read_sensors, ())

        logging.debug('Entering poll loop')
        self.sensor_sink.reset()
        try:
            self.scheduler.run()
        except KeyboardInterrupt:
            pass

    def read_sensors(self):
        # Reschedule
        self.scheduler.enter(0.1, 1, self.read_sensors, ())

        values = {}
        for key, sensor in Sensors.items():
            values[key] = self.client_api[sensor['name']]
            if values[key] is None:
                values[key] = 0
            logging.debug('Sending {}: {}'.format(key, values[key]))

        self.sensor_sink.sink(values)


def main():
    # Setup logging
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
    bridge = iRacingBridge()
    bridge.run()

if __name__ == '__main__':
    main()
