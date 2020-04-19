#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from parser import Parser
from model import Model


TOKEN = '1127148016:AAFgz9RGZWx9m1sNdfhFmLffPTfcSd7IvkM'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

model = Model()

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет! Я очень умный бот и могу понимать является ли новость о коронавирусе фейком или нет.\nПросто скинь ссылку на новость')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Зачем ты просишь помощи?\nЕсли ты чувтсуешь себя плохо, то о симптомах коронавируса COVID-19 можешь ознакомиться здесь\nhttps://covid19.rosminzdrav.ru/')


def check_fake_news(update, context):
    url = update.message.text
    p = Parser()
    logger.info(url)
    logger.info(type(url))
    data = p.read_news(url)
    predict = model.predict(data)
    update.message.reply_text('title = {}\ntext = {}'.format(predict[0], predict[1]))


def error(update, context):
    """Log Errors caused by Updates."""
    update.message.reply_text('Incorrect link')
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, check_fake_news))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
