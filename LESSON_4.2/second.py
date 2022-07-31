#!/usr/bin/env python3

import os
import sys

# Проверяем наличие в аргументах проверяемого каталога репозитория
if len(sys.argv) < 2:
    print("Укажите проверяемый каталог репозитория в виде >python3 first.py [repository_directory] !!!")
    quit()
else:

# Выводим имя текущего пользователя
    curruser = str(os.getlogin())
    print("Текущий пользователь:", curruser)

# Извлекаем проверяемый каталог из аргументов скрипта
    repodir = sys.argv[1]
    print("Проверяемый каталог репозитория:", repodir)

# Переходим в каталог с исходниками git
    os.chdir(sys.argv[1])
    gitdir = os.getcwd()
    print("Смена текущего рабочего каталога на проверяемый: {0}     ".format(gitdir))

# Получаем статус git репозитория
    bash_command = ["git status"]

# Читаем результат выполнения команды.
    print('\033[1;33;40m')
    print("Изменённые файлы:")
    # Читаем результат выполнения команды.
    result_os = os.popen(' && '.join(bash_command)).read()
    for result in result_os.split('\n'):
        if result.find('modified') != -1:
             prepare_result = result.replace('\tmodified:   ', '')
             print( os.getcwd()+'/'+ prepare_result)
    print('\033[0m')