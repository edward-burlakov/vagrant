#!/usr/bin/env python3

import socket as s
import time as t
from datetime import datetime


def inc(n):                                                  # Определяем функцию инкремента
    n = n + 1
    return n


wait_sec = 5  # интервал проверок в секундах                  # Устанавливаем переменные
n = 0         # счетчик итераций проверок

# Создаем объект списка с серверами и их исходными IP адресами:
webserver = {'drive.google.com':'2.2.2.2', 'mail.google.com':'1.1.1.1', 'google.com':'8.8.8.8'}
print( "Наши сервера:", webserver)

while [1 == 1]:

    for host in webserver:

        ip = s.gethostbyname(host)                        # Обращаемся в интернет и получаем очередной IP по имени хоста:

        if ip != webserver[host]:                         # Если значение IP не равно предыдущему - выводим строку ошибки:
            current_time = datetime.now()
            print( str(n)+'   '+ str(current_time.strftime("%d-%m-%Y %H:%M")) + ' [ERROR] ' + str(host) + ' IP mistmatch: ' +
                      webserver[host] + ' ' + ip)

            webserver[host] = ip                           # Записываем новое значение IP для данного сервера в список-буфер для следующей проверки:


            n = inc(n)                                     # Увеличиваем значение n на 1 и ограничиваем кол-во итераций опроса:
            if n > 10:
               exit(0)

            t.sleep(wait_sec)                             # Делаем паузу