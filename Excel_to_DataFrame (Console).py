import pandas as pd
from tabulate import tabulate
from parser import parser # импортируем функцию поиска товара

# функция проверки правильности ввода города (области):
def check_date(d, l):  # список, который сверяем - d, и с которым сверяем - l
    for i in d:
        if i not in l:
            print('Опечатка!')
            return False
        else:
            return True

d_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
g_list = ['2021', '2022']
while True:
    dat = input('Введите дату в формате ммгггг: ')
    if dat[0:2] in d_list and dat[2:] in g_list:
        d = dat[0:2]
        g = dat[2:]
        break
    else:
        print ('Повторите ввод даты! Возможно, случилась опечатка')

while True:
    ob = input('Введите область c заглавной буквы (или г.Минск), или список областей через пробел: ')
    list_ob = ['Беларусь', 'Брестская', 'Витебская', 'Гомельская', 'Гродненская', 'г.Минск', 'Минская',
               'Могилевская']
    ob_list = []
    if ' ' in ob:
        ob_list = ob.split()
    else:
        ob_list.append(ob) # приводим строки к списку

    if check_date(ob_list, list_ob):
        break

# обработка г.Минска (в исходнике он с пробелом):
for i in ob_list:
    if 'г.Минск' in ob_list:
        ob_list[ob_list.index('г.Минск')] = 'г. Минск'

url = 'https://www.belstat.gov.by/upload-belstat/upload-belstat-excel/Oficial_statistika/Average_prices-'+d+'-'+g+'.xls'
ob_list_col = ob_list.copy()
ob_list_col.insert(0, 'Unnamed: 0') # к списку областей добавляем в начало колонку товаров
excel_data_df = pd.read_excel(url, usecols = ob_list_col, header = 6) # читаем Excel файл, начиная с 7-й строки, в объект DataFrame
ex_lower = excel_data_df['Unnamed: 0'].apply(lambda x: x.lower()) # все буквы в выборке станут строчными
list_of_products = ex_lower.tolist() # вывод данных столбца товаров с преобразованием в список строк
#print(list_of_products)

price_list = []
while True:
    product = input('Введите наименование товара (и его описание через пробел): ').split()
    res_list = parser(product, list_of_products)
    index_list = res_list[0]
    choice_list = res_list[1]
    if choice_list == []:
        print('Опечатка или такого товара нет!')
        continue
    break

for i in index_list:
    price_list.append(excel_data_df.iloc[i]) # получаем значения строк по индексу
#print(price_list)

# формируем таблицу-результат:
data_out = pd.DataFrame([price_list[i] for i in range(len(choice_list))], index=choice_list, columns= ob_list)
data_table = tabulate(data_out, headers=ob_list, tablefmt='psql')
print(f'Средние цены за {d} месяц {g} года (в рублях за килограмм, литр, десяток, изделие)\n', data_table)

# вывод на html-страницу:
# html = data_out.to_html()
# f = open("index.html", "w")
# f.write(f'Средние цены за {d} месяц {g} года (в рублях за килограмм, литр, десяток, изделие)\n'+html)
# f.close()








