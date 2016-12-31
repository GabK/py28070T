from collections import deque
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

class RxTx:
    _last_event_times = {}
    _q = deque([], 54)

    rx0_pin = None
    rx1_pin = None

    tx_pin = None

    states = [None, None, None]

    def __init__(self, rx0_pin = None, rx1_pin = None, tx_pin = None, initial_state = [True, False, False]):
        self.rx0_pin = rx0_pin
        self.rx1_pin = rx1_pin
        self.tx_pin = tx_pin

        GPIO.setmode(GPIO.BCM)

        if self.tx_pin is not None:
            GPIO.setup(self.tx_pin, GPIO.OUT)

        if self.rx1_pin is not None:
            GPIO.setup(self.rx1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self.rx1_pin, GPIO.RISING, callback=self._process_gpio_event)

        if self.rx0_pin is not None:
            GPIO.setup(self.rx0_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self.rx0_pin, GPIO.FALLING, callback=self._process_gpio_event)

        if type(initial_state) is list:
            for socket, state in enumerate(initial_state):
                self.set(socket, state)

    def _process_gpio_event(self, channel):
        self._last_event_times[channel] = time.time()

        if self._last_event_times[self.rx0_pin] is not None and self._last_event_times[self.rx1_pin] is not None:
            dt = abs(self._last_event_times[self.rx0_pin] - self._last_event_times[self.rx1_pin])

            if channel == self.rx0_pin and dt >= LONG_HIGH:
                # ---\
                pass
            elif channel == self.rx0_pin and dt >= SHORT_HIGH:
                # -\
                pass
            elif channel == self.rx1_pin and dt >= LONG_LOW:
                # ___/
                pass
            elif channel == self.rx1_pin and dt >= SHORT_LOW:
                # _/
                pass

        if channel == self.rx0_pin:
            print "FALLING: %s ------ %s" % (str(time.time()), GPIO.input(self.rx0_pin))
        else:
            print "RISING:  %s ------ %s" % (str(time.time()), GPIO.input(self.rx1_pin))

    def set(self, socket, state):
        if self.tx_pin is None:
            pass
            # warning
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

            #GPIO.cleanup()
