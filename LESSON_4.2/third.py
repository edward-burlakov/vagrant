#!/usr/bin/env python3

import os
import sys
import time
import shutil
import tempfile
import urllib.request

# while [1==1]:
#  По умолчанию команда curls проверяет доступность web-сервиса.
#  Статус выполнения предыдущей команды $? равный 0 означает успех.
#  Ненулевой возвращаемый статус выполнения предыдущей команды $? обозначает ошибку.


req = urllib.request.Request('http://www.google.com')
with urllib.request.urlopen(req) as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)
    the_page = response.read()
# print(the_page)

# with open(tmp_file.name) as html:
#    pass

