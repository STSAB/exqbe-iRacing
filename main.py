import exhub
import config
from api import api

import logging
import platform
import os
import mmap
import serial
import sys

def main():
    # Setup logging
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

    local_hub = exhub.Exhub('/dev/cu.usbserial-A603AVX6')
    configuration = config.Config('config.bin')

    # iRacing memory mapped files only works on Windows systems. In case of a non-Windows system we can simulate
    # the behavior by mapping against a memory dump instead.
    mmap_item = None
    if platform.system() != 'Windows':
        mmap_file = os.path.join('api', 'tests', 'memorydump.dmp')
        mmap_f = open(mmap_file, 'r+b')
        mmap_item = mmap.mmap(mmap_f.fileno(), api.MEMMAPFILESIZE)
    client_api = api.API(mmap_item)

    try:
        while True:
            try:
                logging.debug('Wait for request')
                # Wait for a request from the Exhub
                address = local_hub.blocking_read()
                # Fetch iRacing value
                iracing_key = configuration.get_definition(address).sensor_name
                iracing_value = client_api[iracing_key]
                # Apply reverse calculation
                ad_reading = int(configuration.apply_formulas(address, iracing_value))
                # Reply to Exhub
                logging.debug('Sending sensor {} value {}'.format(iracing_key, ad_reading))
                local_hub.send(address, ad_reading)
            except serial.SerialException, e:
                logging.error('Unrecoverable serial exception, {}'.format(e))
                raise
            except config.ConfigError, e:
                logging.error('Configuration error: {}'.format(e.message))
            except KeyError, e:
                logging.error('Unknown sensor name: {}'.format(e.message))
            except Exception, e:
                logging.error('Unknown error, {}'.format(sys.exc_info()[0]))

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
