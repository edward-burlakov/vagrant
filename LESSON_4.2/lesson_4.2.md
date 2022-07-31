
   ##     Самоучитель Python 3 для начинающих
   
        https://pythonworld.ru/samouchitel-python

   ##     Python 3.10.5 documentation

        https://docs.python.org/3/

# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос                                           | Ответ                                           |
|--------------------------------------------------|-------------------------------------------------|
| Какое значение будет присвоено переменной `c`?   | Строковое.  // >>> type(c) // <class 'str'>     |
| Как получить для переменной `c` значение 12?     | // >>> c = str(a) + b    // >>> print (c) // 12 |
| Как получить для переменной `c` значение 3?      | // >>> c = a + int(b) // >>> print (c) // 3     |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, 
какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, 
потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. 
Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:

<https://github.com/edward-burlakov/vagrant/blob/61aaeb87548eaa9bfd1dbd79f1088330f73d1ffc/LESSON_4.2/first.py>

    Убираем лишнюю переменную is_change  
    и команду break - прерывание процесса поиска изменённых файлов, при нахождении первого-же.  

    #!/usr/bin/env python3

    import os
    import pwd

    curruser = str(os.getlogin())                           # Выводим на экран имя текущего пользователя
    print("Текущий пользователь:", curruser )
   
    workdir = os.getcwd()                                   # Выводим на экран рабочий каталог пользователя
    print("Рабочий каталог:", workdir) 
    
    homedir = pwd.getpwuid(os.getuid()).pw_dir             # Определяем домашний каталог пользователя

    os.chdir( homedir+"/netology/sysadm-homeworks")        # Переходим в каталог с исходниками git
    gitdir = os.getcwd()
    print("Смена текущего рабочего каталога на проверяемый: {0} ".format( gitdir ))
    
    bash_command = ["git status"]                          # Получаем статус git репозитория
    
  
    print('\033[1;33;40m')
    result_os = os.popen(' && '.join(bash_command)).read()      # Читаем результат выполнения команды.
    for result in result_os.split('\n'):
        if result.find('modified') != -1:
             prepare_result = result.replace('\tmodified:   ', '')
             print( os.getcwd()+'/'+ prepare_result )
    print('\033[0m')

## Вывод скрипта при запуске при тестировании:

    vagrant@vagrant:~/$ python3 first.py
    Текущий пользователь: vagrant
    Рабочий каталог: /home/vagrant/netology/sysadm-homeworks/LESSON_4.2
    Смена текущего рабочего каталога на проверяемый: /home/vagrant/netology/sysadm-homeworks
    
    /home/vagrant/netology/sysadm-homeworks/LESSON_4.2/first.py
    /home/vagrant/netology/sysadm-homeworks/LESSON_4.2/second.py
    /home/vagrant/netology/sysadm-homeworks/LESSON_4.2/third.py

    vagrant@vagrant:~/$

## Обязательная задача 3
Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, 
а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. 
Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, 
которые не являются локальными репозиториями.

### Ваш скрипт:

<https://github.com/edward-burlakov/vagrant/blob/61aaeb87548eaa9bfd1dbd79f1088330f73d1ffc/LESSON_4.2/second.py>

    #!/usr/bin/env python3

    import os
    import sys
    
    if len(sys.argv) < 2:             # Проверяем наличие в аргументах проверяемого каталога репозитория
        print("Укажите проверяемый каталог репозитория в виде >python3 second.py [repository_directory] !!!")
        quit()
    else:
    
    curruser = str(os.getlogin())         #  Выводим имя текущего пользователя
    print("Текущий пользователь:", curruser)

    repodir = sys.argv[1]                 # Извлекаем проверяемый каталог из аргументов скрипта  
    print("Проверяемый каталог репозитория:", repodir)

    os.chdir(sys.argv[1])                 # Переходим в каталог с исходниками git  
    gitdir = os.getcwd()
    print("Смена текущего рабочего каталога на проверяемый: {0}     ".format(gitdir))
   
    bash_command = ["git status"]          # Получаем статус git репозитория
   
    print('\033[1;33;40m')
    result_os = os.popen(' && '.join(bash_command)).read()     # Читаем результат выполнения команды.
    for result in result_os.split('\n'):
        if result.find('modified') != -1:
             prepare_result = result.replace('\tmodified:   ', '')
             print( os.getcwd()+'/'+ prepare_result)
    print('\033[0m')

### Вывод скрипта при запуске при тестировании:

    vagrant@vagrant:~/$ python3 second.py ~/netology/sysadm-homeworks/
    Текущий пользователь: vagrant
    Проверяемый каталог репозитория: /home/vagrant/netology/sysadm-homeworks/
    Смена текущего рабочего каталога на проверяемый: /home/vagrant/netology/sysadm-homeworks
    
    /home/vagrant/netology/sysadm-homeworks/LESSON_4.2/first.py
    /home/vagrant/netology/sysadm-homeworks/LESSON_4.2/second.py
    /home/vagrant/netology/sysadm-homeworks/LESSON_4.2/third.py
    
    vagrant@vagrant:~/$


## Обязательная задача 4
Наша команда разрабатывает несколько веб-сервисов, доступных по http. 
Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис.

Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, 
поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. 
Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, 
который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, 
выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. 
Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. 
Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. 
Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:

<https://github.com/edward-burlakov/vagrant/blob/794dd9c77840492875beec4f739b2300e0627e59/LESSON_4.2/third.py>

    #!/usr/bin/env python3

    import socket as s
    import time as t
    from datetime import datetime

    def inc(n):                                          # Определяем функцию инкремента
        n = n + 1
        return n

    wait_sec = 4  # интервал проверок в секундах          # Устанавливаем переменные
    n = 1         # счетчик итераций проверок

    ### Создаем объект словаря  с серверами и их исходными IP адресами:
    webserver = {'drive.google.com': '2.2.2.2', 'mail.google.com': '1.1.1.1', 'google.com': '8.8.8.8'}   
    print( "Наши сервера:", webserver)                    

    while [1 == 1]:

    for host in webserver:        
        ip = s.gethostbyname(host)                         # Обращаемся в интернет и получаем очередной IP по имени хоста:
               if ip != webserver[host]:                   # Если значение IP не равно предыдущему - выводим строку ошибки:                 
            current_time = datetime.now()
            print( str(n)+'   '+ str(current_time.strftime("%d-%m-%Y %H:%M")) + ' [ERROR] ' + str(host) + ' IP mistmatch: ' +
                      webserver[host] + ' ' + ip)        
            webserver[host] = ip                           # Записываем новое значение IP для данного сервера в словарь-буфер для следующей проверки:
    
            n = inc(n)                                     # Увеличиваем значение n на 1 и ограничиваем кол-во итераций опроса:  
            if n > 10:
               exit(0)
        
            t.sleep(wait_sec)                              # Делаем паузу 

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
        10  31-07-2022 16:35 [ERROR] mail.google.com IP mistmatch: 173.194.73.19 173.194.73.17
        vagrant@vagrant:~/$

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. 
Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, 
то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, 
формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge 
мы наконец можем официально подтвердить, что новая конфигурация применена. 
Мы хотим максимально автоматизировать всю цепочку действий. 
Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, 
создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр 
при обращении к py-файлу (сообщение не может быть пустым). 
При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. 
С директорией локального репозитория можно делать всё, что угодно. 
Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, 
так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения.

### Ваш скрипт:
```python


### Вывод скрипта при запуске при тестировании:
```
