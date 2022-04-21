from flask import Flask, render_template
import logging
import csv
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/news', '/statistic'],
                  ['/developers', '/info'],
                  ['/social_media']]

TOKEN = '5193054775:AAHmmNiMl5903TX_C8Wk9Xp6fJ2REQVvdyE'

app = Flask(__name__)

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(bot, context):
    bot.message.reply_text(
        "Привет {}! От меня ты можешь узнать много о нашем футболе. С чего хочешь начать?".
            format(bot.message.chat.first_name),
        reply_markup=markup
    )


def close_keyboard(bot, context):
    bot.message.reply_text(
        "Клвиатура изменена",
        reply_markup=ReplyKeyboardRemove()
    )


def statistic(bot, context):
    close_keyboard(bot, context)
    keyboard_stat = [['Турнирная талица', 'Бомбардиры'],
                     ['"Сухие" матчи', 'Голевые передачи'],
                     ["Желыте карточки", "Красные карточки"],
                     ["Назад"]]
    markup_stat = ReplyKeyboardMarkup(keyboard_stat, one_time_keyboard=True)
    bot.message.reply_text(
        "Я могу предоставить тебе доступ к такой статистике:", reply_markup=markup_stat)


def news(bot, context):
    keyboard = [
        [
            InlineKeyboardButton('Матч Премьер', callback_data='Матч Премьер'),
            InlineKeyboardButton("tg2", callback_data='2'),
        ],
        [InlineKeyboardButton("tg 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.message.reply_text(
        'Итак тут ты можешь узнать последние новости о нашем футболе. Выбери Телеграм канал, '
        'а я 10 последних новостей)', reply_markup=reply_markup)


def developers(bot, context):
    bot.message.reply_text("will be soon")


def social_media(bot, context):
    bot.message.reply_text(
        "will be soon")


def table_rpl(bot, context):
    context.bot.send_photo(chat_id=bot.message.chat.id, photo=open('images/table.jpg', 'rb'))


def zeros(bot, context):
    zeros = open('zeros.txt', 'r', encoding='utf-8').read()
    bot.message.reply_text(f'{zeros}')


def assists(bot, context):
    asists = open('asists.txt', 'r', encoding='utf-8').read()
    bot.message.reply_text(f'{asists}')


def yk(bot, context):
    yk = open('yk.txt', 'r', encoding='utf-8').read()
    bot.message.reply_text(f'{yk}')


def kk(bot, context):
    kk = open('kk.txt', 'r', encoding='utf-8').read()
    bot.message.reply_text(f'{kk}')


def goals(bot, context):
    goals = open('goals.txt', 'r', encoding='utf-8').read()
    bot.message.reply_text(f'{goals}')


def info(bot, context):
    bot.message.reply_text(
        "will be soon")


def main():
    my_bot = Updater(TOKEN)
    dp = my_bot.dispatcher
    text_handler = MessageHandler(Filters.text & ~Filters.command, start)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(MessageHandler(Filters.regex("Турнирная талица"), table_rpl))
    dp.add_handler(MessageHandler(Filters.regex("Бомбардиры"), goals))
    dp.add_handler(MessageHandler(Filters.regex("Голевые передачи"), assists))
    dp.add_handler(MessageHandler(Filters.regex('"Сухие" матчи'), zeros))
    dp.add_handler(MessageHandler(Filters.regex('Желыте карточки'), yk))
    dp.add_handler(MessageHandler(Filters.regex('Красные карточки'), kk))
    dp.add_handler(MessageHandler(Filters.regex("Назад"), start))
    dp.add_handler(CommandHandler("developers", developers))
    dp.add_handler(CommandHandler("statistic", statistic))
    dp.add_handler(CommandHandler("social_media", social_media))
    dp.add_handler(text_handler)
    my_bot.start_polling()

    my_bot.idle()


if __name__ == '__main__':
    main()
