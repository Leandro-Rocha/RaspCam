import os

STOP_FILE = "/home/pi/carPi/temp/STOP"


def isStop():
    try:
        f = open(STOP_FILE)
        return True
    except IOError:
        return False


def initialize():
    try:
        os.remove(STOP_FILE)
    except OSError:
        pass


def stop():
    open(STOP_FILE, "w")
