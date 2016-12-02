import time
from subprocess import check_output

import bot
import video

TEMP_FOLDER = "../../temp/"
CAPTURE_FILE = TEMP_FOLDER + "capture.jpg"
GIF_FILE = TEMP_FOLDER + "gif.h264"
CONVERTED_GIF_FILE = TEMP_FOLDER + "gif.mp4"
STATUS_FILE = TEMP_FOLDER + "status.txt"


def status():
    cmd = "uptime -p"
    return check_output(cmd, shell=True)


def main():
    bot.start_bot()
    video.start_record_loop()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    video.stop()
    bot.stop()


if __name__ == '__main__':
    main()
