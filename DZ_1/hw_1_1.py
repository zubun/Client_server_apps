'''1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и
также проверить тип и содержимое переменных.
'''


def print_type(lists):
    for i in lists:
        print(f'{i} тип - {type(i)}')
    return


list_1 = ['Разработка', 'Сокет', 'Декоратор']
list_2 = ['\u0420\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430', '\u0421\u043e\u043a\u0435\u0442', '\u0414\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
print_type(list_1)
print('-----------------------------------------------------')
print_type(list_2)