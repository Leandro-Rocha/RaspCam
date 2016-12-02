import RPi.GPIO as GPIO
import time
import os

YELLOW = 32
RED = 22
BLUE = 18
WHITE = 16
GREEN = 12


def turnOnFor(port, interval):
    if os.fork() == 0:
        GPIO.output(port, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(port, GPIO.LOW)
        os._exit(0)


def turnOn(port):
    GPIO.output(port, GPIO.HIGH)


def turnOff(port):
    GPIO.output(port, GPIO.LOW)


def blink(port, interval):
    if os.fork() == 0:
        start = time.time()
        i = 0
        while (True):
            if i % 2:
                GPIO.output(port, GPIO.HIGH)
            else:
                GPIO.output(port, GPIO.LOW)

            if time.time() - start > interval:
                break

            i = i + 1
            time.sleep(0.1)

        os._exit(0)


def main():
    setup()

    turnOnFor(GREEN, 2)
    blink(WHITE, 2)
    turnOff(BLUE)
    blink(RED, 4)
    turnOnFor(YELLOW, 3)


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(YELLOW, GPIO.OUT)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(BLUE, GPIO.OUT)
    GPIO.setup(WHITE, GPIO.OUT)
    GPIO.setup(GREEN, GPIO.OUT)


if __name__ == '__main__':
    main()

setup()
