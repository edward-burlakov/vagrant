##!/usr/bin/env python3

import socket as s
import time as t
from datetime import datetime



# set variables
i = 0    # счетчик проверок
wait = 2 # интервал проверок в секундах
# Задаем массив серверов с их исходными IP адресами:
webservers = {'drive.google.com':'2.2.2.2', 'mail.google.com':'1.1.1.1', 'google.com':'8.8.8.8'}
init=0

print('*** start script ***')
print(webservers)
print('********************')

while [1==1] :
#Ограничение числа проверок
  i += 1
  if i >= 10:
    exit(0)

  for host in webservers:
# Получаем IP адрес хоста
    ip = s.gethostbyname(host)
# Если значение IP не равно предыдущему - выводим строку ошибки.
    if ip != srv[host]:
      if i==1 and init !=1:
        current_time = datetime.now()
        print(str(current_time.strftime("%d-%m-%Y %H:%M")) +' [ERROR] ' + str(host) +' IP mistmatch: '+srv[host]+' '+ip)
      Записываем значение IP в буфер для следующей проверки
      srv[host]=ip
  t.sleep(wait)