'''1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных
из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

    Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
    данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
     «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
     соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
     os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и
     поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
     «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
     каждого файла);
    Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
    данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
    Проверить работу программы через вызов функции write_to_csv().

'''
import chardet
from chardet import detect
import re
import csv


# LENOVO, Microsoft Windows 7, 00971-OEM-1982661-00231, x64-based PC



def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    data_all = []

    for i in range(1, 4):
        with open(f'info_{i}.txt', 'rb') as f:
            data_bytes = f.read()
            result = chardet.detect(data_bytes)
            data = data_bytes.decode(result['encoding'])

        os_prod = re.compile(r'Изготовитель системы: \s*\S*')
        os_prod_list.append(os_prod.findall(data)[0].split()[2])

        os_code = re.compile(r'Код продукта: \s*\S*')
        os_code_list.append(os_code.findall(data)[0].split()[2])

        os_name = re.compile(r'Windows\s\S*')
        os_name_list.append(os_name.findall(data)[0])

        os_type = re.compile(r'Тип системы:\s*\S*')
        os_type_list.append(os_type.findall(data)[0].split()[2])

    head = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    data_all.append(head)

    matrixs = [os_prod_list, os_name_list, os_code_list, os_type_list]
    # print(matrixs)
    for i in range(len(matrixs[0])):
        line = [row[i] for row in matrixs]
        data_all.append(line)
    # print(data_all)
    return data_all


def write_to_csv(file):
    data_all = get_data()
    with open(file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in data_all:
            writer.writerow(row)


write_to_csv('data.csv')


