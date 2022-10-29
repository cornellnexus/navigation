import io
import os
"""a function from : https://raspberrypi.stackexchange.com/questions/5100/detect-that-a-python-program-is-running-on-the-pi/74541#74541
return True if the current device is a raspberry_pi, False otherwise"""
def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False


print(is_raspberrypi())