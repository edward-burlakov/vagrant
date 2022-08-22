# !/usr/bin/env python3
# Скрипт проверяет изменение IP-адресов переданных на вход
import socket as s
import time as t
from datetime import datetime
import json
import yaml


#  Определяем функцию инкремента.

def inc(n1):
    n1 = n1 + 1
    return n1


# Задаем интервал проверок в секундах.
wait_sec = 4

# Устанавливаем счетчик итераций проверок.
n = 1

# Создаем объект словаря с серверами и их исходными адресами:
webservers = {'drive.google.com': '2.2.2.2', 'mail.google.com': '1.1.1.1', 'google.com': '8.8.8.8'}
print("Наши сервера:", webservers)


# Функция заполнения объекта словаря актуальными адресами:
def fill_dictionary(x):
    for node in x:
        ipaddress = s.gethostbyname(node)
        x[node] = ipaddress
    return x


# Функция формирования словаря в формате json в файле  webservers.json
def fill_json(y):
    with open('webservers.json', 'w') as jtmp:
        jtmp.write(str(json.dumps(y)))  # Сериализация объекта Python в строку формата JASON
    return None


# Функция формирования словаря в формате yaml в файле  webservers.yaml
def fill_yaml(z):
    with open('webservers.yaml', 'w') as ytmp:
        ytmp.write(yaml.dump(z))  # Сериализация объекта Python в строку формата YAML
    return None


# Заполняем YAML и JSON файлы, чтобы в них был актуальный список адресов
fill_json(fill_dictionary(webservers))
fill_yaml(fill_dictionary(webservers))

while True:
    tmp = fill_dictionary(webservers)  # Создаем временную копию словаря.
    for host in webservers:
        ip = s.gethostbyname(host)  # Обращаемся в интернет и получаем очередной IP-адрес по имени хоста.
        if ip != tmp[host]:  # Если значение IP-адреса не равно предыдущему - выводим строку ошибки.

            print(str(datetime.now().strftime("%d-%m-%Y %H:%M")) + ' [ERROR] ' + str(host)
                  + ' IP mistmatch: ' + tmp[host] + ' ' + ip)
            tmp[host] = ip  # Записываем новое значение IP для данного сервера в словарь-буфер для следующей проверки.
            fill_json(tmp)  # Дублируем изменения в файл webservers.json
            fill_yaml(tmp)  # Дублируем изменения в файл webservers.yaml
            n = inc(n)  # Увеличиваем значение n на 1 и ограничиваем кол-во итераций опроса.
            if n > 10:
                exit(0)
        else:
            print(str(datetime.now().strftime("%d-%m-%Y %H:%M")) + ' ' + str(host) + ' ' + ip + ' is OK ')
        t.sleep(wait_sec)  # Делаем паузу.
