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

"""Программа-сервер"""


# import sys
# import json
# from socket import socket, AF_INET, SOCK_STREAM
# import time
# from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
#     RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
# from common.utils import get_message, send_message
#
# SERV_SOCK = socket(AF_INET, SOCK_STREAM)
# SERV_SOCK.bind(('', 8888))
# SERV_SOCK.listen(5)
#
#
# try:
#     while True:
#         CLIENT_SOCK, ADDR = SERV_SOCK.accept()
#         print(f'Получен запрос на соединение от клиента с адресом и портом: {ADDR}')
#         TIMESTR = time.ctime(time.time()) + "\n"
#         CLIENT_SOCK.send(TIMESTR.encode('utf-8'))
#         CLIENT_SOCK.close()
# finally:
#     SERV_SOCK.close()
# -----------------------------------------------
import socket
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
