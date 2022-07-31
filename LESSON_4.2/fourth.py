#!/usr/bin/env python3

# import os
# import sys
# import shutil
# import tempfile
import socket
from datetime import datetime
time = datetime.now()
print(time.strftime("%d-%m-%Y %H:%M"))

# ваша ОС отправит запрос на удаленный DNS сервер

#print(socket.gethostbyname('google.com'))
#print(socket.gethostbyname('google.com'))
#print(socket.gethostbyname('google.com'))



print(socket.gethostbyname_ex("drive.google.com"))
print(socket.gethostbyname_ex("mail.google.com"))
print(socket.gethostbyname_ex("google.com"))


