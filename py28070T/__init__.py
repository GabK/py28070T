import logging
import RPi.GPIO as GPIO
import time

logging.getLogger().setLevel(logging.DEBUG)

CODE = '{0}11011101111{1}111111010111'

LONG_HIGH = 0.0014583
LONG_LOW = 0.00114583
SHORT_HIGH = 0.0005859375
SHORT_LOW = 0.000260416
WAIT = 0.0139114583
RETRIES = 10

STATES = {
    True: '01',
    False: '10'
}

SOCKETS = ['01', '10', '00']

class Socket(object):
    tx_pin = None
    socket = None
    _state = None

    def __init__(self, tx_pin = None, socket = None, state = False):
        self.tx_pin = tx_pin
        self.socket = socket

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        if self.tx_pin is not None:
            GPIO.setup(self.tx_pin, GPIO.OUT)

        if state is not None:
            self.state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self.tx_pin is None:
            logging.warning("TX pin is not set.")
        else:
            self._state = value
            code = CODE.format(STATES[value], SOCKETS[self.socket])

            logging.debug("Sending code [ {0} ]", code)

            for attempt in range(RETRIES):
                for b in code:
                    if b == '1':
                        GPIO.output(self.tx_pin, 1)
                        time.sleep(SHORT_HIGH)
                        GPIO.output(self.tx_pin, 0)
                        time.sleep(LONG_LOW)
                    elif b == '0':
                        GPIO.output(self.tx_pin, 1)
                        time.sleep(LONG_HIGH)
                        GPIO.output(self.tx_pin, 0)
                        time.sleep(SHORT_LOW)
                    else:
                        continue

                time.sleep(WAIT)
