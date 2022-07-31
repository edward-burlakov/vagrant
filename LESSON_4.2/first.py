#!/usr/bin/env python3

import os
import pwd

# Выводим на экран имя текущего пользователя
    curruser = str(os.getlogin())
    print("Текущий пользователь:", curruser )

# Выводим на экран рабочий каталог пользователя
    workdir = os.getcwd()
    print("Рабочий каталог:", workdir)

# Определяем домашний каталог пользователя
    homedir = pwd.getpwuid(os.getuid()).pw_dir

# Переходим в каталог  с исходниками git
    os.chdir( homedir+"/netology/sysadm-homeworks")
    gitdir = os.getcwd()
    print("Смена текущего рабочего каталога на проверяемый: {0} ".format( gitdir ))

# Получаем статус git репозитория
    bash_command = ["git status"]

# Читаем результат выполнения команды.
    print('\033[1;33;40m')
    result_os = os.popen(' && '.join(bash_command)).read()
    for result in result_os.split('\n'):
        if result.find('modified') != -1:
             prepare_result = result.replace('\tmodified:   ', '')
             print( os.getcwd()+'/'+ prepare_result )
    print('\033[0m')