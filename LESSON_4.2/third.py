#!/usr/bin/env python3

import os
import sys
import time
import shutil
import tempfile
import urllib.request

while [1==1]:
#  По умолчанию команда curls проверяет доступность web-сервиса.
#  Статус выполнения предыдущей команды $? равный 0 означает успех.
#  Ненулевой возвращаемый статус выполнения предыдущей команды $? обозначает ошибку.


with urllib.request.urlopen('http://googleython.org/') as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

with open(tmp_file.name) as html:
    pass

