import logging
import sqlite3
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['Новости', 'Статистика'],
                  ['Разработчикам', 'Информация']]

TOKEN = '5193054775:AAHmmNiMl5903TX_C8Wk9Xp6fJ2REQVvdyE'

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(bot, context):
    bot.message.reply_text(
        "Привет {}! От меня ты можешь узнать много о нашем футболе. С чего хочешь начать?".
            format(bot.message.chat.first_name),
        reply_markup=markup
    )


def close_keyboard(bot, context):
    bot.message.reply_text(
        "Клавиатура изменена",
        reply_markup=ReplyKeyboardRemove()
    )


def statistic(bot, context):
    close_keyboard(bot, context)
    keyboard_stat = [['Турнирная таблица', 'Бомбардиры'],
                     ['"Сухие" матчи', 'Голевые передачи'],
                     ["Желыте карточки", "Красные карточки"],
                     ["Назад"]]
    markup_stat = ReplyKeyboardMarkup(keyboard_stat, one_time_keyboard=True)
    bot.message.reply_text(
        "Я могу предоставить тебе доступ к следующей статистике... \n "
        "Статистика обновляется после каждого тура", reply_markup=markup_stat)


def news(bot, context):
    close_keyboard(bot, context)
    keyboard_news = [['tg: Матч Премьер'], ['tg: Сборная России по футболу'],
                     ['сайт: Чемпионат'], ['сайт: Спорт-Экспресс'],
                     ["Назад"]]
    markup_news = ReplyKeyboardMarkup(keyboard_news, one_time_keyboard=True)

    bot.message.reply_text(
        'Итак тут ты можешь узнать последние новости о нашем футболе. Выбери СМИ,'
        ' а я дам тебе на них ссылку канал,)', reply_markup=markup_news)
    return 1


def get_last_news(bot, context):
    smi = ['tg: Матч Премьер', 'tg: Сборная России по футболу', 'сайт: Чемпионат',
           'сайт: Спорт-Экспресс', 'Назад']
    if bot.message.text in smi:
        smi_link = open('news.txt', 'r', encoding='utf-8').readlines()
        bot.message.reply_text(f"Ссылка: {smi_link[smi.index(bot.message.text)]}")
        return ConversationHandler.END
    else:
        return 1


def developers(bot, context):
    bot.message.reply_text("Хочешь оставить для нас послание/пожелание/предложение/похвалу? \n"
                           "Сеня - https://t.me/molnia_macvin \n"
                           "Или напиши: <Обратная связь> ")


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
        "В этом блоке вы можете узнать конкретнее о каждом "
        "клубе выступающем в Тинькофф Российской Премьер Лиге \n "
        "Выберите клуб:")
    clubs = open('all_clubs.txt', 'r', encoding='utf-8').read()
    bot.message.reply_text(f'{clubs}')
    return 1


def choose_club(bot, context):
    clubs = open('all_clubs.txt', 'r', encoding='utf-8').readlines()
    for i in range(len(clubs)):
        clubs[i] = clubs[i].rstrip()
    if bot.message.text in clubs:
        context.user_data['club'] = bot.message.text
        close_keyboard(bot, context)
        keyboard_info = [["История", "Стадион"],
                         ['Трофеи', 'Состав'],
                         ["Обратно"]]
        markup_info = ReplyKeyboardMarkup(keyboard_info, one_time_keyboard=True)
        bot.message.reply_text('Команда "{}" выбрана'.format(bot.message.text),
                               reply_markup=markup_info)
        return 2
    else:
        bot.message.reply_text("Неверно введено название команды. Попробуйте еще раз.")
        return 1


def info_about_current_club(bot, context):
    ru = ["История", "Стадион", 'Состав', 'Трофеи']
    if bot.message.text in ru:
        con = sqlite3.connect('clubs.db')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM all_clubs WHERE team == ?""",
                             [context.user_data['club']]).fetchone()
        otevt = list(result)[ru.index(bot.message.text) + 1].split('???')
        if len(otevt) == 2:
            foto = 'images/' + otevt[1]
            context.bot.send_photo(chat_id=bot.message.chat.id, photo=open(foto, 'rb'))
        otevt = otevt[0]
        bot.message.reply_text(f'{otevt}')
        return 2
    else:
        start(bot, context)
    return ConversationHandler.END


def vopros1(bot, context):
    bot.message.reply_text(f'Пишите вопрос')
    return 1


def accept_vopros(bot, context):
    id = bot.message.chat.id
    name = bot.message.chat.first_name
    otvet = bot.message.text
    con = sqlite3.connect('vopros.db')
    cur = con.cursor()
    result = cur.execute("""INSERT INTO vopros(id, name, vopros) VALUES(?, ?, ?)""",
                         [id, name, otvet])
    con.commit()
    con.close()
    bot.message.reply_text(f"Вопрос принят")
    return ConversationHandler.END


def main():
    my_bot = Updater(TOKEN)
    dp = my_bot.dispatcher
    text_handler = MessageHandler(Filters.text & ~Filters.command, start)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("Статистика"), statistic))
    dp.add_handler(MessageHandler(Filters.regex("Турнирная таблица"), table_rpl))
    dp.add_handler(MessageHandler(Filters.regex("Бомбардиры"), goals))
    dp.add_handler(MessageHandler(Filters.regex("Голевые передачи"), assists))
    dp.add_handler(MessageHandler(Filters.regex('"Сухие" матчи'), zeros))
    dp.add_handler(MessageHandler(Filters.regex('Желыте карточки'), yk))
    dp.add_handler(MessageHandler(Filters.regex('Красные карточки'), kk))
    dp.add_handler(MessageHandler(Filters.regex("Назад"), start))
    dp.add_handler(MessageHandler(Filters.regex("Разработчикам"), developers))
    dp.add_handler(CommandHandler("statistic", statistic))
    vopros = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Обратная связь"), vopros1)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, accept_vopros)]
        },
        fallbacks=[CommandHandler('ok', start)]
    )
    info_about_clubs = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Информация"), info, pass_user_data=True)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, choose_club)],
            2: [MessageHandler(Filters.text & ~Filters.command, info_about_current_club)]
        },
        fallbacks=[CommandHandler('ok', start)]
    )
    novosty = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Новости"), news, pass_user_data=True)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, get_last_news)],
        },
        fallbacks=[CommandHandler('ok', start)]
    )
    dp.add_handler(novosty)
    dp.add_handler(info_about_clubs)
    dp.add_handler(vopros)
    dp.add_handler(text_handler)
    my_bot.start_polling()

    my_bot.idle()


if __name__ == '__main__':
    main()
