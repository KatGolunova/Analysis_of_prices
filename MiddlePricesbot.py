import telebot
import config
from telebot import types
from classes import *

bot = telebot.TeleBot(config.TOKEN)

date = Date()
town = Town()
product = Product()
data_out = DataOut()


@bot.message_handler(commands=['start'])
def welkom_to_my_bot(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ <b>{1.first_name}</b> - "
                     "бот, который позволит Вам лучше разбираться в ценах на товары.\n"
                     "Вы сможете получить информацию о средних ценах на товары по областям или по стране "
                     "за 2021-2022 гг (диапазон лет будет расширяться!).\n"
                     "Последовательно вызывайте команды меню для ввода данных:\n"
                     "/inputdate - для ввода даты\n"
                     "/inputregion - для ввода области (чтобы узнать средние цены по стране - пишите Беларусь)\n"
                     "/start - в экран приветствия".format(message.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(commands=['inputdate'])
def add_date(message):
    bot.send_message(message.chat.id,
                     "Введите интересующий Вас месяц и год в формате ММГГГГ "
                     "(например, '072022')")
    bot.register_next_step_handler(message, check_date)


def check_date(message):
    if date.check_date(message.text):
        if date.url_pars():
            bot.send_message(message.chat.id, "Отлично! Теперь введите /inputregion")
        else:
            bot.send_message(message.chat.id, "На заданную дату нет информации")
    else:
        bot.send_message(message.chat.id,
                         "Повторите ввод даты! Возможно, случилась опечатка")


@bot.message_handler(commands=['inputregion'])
def add_region(message):
    bot.send_message(message.chat.id,
                     "Введите область c заглавной буквы (или г.Минск),"
                     " или список областей через пробел:")
    bot.register_next_step_handler(message, check_region)


def check_region(message):
    if town.check_town(message.text):
        bot.send_message(message.chat.id, 'Отправьте мне любую букву, чтобы начать ввод товара')
        bot.register_next_step_handler(message, add_product)
    else:
        bot.send_message(message.chat.id,
                         "Повторите ввод области! Возможно, случилась опечатка")


def add_product(message):
    Product.list_of_products(product, date.url, town.ob_list)  # доступ к методу через класс
    bot.send_message(message.chat.id, "Введите наименование товара строчными буквами (и его описание через пробел):")
    bot.register_next_step_handler(message, check_product)


def check_product(message):
    if not product.parser(message.text):
        bot.send_message(message.chat.id,
                         f'Повторите ввод товара! Возможно, случилась опечатка или такого товара нет. Нажмите "п"')
        bot.register_next_step_handler(message, add_product)
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Список найденных товаров", callback_data='list_prod')
        item2 = types.InlineKeyboardButton("Итоговая таблица с ценами", callback_data='all_inf')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Как мне отобразить данные (сделайте выбор)?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'all_inf':
            out = f'Средние цены за {date.d} месяц {date.g} года ' \
                  f'(в рублях за килограмм, литр, десяток, изделие)\n' \
                  f'{data_out.table_of_dat(product.price_list, product.choice_list, town.ob_list)}'
            bot.send_message(call.message.chat.id, out)  # вывод итоговой таблицы
        elif call.data == 'list_prod':
            choice_out = '\n'.join(product.choice_list)
            bot.send_message(call.message.chat.id, f'{choice_out}')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Выборка окончена')


bot.polling(none_stop=True)
