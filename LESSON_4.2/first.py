#!/usr/bin/env python3
import os

      #  Переходим в каталог  с исходниками git и получаем статус git репозитория
      #  bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]

      #  Open a pipe to or from command cmd.
      #  The return value is an open file object connected to the pipe, which can be read
      #  or written depending on whether mode is 'r' (default) or 'w'.
      #  The buffering argument has the same meaning as the corresponding argument to the built-in open() function.
      #  The returned file object reads or writes text strings rather than bytes.

os.chdir ("C:\Users\med1094\PycharmProjects\Vagrant\")
cmd = "git status"

# Читаем результат выполнения команды.

result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
         prepare_result = result.replace('\tmodified:   ', '')
         print(prepare_result)
         break