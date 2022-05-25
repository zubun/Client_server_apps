'''4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить обратное
 преобразование (используя методы encode и decode).'''

list_1 = ['Разработка', 'Администрирование', 'protocol', 'standart']
for i in list_1:
    value = i.encode('utf-8')
    print(f'{value} - Байтовое представление.')
    devalue = value.decode('utf-8')
    print(f'{devalue} - строковое представление.')
