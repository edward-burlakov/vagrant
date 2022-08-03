#!/usr/bin/env python3

import os
import pwd

curruser = str(os.getlogin())                 # Выводим на экран имя текущего пользователя
print("Текущий пользователь:", curruser )


workdir = os.getcwd()                         # Выводим на экран рабочий каталог пользователя
print("Рабочий каталог:", workdir)


homedir = pwd.getpwuid(os.getuid()).pw_dir    # Определяем домашний каталог пользователя


os.chdir( homedir+"/netology/sysadm-homeworks")  # Переходим в каталог  с исходниками git
gitdir = os.getcwd()
print("Смена текущего рабочего каталога на проверяемый: {0} ".format( gitdir ))


bash_command = ["git status"]                  # Получаем статус git репозитория


print('\033[1;33;40m')                         # Читаем результат выполнения команды.
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
        if result.find('modified') == 1:
             prepare_result = result.replace('\tmodified:   ', '')
             print( os.getcwd()+'/'+ prepare_result )
print('\033[0m')