'''5. Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и преобразовывает результат из
байтовового типа данных в строковый без ошибок для любой кодировки операционной системы.'''


import platform
import subprocess
from chardet import detect

site_urls = ['yandex.ru', 'youtube.com']
code = '-n' if platform.system().lower() == 'windows' else '-c'


for url in site_urls:
    args = ['ping', code, '4', url]
    ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in ping.stdout:
        result = detect(line)
        print(result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))

