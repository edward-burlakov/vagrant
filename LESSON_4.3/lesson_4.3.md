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
    import os
    import json
    import yaml
    
### Определяем функцию инкремента.

def inc(n):
    n = n + 1
    return n

### Создаем объект словаря с серверами и их исходными IP адресами:

  webservers = {'drive.google.com': '2.2.2.2', 'mail.google.com': '1.1.1.1', 'google.com': '8.8.8.8'}
  print("Наши сервера:", webservers)

### Устанавливаем счетчик  
n = 1

# Функция заполнения объекта словаря актуальными IP адресами

def fill_dictionary(x):
    for node in x:
         ip = socket.gethostbyname(node)
         x[node] = ip
    return x

# Функция формирования словаря в формате json в файл  webservers.json

def fill_json(y):
    with open('webservers.json', 'w') as jtmp:
         jtmp.write(str(json.dumps(y)))        # Сериализация  объекта Python в строку формата JASON
    return

# Функция формирования словаря в формате yaml в файл  webservers.yaml

def fill_yaml(z):
    with open('webservers.yaml', 'w') as ytmp:
         ytmp.write(yaml.dump(z))             # Сериализация  объекта Python в строку формата YAML
    return

# Заполняем словарь и запишем YAML и JSON файлы, чтобы в них был актуальный список адресов
  fill_json(fill_dictionary(webservers))
  fill_yaml(fill_dictionary(webservers))

Варинат 1

# цикл проверки изменения адреса. цикл прерывается при изменениях и записывает последние актуальные адреса в JSON \ YAML
while n != 0:
    tmp = fill_tlist(webservers)
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

# Вариант 2


while True:

        tmp = fill_dictionary(webservers)   # Создаем временную копию словаря .
        os.system('cls')                    # Очищаем консоль
        for host in webservers:
            ip = s.gethostbyname(host)  # Обращаемся в интернет и получаем очередной IP по имени хоста.

            if ip != tmp[host]:  # Если значение IP не равно предыдущему - выводим строку ошибки.
                current_time = datetime.now()
                print(str(n) + '   ' + str(current_time.strftime("%d-%m-%Y %H:%M")) + ' [ERROR] ' + str(
                    host) + ' IP mistmatch: ' + tmp[host] + ' ' + ip)

                tmp[host] = ip  # Записываем новое значение IP для данного сервера в словарь-буфер для следующей проверки.
                fill_json(tmp)  # Дублируем изменения в файл webservers.json
                fill_yaml(tmp)  # Дублируем изменения в файл webservers.yaml
                n = inc(n)  # Увеличиваем значение n на 1 и ограничиваем кол-во итераций опроса.
                if n > 10:
                exit(0)
            else:
               print(str(host) + ' ' + ip + 'is OK ')
            t.sleep(wait_sec)  # Делаем паузу.


Вывод скрипта при запуске при тестировании:

### Вывод скрипта при запуске при тестировании:

        vagrant@vagrant:~/$  python3 third.py
        Наши сервера: {'drive.google.com': '2.2.2.2', 'mail.google.com': '1.1.1.1', 'google.com': '8.8.8.8'}
        1   31-07-2022 16:34 [ERROR] drive.google.com IP mistmatch: 2.2.2.2 142.251.1.194
        2   31-07-2022 16:34 [ERROR] mail.google.com IP mistmatch: 1.1.1.1 173.194.73.17
        3   31-07-2022 16:34 [ERROR] google.com IP mistmatch: 8.8.8.8 74.125.131.101
        4   31-07-2022 16:34 [ERROR] mail.google.com IP mistmatch: 173.194.73.17 173.194.73.83
        5   31-07-2022 16:34 [ERROR] mail.google.com IP mistmatch: 173.194.73.83 173.194.73.17
        6   31-07-2022 16:34 [ERROR] google.com IP mistmatch: 74.125.131.101 74.125.131.139
        7   31-07-2022 16:34 [ERROR] google.com IP mistmatch: 74.125.131.139 74.125.131.101
        8   31-07-2022 16:34 [ERROR] mail.google.com IP mistmatch: 173.194.73.17 173.194.73.19
        9   31-07-2022 16:35 [ERROR] google.com IP mistmatch: 74.125.131.101 74.125.131.100
        10   31-07-2022 16:35 [ERROR] mail.google.com IP mistmatch: 173.194.73.19 173.194.73.17
        vagrant@vagrant:~/$
