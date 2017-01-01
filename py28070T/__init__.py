import logging
import RPi.GPIO as GPIO
import time

CODE = '%s11011101111%s111111010111'

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

class Tx:
    tx_pin = None

    states = [None, None, None]

    def __init__(self, tx_pin = None, initial_state = [False, False, False]):
        self.tx_pin = tx_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        if self.tx_pin is not None:
            GPIO.setup(self.tx_pin, GPIO.OUT)

        if type(initial_state) is list:
            for socket, state in enumerate(initial_state):
                self.set(socket, state)

    def set(self, socket, state):
        if self.tx_pin is None:
            logging.warning("TX pin is not set.")
        else:
            code = CODE % (STATES[state], SOCKETS[socket])

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

                GPIO.output(self.tx_pin, 0)
                time.sleep(WAIT)
