import time
import RPi.GPIO as GPIO

class Transmitter:
    _CODE = '%s11011101111%s111111010111'

    _LONG_HIGH = 0.0014583
    _LONG_LOW = 0.00114583
    _SHORT_HIGH = 0.0005859375
    _SHORT_LOW = 0.000260416
    _WAIT = 0.0139114583
    _RETRIES = 10

    _STATES = {
        True : '01',
        False : '10'
    }

    _SOCKETS = ['01', '10', '00']


    data_pin = None
    states = [None, None, None]

    def __init__(self, data_pin, initial_state=[False, False, False]):
        self.data_pin = data_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.data_pin, GPIO.OUT)

        if type(initial_state) is list:
            for socket, state in enumerate(initial_state):
                self.set(socket, state)

    def set(self, socket, state):
        code = self._CODE % (self._SOCKETS[socket], self._STATES[state])

        for attempt in range(self._RETRIES):
            for b in code:
                if b == '1':
                    GPIO.output(self.data_pin, 1)
                    time.sleep(self._SHORT_HIGH)
                    GPIO.output(self.data_pin, 0)
                    time.sleep(self._LONG_LOW)
                elif b == '0':
                    GPIO.output(self.data_pin, 1)
                    time.sleep(self._LONG_HIGH)
                    GPIO.output(self.data_pin, 0)
                    time.sleep(self._SHORT_LOW)
                else:
                    continue

            GPIO.output(self.data_pin, 0)
            time.sleep(self._WAIT)

        GPIO.cleanup()
