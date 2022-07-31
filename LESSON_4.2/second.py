#!/usr/bin/env python3

import os
import sys


if  len(sys.argv) < 2:              # Проверяем наличие в аргументах проверяемого каталога репозитория
    print("Укажите проверяемый каталог репозитория в виде >python3 first.py [repository_directory] !!!")
    quit()
else:

    curruser = str(os.getlogin())   # Выводим имя текущего пользователя
    print("Текущий пользователь:", curruser)


    repodir = sys.argv[1]           # Извлекаем проверяемый каталог из аргументов скрипта
    print("Проверяемый каталог репозитория:", repodir)


    os.chdir(sys.argv[1])            # Переходим в каталог с исходниками git
    gitdir = os.getcwd()
    print("Смена текущего рабочего каталога на проверяемый: {0}     ".format(gitdir))


    bash_command = ["git status"]    # Получаем статус git репозитория


    print('\033[1;33;40m')            # Читаем результат выполнения команды.
    result_os = os.popen(' && '.join(bash_command)).read()
    for result in result_os.split('\n'):
        if result.find('modified') != -1:
             prepare_result = result.replace('\tmodified:   ', '')
             print( os.getcwd()+'/'+prepare_result)
    print('\033[0m')