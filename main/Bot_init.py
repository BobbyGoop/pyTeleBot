from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import sys

sys.path.append('../')

from pyTeleBot.resources import config as cfg
from pyTeleBot.resources.json_search import *


begin, word, match = 0, 1, 2
def start_message(update, context: CallbackContext):
    update.message.reply_text('Привет, человек! Я - телеграмный бот, который может оказаться весьма полезным'
                              ' при изучении английского языка. Отправь команду /continue чтобы продолжить общаться'
                              ' или введи /stop если я тебе больше не нужен ')
    return begin


def start_working(update, context: CallbackContext):
    update.message.reply_text('Хорошо, тогда начнем. Введи любое слово (на английском) и я '
                              'покашу тебе все возможные определения этого слова, тоже разумеется '
                              'на английском языке')
    return word


def continue_working(update, context: CallbackContext):
    update.message.reply_text('Однако, здравствуйте. Я снова готов работать для вас')
    return word


def echo_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Чтобы продолжить пользоваться ботом, нажми или введи /continue')


def word_handler(update, context: CallbackContext):
    global text
    text = update.message.text
    answer = retrive_definition(text)
    if text == "/stop":
        update.message.reply_text('Бот отдыхает. Чтобы его разбудить, нажми или введи /continue')
        return ConversationHandler.END
    if type(answer) == list:
        for item in answer:
            update.message.reply_text('- ' + item)
        return word
    elif len(get_close_matches(answer, data.keys())) != 0:
        update.message.reply_text(
            "Возможно вы имели ввиду слово %s? (Да или Нет):" % get_close_matches(text, data.keys())[0])
        return match
    else:
        update.message.reply_text('Такого слова не существует либо допущено слишком много ошибок ')
        return word


def get_matches(update, context: CallbackContext):
    action = update.message.text
    if action.lower() == "да":
        for item in data[get_close_matches(text, data.keys())[0]]:
            update.message.reply_text('- ' + item)
        return word
    elif action.lower() == "нет":
        update.message.reply_text('Такого слова не существует')
        return word
    else:
        update.message.reply_text('Введите корректный ответ')


def main():
    bot = Bot(token=cfg.TG_TOKEN,
              base_url=cfg.TG_API_URL)

    updater = Updater(bot=bot,
                      use_context=True)
    con_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_message),
                      CommandHandler('continue', continue_working)],
        states={
            begin: [
                CommandHandler('continue', start_working)
            ],
            word: [
                MessageHandler(Filters.text, word_handler, pass_user_data=True),
            ],
            match: [
                MessageHandler(Filters.text, get_matches, pass_user_data=True),
            ]
        },
        fallbacks=[])

    updater.dispatcher.add_handler(con_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo_handler))
    updater.start_polling()
    print(" Бот работает")
    updater.idle()


if __name__ == '__main__':
    main()
