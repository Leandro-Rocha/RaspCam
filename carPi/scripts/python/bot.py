#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from threading import Thread

import dash
import gpio
import gpsdaemon
import video
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

should_stop = False

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def cade(bot, update):
    logger.warning(get_user_name(update) + " - cade")
    gpio.blink(gpio.YELLOW, 2)
    entry = gpsdaemon.get_last_entry()
    update.message.reply_location(entry["lat"], entry["lon"])


def photo(bot, update):
    logger.warning(get_user_name(update) + " - photo")
    gpio.blink(gpio.WHITE, 2)
    video.capture(dash.CAPTURE_FILE)
    update.message.reply_photo(photo=open(dash.CAPTURE_FILE, 'rb'))


def gif(bot, update):
    logger.warning(get_user_name(update) + " - gif")
    update.message.reply_text("Gravando gif!")
    gpio.blink(gpio.BLUE, 5)
    video.record_gif(update, 5)


def status(bot, update):
    logger.warning(get_user_name(update) + " - status")
    update.message.reply_text(dash.status())


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def get_user_name(update):
    return str(update.message.from_user["first_name"] + " " + update.message.from_user["last_name"])


def main():
    logger.info("Starting bot main method")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("274260732:AAGBhKLQri04sWPuCz2MxkqWWGUF9TyqjWo")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("cade", cade))
    dp.add_handler(CommandHandler("photo", photo))
    dp.add_handler(CommandHandler("gif", gif))
    dp.add_handler(CommandHandler("status", status))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    while True:
        time.sleep(1)
        if should_stop:
            break

    logger.info("Stopping bot main method")
    updater.stop()


def start_bot():
    thread_bot = Thread(target=main, name="botThread")
    thread_bot.start()


def stop():
    global should_stop
    should_stop = True


if __name__ == '__main__':
    main()
