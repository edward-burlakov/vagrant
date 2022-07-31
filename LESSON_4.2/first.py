#!/usr/bin/env python3

import os
import pwd

# Выводим на экран имя текущего пользователя
curruser = str(os.getlogin())
print("Текущий пользователь:", curruser )

# Выводим на экран рабочий каталог пользователя
currdir = os.getcwd()
print("Рабочий каталог:", currdir)

# Определяем домашний каталог пользователя
homedir = pwd.getpwuid(os.getuid()).pw_dir

# Переходим в каталог  с исходниками git
os.chdir( homedir+"/netology/sysadm-homeworks")
currdir = os.getcwd()
print("Смена текущего рабочего каталога на проверяемый: {0} ".format( currdir ))

# Получаем статус git репозитория
bash_command = ["git status"]

# Читаем результат выполнения команды.
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
         prepare_result = result.replace('\tmodified:   ', '')
         print(prepare_result)