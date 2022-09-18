import requests
import pandas as pd
import string
from tabulate import tabulate


class Date:
    d_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    g_list = ['2021', '2022']

    def __init__(self):
        self.d = ''
        self.g = ''
        self.url = ''

    def check_date(self, dat):  # введите дату
        if dat[0:2] in self.d_list and dat[2:] in self.g_list:
            self.d = dat[0:2]
            self.g = dat[2:]
            return self.d, self.g  # вернет кортеж значений при печати
        else:
            return False

    def url_pars(self):
        urls = ['https://www.belstat.gov.by/upload-belstat/upload-belstat-excel/'
                'Oficial_statistika/Average_prices-' + self.d + '-' + self.g + '.xls',
                'https://www.belstat.gov.by/upload-belstat/upload-belstat-excel/'
                'Oficial_statistika/' + self.g + '/Average_prices-' + self.d + '-' + self.g + '.xls']
        for i in urls:
            r = requests.get(i)
            if r.status_code == 200:
                self.url = i
        if self.url != '':
            return self.url
        else:
            return False


class Town:
    list_ob = ['Беларусь', 'Брестская', 'Витебская', 'Гомельская', 'Гродненская', 'г.Минск',
               'Минская',
               'Могилевская']

    def __init__(self):
        self.ob_list = []

    def check_town(self, ob):  # ввод области
        rez = True
        if ' ' in ob:
            self.ob_list = ob.split()
        else:
            self.ob_list.append(ob)  # приводим строку к списку
        if 'г.Минск' in self.ob_list:  # обрабатываем город Минск (пробел)
            self.ob_list[self.ob_list.index('г.Минск')] = 'г. Минск'
        for i in self.ob_list:
            if i not in self.list_ob:
                rez = False
        if rez:
            return self.ob_list
        else:
            return False


class Product:
    def __init__(self):
        self.url = ''
        self.ob_list = []
        self.price_list = []
        self.list_of_products = []
        self.excel_data_df = pd.DataFrame()
        self.choice_list = []

    def list_of_products(self, url, ob_list):  # метод выбирает данные по области и по дате
        ob_list_col = ob_list.copy()
        ob_list_col.insert(0, 'Unnamed: 0')  # к списку областей добавляем в начало колонку товаров
        # читаем Excel файл, начиная с 7-й строки, в объект DataFramе
        # sheet_name=0 обязательно!
        self.excel_data_df = pd.read_excel(url, sheet_name=0, usecols=ob_list_col, header=6)
        ex_lower = self.excel_data_df['Unnamed: 0'].apply(lambda x: x.lower())  # все буквы в выборке станут строчными
        self.list_of_products = ex_lower.tolist()  # вывод данных столбца товаров с преобразованием в список строк
        self.url, self.ob_list = url, ob_list
        return self.list_of_products, self.excel_data_df

    def parser(self, product):  # введите товар и его описание через пробел
        product = product.split()
        ind_list = []
        for pr in self.list_of_products:
            # ищем подстроку:
            if product[0] in pr:  # первое введенное слово - основа поиска
                # ищем товар в списке товаров (парсим строку)
                pr_str = pr.replace('-', ' ')  # заменяем дефис на пробел
                pr_str = pr_str.translate(str.maketrans('', '', string.punctuation))  # удалим все знаки препинания
                pr_list = pr_str.split()
                if len(product) == 1 and (product[0] in pr_list):  # введено только одно слово
                    ind_list.append(self.list_of_products.index(pr))  # вытаскиваем индексы найденных строк
                    self.choice_list.append(pr)  # добавляем сами товары
                else:  # иначе проходим по остальному списку
                    for tov in product[1:]:  # добавляем к поиску остальные слова описания
                        if tov in pr_list:
                            ind_list.append(self.list_of_products.index(pr))
                            self.choice_list.append(pr)
        if len(self.choice_list) == 0:
            return False
        else:
            for i in ind_list:
                self.price_list.append(self.excel_data_df.iloc[i])
            return self.choice_list, self.price_list  # список товаров и список цен


class DataOut:
    def __init__(self):
        self.price_list = []
        self.choice_list = []
        self.ob_list = []

    def table_of_dat(self, price_list, choice_list, ob_list):
        data_out = pd.DataFrame([price_list[i] for i in range(len(choice_list))],
                                index=choice_list, columns=ob_list)
        data_table = tabulate(data_out, headers=ob_list, tablefmt='psql')
        self.price_list = price_list
        self.choice_list = choice_list
        self.ob_list = ob_list
        return data_table
