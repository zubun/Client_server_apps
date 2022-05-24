"""Программа-клиент"""
'''1. Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):

    клиент отправляет запрос серверу;сервер отвечает соответствующим кодом результата. 
    Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции. 
    Функции клиента: сформировать presence-сообщение; 
    отправить сообщение серверу; 
     получить ответ сервера; 
     разобрать сообщение сервера; 
     параметры командной строки скрипта client.py <addr> [<port>]:addr — ip-адрес сервера; port — tcp-порт на сервере, 
     по умолчанию 7777. 
     Функции сервера: принимает сообщение клиента; 
     формирует ответ клиенту; 
     отправляет ответ клиенту; 
     имеет параметры командной строки: -p <port> — TCP-порт для работы 
     (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).

'''

# from socket import socket, AF_INET, SOCK_STREAM
#
# CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
# CLIENT_SOCK.connect(('localhost', 8888))
# TIME_BYTES = CLIENT_SOCK.recv(1024)
# print(f"Текущее время: {TIME_BYTES.decode('utf-8')}")
# CLIENT_SOCK.close()
# --------------------------------------
import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message


def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    '''Загружаем параметы коммандной строки'''
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
