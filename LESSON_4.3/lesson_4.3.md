# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1

Мы выгрузили JSON, который получили через API запрос к нашему сервису:

    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }

Нужно найти и исправить все ошибки, которые допускает наш сервис

Ответ:
   1) Проверить корректность первого IP-адреса в источнике данных.
      Для IP м.4 должна быть формат вида xxx.xxx.xxx.xxx, если это не DNS имя.
   2) Вывести данный IP адрес в кавычках.
   3) Установить запятую между блоками {...},{...}  .
      
    {
       "info": "Sample JSON output from our service\t",
       "elements" : [
           {
               "name" : "first",
               "type" : "server",
               "ip" : "xxx.xxx.xxx.xxx"
           },
           {
               "name" : "second",
               "type" : "proxy",
               "ip" : "71.78.22.43"
           }
       ]
    }


--------------------------------------------------------------------------------------------------


## Обязательная задача 2

В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. 
К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, 
описывающих наши сервисы. 
Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. 
Формат записи YAML по одному сервису: - имя сервиса: его IP. 
Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

Ответ:

#!/usr/bin/env python3
# Скрипт проверяет изменение IP адресов переданный на вход
import socket as s
import time as t
from datetime import datetime
import json
import yaml

def inc(n):                     #  Определяем функцию инкремента.
    n = n + 1
    return n

wait_sec = 4                    # Задаем интервал проверок в секундах.
n = 1                           # Устанавливаем счетчик итераций проверок.

# Создаем объект словаря с серверами и их исходными IP адресами:

webservers = {'drive.google.com': '2.2.2.2', 'mail.google.com': '1.1.1.1', 'google.com': '8.8.8.8'}
print("Наши сервера:", webservers)

def fill_dictionary(x):               # Функция заполнения объекта словаря актуальными IP адресами
    for node in x:
        ip = socket.gethostbyname(node)
        x[node] = ip
    return x

def fill_json(y):                     # Функция формирования словаря в формате json в файле  webservers.json
    with open('webservers.json', 'w') as jtmp:
        jtmp.write(str(json.dumps(y)))        # Сериализация объекта Python в строку формата JASON
    return



def fill_yaml(z):                      # Функция формирования словаря в формате yaml в файле  webservers.yaml
    with open('webservers.yaml', 'w') as ytmp:
        ytmp.write(yaml.dump(z))              # Сериализация объекта Python в строку формата YAML
    return

fill_json(fill_dictionary(webservers))    # Заполняем YAML и JSON файлы, чтобы в них был актуальный список адресов
fill_yaml(fill_dictionary(webservers))

while True:

        tmp = fill_dictionary(webservers)   # Создаем временную копию словаря.
        for host in webservers:
            ip = s.gethostbyname(host)  # Обращаемся в интернет и получаем очередной IP по имени хоста.
            if ip != tmp[host]:  # Если значение IP не равно предыдущему - выводим строку ошибки.

                print( str( datetime.now().strftime("%d-%m-%Y %H:%M")) + ' [ERROR] ' + str(host)
                       + ' IP mistmatch: ' + tmp[host] + ' ' + ip)
                tmp[host] = ip  # Записываем новое значение IP для данного сервера в словарь-буфер для следующей проверки.
                fill_json(tmp)  # Дублируем изменения в файл webservers.json
                fill_yaml(tmp)  # Дублируем изменения в файл webservers.yaml
                n = inc(n)  # Увеличиваем значение n на 1 и ограничиваем кол-во итераций опроса.
                if n > 10:
                exit(0)
            else:
                print( str( datetime.now().strftime("%d-%m-%Y %H:%M")) + str(host) + ' ' + ip + ' is OK ')
            t.sleep(wait_sec)  # Делаем паузу.


### Вывод скрипта при запуске при тестировании:

    root@vagrant:/home/vagrant# python3 first_4.3.py
    Наши сервера: {'drive.google.com': '2.2.2.2', 'mail.google.com': '1.1.1.1', 'google.com': '8.8.8.8'}
    21-08-2022 17:15 drive.google.com 108.177.14.194 is OK
    21-08-2022 17:15 [ERROR] mail.google.com IP mistmatch: 64.233.161.18 64.233.161.17
    21-08-2022 17:15 google.com 173.194.73.100 is OK
    21-08-2022 17:15 drive.google.com 108.177.14.194 is OK
    21-08-2022 17:15 [ERROR] mail.google.com IP mistmatch: 64.233.161.18 64.233.161.17
    21-08-2022 17:15 [ERROR] google.com IP mistmatch: 64.233.163.101 173.194.73.139
    21-08-2022 17:15 drive.google.com 108.177.14.194 is OK
    21-08-2022 17:15 [ERROR] mail.google.com IP mistmatch: 64.233.161.18 64.233.161.17
    21-08-2022 17:15 [ERROR] google.com IP mistmatch: 173.194.73.101 173.194.73.139
    21-08-2022 17:15 drive.google.com 108.177.14.194 is OK
    21-08-2022 17:15 [ERROR] mail.google.com IP mistmatch: 64.233.161.18 64.233.161.17
    21-08-2022 17:15 [ERROR] google.com IP mistmatch: 173.194.73.139 173.194.73.138
    21-08-2022 17:15 drive.google.com 108.177.14.194 is OK
    21-08-2022 17:15 [ERROR] mail.google.com IP mistmatch: 64.233.161.19 64.233.161.83
    21-08-2022 17:15 [ERROR] google.com IP mistmatch: 173.194.73.101 173.194.73.113
    21-08-2022 17:15 drive.google.com 108.177.14.194 is OK
    21-08-2022 17:16 mail.google.com 64.233.161.17 is OK
    21-08-2022 17:16 [ERROR] google.com IP mistmatch: 173.194.73.101 173.194.73.138
    root@vagrant:/home/vagrant#

### json-файл(ы), который(е) записал ваш скрипт:

    root@vagrant:/home/vagrant# cat webservers.json
    {"drive.google.com": "108.177.14.194", "mail.google.com": "64.233.161.17", "google.com": "173.194.73.138"}

### yml-файл(ы), который(е) записал ваш скрипт:

    root@vagrant:/home/vagrant# cat webservers.yaml
    drive.google.com: 108.177.14.194
    google.com: 173.194.73.138
    mail.google.com: 64.233.161.17
    root@vagrant:/home/vagrant#

