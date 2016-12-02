import datetime as dt
import logging
import time
from os import remove
from subprocess import call
from threading import Thread

import dash
import gpio
import gpsdaemon
from picamera import PiCamera

VIDEO_FOLDER = "../../video/"
FILE_FORMAT = "%Y-%m-%d_%H.%M.%S"
RECORD_TIME = 300
RESOLUTION = "1920x1080"
# RESOLUTION = "800x600"
# RESOLUTION = "1280x720"

should_stop = False
camera = PiCamera(resolution=RESOLUTION)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start_record_loop():
    thread = Thread(target=record, name="videoThread")
    thread.start()


def capture(file_name):
    camera.capture(file_name, use_video_port=True)


def record_gif(update, duration):
    thread = Thread(target=bg_record_gif, args=(update, duration))
    thread.start()


def clean_up_gif():
    try:
        remove(dash.GIF_FILE)
        remove(dash.CONVERTED_GIF_FILE)
    except OSError:
        pass


def bg_record_gif(update, duration):
    clean_up_gif()

    camera.start_recording(dash.GIF_FILE, splitter_port=3)
    camera.wait_recording(duration)
    camera.stop_recording(splitter_port=3)

    cmd = "MP4Box -add " + dash.GIF_FILE + " " + dash.CONVERTED_GIF_FILE
    call([cmd], shell=True)
    update.message.reply_video(video=open(dash.CONVERTED_GIF_FILE, 'rb'))


def record():
    logger.info("Starting record loop")
    gpio.setup()
    gpio.turnOn(gpio.RED)

    while not should_stop:
        file_name = time.strftime(FILE_FORMAT) + ".h264"

        start = time.time()
        camera.start_recording(VIDEO_FOLDER + file_name, splitter_port=1)

        while True:
            if (time.time() - start > RECORD_TIME) or should_stop:
                break

            entry = gpsdaemon.get_last_entry()
            overlay = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # overlay += " lat: " + str(entry["lat"])
            # overlay += " lon: " + str(entry["lon"])
            overlay += " speed: " + str(entry["speed"]) + "km/h"

            camera.annotate_text = overlay
            camera.wait_recording(1)

        camera.stop_recording(splitter_port=1)

    gpio.turnOff(gpio.RED)
    logger.info("Stopping record loop")


def stop():
    global should_stop
    should_stop = True

# record()
