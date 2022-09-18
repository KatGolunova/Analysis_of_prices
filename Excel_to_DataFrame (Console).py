from classes import *

# создаем объект пользовательского класса Date для проверки даты
date = Date()
while True:
    if date.check_date(input('Введите интересующий Вас месяц и год в формате ММГГГГ: ')):
        if date.url_pars():
            break
        else:
            print('На заданную дату нет информации')
    else:
        print("Повторите ввод даты! Возможно, случилась опечатка")

# создаем объект пользовательского класса Town для проверки области
town = Town()
while True:
    if town.check_town(input('Введите область c заглавной буквы (или г.Минск), или список областей через пробел: ')):
        break
    else:
        print('Повторите ввод области! Возможно, случилась опечатка')

# создаем объект пользовательского класса Product для выборки нужных данных
product = Product()  # передаем url и список областей при инициализации
Product.list_of_products(product, date.url, town.ob_list)  # доступ к методу через класс
while True:
    if product.parser(input('Введите наименование товара (и его описание) через пробел: ')):
        break
    else:
        print('Опечатка или такого товара нет!')

# формируем таблицу-результат (создаем объект DataOut)
data_out = DataOut()
print(f'Средние цены за {date.d} месяц {date.g} года (в рублях за килограмм, '
      f'литр, десяток, изделие):\n', data_out.table_of_dat(product.price_list, product.choice_list, town.ob_list))
