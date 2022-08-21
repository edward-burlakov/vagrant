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

В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.
Ваш скрипт:

#!/usr/bin/env python3
# Скрипт проверяет изменение IP адресов переданныйх на вход
import socket
from time import sleep
import os
import json
import yaml

tlist = {'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
n = 1


# Функция заполнения словаря Актуальными IP адресами
def fill_tlist(x):
    for node in x:
        ipaddres = socket.gethostbyname(node)
        x[node] = ipaddres
    return x


# запись в формате json \ yaml
def fill_json_yaml(y):
    with open('hosts.json', 'w') as jtmp:
        jtmp.write(str(json.dumps(y)))
    with open('hosts.yaml', 'w') as ytmp:
        ytmp.write(yaml.dump(y))
    return


# заполним словарь и запишем YAML\JSON чтобы был актуальный спикок всегда
fill_json_yaml(fill_tlist(tlist))


# цикл проверки изменения адреса. цикл прерывается при изменениях и записывает последние актуальные адреса в JSON \ YAML
while n != 0:
    tmp = fill_tlist(tlist)
    sleep(1)
    os.system('cls')
    for host in tmp:
        ipaddress = socket.gethostbyname(host)
        if ipaddress != tmp[host]:
            print(' [ERROR] ' + str(host) + ' IP mistmatch: ' + tmp[host] + ' ---> ' + ipaddress)
            tmp[host] = ipaddress
            fill_json_yaml(tmp)
            n = 0
        else:
            print(str(host) + ' ' + ipaddress + ' OK ')

Вывод скрипта при запуске при тестировании:

C:\repo\netology>script2.py
drive.google.com 173.194.73.194 OK
mail.google.com 64.233.165.17 OK
google.com 64.233.161.100 OK
