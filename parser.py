import string

# функция поиска товара по ключевым словам, где первое слово - основное
def parser(products, list_of_products): # на входе 2 списка
    ind_list = []
    choicelist = []
    for pr in list_of_products:
        if products[0] in pr: # первое введенное слово - основа поиска
            # ищем товар в списке товаров (парсим строку)
            pr_str = pr.translate(str.maketrans('', '', string.punctuation)) # удалим все знаки препинания
            pr_list = pr_str.split()
            if len(products) == 1 and (products[0] in pr_list): # введено только одно слово
                ind_list.append(list_of_products.index(pr))  # вытаскиваем индексы найденных строк
                choicelist.append(pr) # добавляем сами товары
            else:  # иначе проходим по остальному списку
                for tov in products[1:]: # добавляем к поиску остальные слова описания
                    if tov in pr_list:
                        ind_list.append(list_of_products.index(pr))
                        choicelist.append(pr)
    list_item = [ind_list, choicelist] # на выходе список из 2-х списков: индексов и товаров
    return list_item
