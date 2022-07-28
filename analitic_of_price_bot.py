import telebot
import config
from telebot import types
import pandas as pd
from parser import parser # импортируем функцию поиска товара

bot = telebot.TeleBot(config.TOKEN)

d_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
g_list = ['2021', '2022']
list_ob = ['Беларусь', 'Брестская', 'Витебская', 'Гомельская', 'Гродненская', 'г.Минск', 'Минская',
               'Могилевская']

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
     "/start - в экран приветствия"
    .format(message.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(commands=['inputdate'])
def add_date(message):
    bot.send_message(message.chat.id,
                         "Введите интересующий Вас месяц и год в формате ММГГГГ "
                         "(например, '062022')")
    bot.register_next_step_handler(message, check_date)

def check_date(message):
    global dat
    global d
    global g
    dat = message.text
    if dat[0:2] in d_list and dat[2:] in g_list:
        d = dat[0:2]
        g = dat[2:]
        bot.send_message(message.chat.id, "Отлично! Теперь введите /inputregion")
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
        global ob_list
        global list_of_products
        global excel_data_df

        ob_list = []
        ob = message.text
        if ' ' in ob:
            ob_list = ob.split()
        else:
            ob_list.append(ob)  # приводим строки к списку
        for i in ob_list:
            if i not in list_ob:
                bot.send_message(message.chat.id,
                                 "Повторите ввод области! Возможно, случилась опечатка")

        #обработка г.Минска (в exel-исходнике он с пробелом):
        if 'г.Минск' in ob_list:
            ob_list[ob_list.index('г.Минск')] = 'г. Минск'

        # получаем в переменную Excel-файл с сайта Белстата
        url = 'https://www.belstat.gov.by/upload-belstat/upload-belstat-excel/Oficial_statistika/Average_prices-'+d+'-'+g+'.xls'
        ob_list_col = ob_list.copy()

        # к списку областей добавляем в начало колонку товаров (исходное название столбца DataFrame не меняем)
        ob_list_col.insert(0, 'Unnamed: 0')

        # читаем Excel файл, начиная с 7-й строки, в объект DataFrame
        excel_data_df = pd.read_excel(url, usecols = ob_list_col, header = 6)

        ex_lower = excel_data_df['Unnamed: 0'].apply(lambda x: x.lower()) # все буквы в выборке станут строчными
        list_of_products = ex_lower.tolist() # вывод данных столбца товаров с преобразованием в список строк

        bot.send_message(message.chat.id, 'Нажмите "п", чтобы начать ввод товара')
        bot.register_next_step_handler(message, add_product)

    def add_product(message):
        bot.send_message(message.chat.id, "Введите наименование товара (и его описание через пробел):")
        bot.register_next_step_handler(message, check_product)

    def check_product(message):
        global choice_list
        global index_list
        global price_list
        product = message.text.split()
        price_list = []
        res_list = parser(product, list_of_products) # вызываем функцию поиска товара
        index_list = res_list[0]
        choice_list = res_list[1]
        if choice_list == []:
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
                for i in index_list:
                    price_list.append(excel_data_df.iloc[i])  # получаем значения строк по индексу
                # формируем таблицу-результат:
                data_out = pd.DataFrame([price_list[i] for i in range(len(choice_list))],
                                        index=choice_list, columns=ob_list)
                # рисуем табличку на языке markdown:
                data_out_t = data_out.to_markdown()
                out = f'Средние цены за {d} месяц {g} года (в рублях за килограмм, литр, десяток, изделие)\n{data_out_t}'
                bot.send_message(message.chat.id, out)  # вывод итоговой таблицы
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Выборка окончена')

            elif call.data == 'list_prod':
                choice_out = '\n'.join(choice_list)
                bot.send_message(message.chat.id, f'{choice_out}')
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Выборка окончена')

bot.polling(none_stop = True)