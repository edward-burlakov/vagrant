#!/usr/bin/env python3

import os
import sys

# Проверяем наличие в аргументах проверяемого каталога репозитория
if len(sys.argv) < 2:
    print("Укажите проверяемый каталог репозитория !!!")
    quit()
else:

# Выводим имя текущего пользователя
    curruser = str(os.getlogin())
    print("Текущий пользователь:", curruser)

# Извлекаем проверяемый каталог из аргументов скрипта
    checkdir = sys.argv[1]
    print("Проверяемый каталог репозитория:", checkdir)

# Переходим в каталог с исходниками git
    os.chdir(sys.argv[1])
    currdir = os.getcwd()
    print("Смена текущего рабочего каталога на проверяемый: {0}     ".format(currdir))

# Получаем статус git репозитория
    bash_command = ["git status"]

# Читаем результат выполнения команды.
    print("Изменённые файлы:")
    result_os = os.popen(' && '.join(bash_command)).read()
    for result in result_os.split('\n'):
        if result.find('modified') != -1:
              prepare_result = result.replace('\tmodified:   ', '')
              print(prepare_result)
