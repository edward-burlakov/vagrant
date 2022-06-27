Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

1) Какой системный вызов делает команда cd? В прошлом ДЗ мы выяснили, что cd не является самостоятельной программой, 
   это shell builtin, поэтому запустить strace непосредственно на cd не получится. 
   Тем не менее вы можете запустить 
   strace на /bin/bash -c 'cd /tmp'. 
   В этом случае вы увидите полный список системных вызовов, которые делает сам bash при старте. 
   Вам нужно найти тот единственный, который относится именно к cd. 
   Обратите внимание, что strace выдаёт результат своей работы в поток stderr, а не в stdout.

Ответ:

   Выводим:

      strace /bin/bash -c 'cd /tmp' 2<&1 | less

   Ищем системный вызов: 
    
      chdir("/tmp") 

2) Попробуйте использовать команду file на объекты разных типов на файловой системе. Например:

  
    vagrant@netology1:~$ file /dev/tty
    /dev/tty: character special (5/0)
    vagrant@netology1:~$ file /dev/sda
    /dev/sda: block special (8/0)
    vagrant@netology1:~$ file /bin/bash
    /bin/bash: ELF 64-bit LSB shared object, x86-64

Ответ:

     root@vagrant:~/test# file /dev/tty           
     /dev/tty: character special (5/0)
 
     root@vagrant:~/test# file /dev/sda*
     /dev/sda:  block special (8/0)
     /dev/sda1: block special (8/1)
     /dev/sda2: block special (8/2)
     /dev/sda3: block special (8/3)

     root@vagrant:~/test# file /bin/bash
     /bin/bash: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter 
     /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2a9f157890930ced4c3ad0e74fc1b1b84aad71e6, for GNU/Linux 3.2.0, stripped

   Используя strace выясните, где находится база данных file, на основании которой она делает свои догадки.

     1.Сначала база ищется в домашнем каталоге пользователя
     ~/.magic.mgc    -файл   
     ~/.magic        -каталог

     2. Затем база ищется в /etc
     /etc/magic.mgc - файл  
     /etc/magic     -  каталог

     3. База найдена в /usr/share/misc/magic.mgc  и  /usr/share/misc/magic  
     /usr/share/misc/magic.mgc  - символическая ссылка на искомый файл     /usr/lib/file/magic.mgc
     /usr/share/misc/magic      - символическая ссылка на искомый каталог  /usr/share/file/magic 

3)  Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), 
   однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. 
   Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. 
   Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла 
   (чтобы освободить место на файловой системе).
    
       
       root@vagrant:~/test#  apt-get install gdb            #  Устанавливаем  программу GBD

       root@vagrant:~/test#  tail -f /var/log/syslog > /root/test/trace &     # Запускаем вывод процесса в файл и посылаем в фон.

       root@vagrant:~/test# ps -aux | grep tail             # Получаем PID процесcа
       root        1302  0.0  0.0   5512   580 pts/0    S    07:07   0:00 tail -f /var/log/syslog
       root        1685  0.0  0.0   6300   720 pts/0    S+   07:49   0:00 grep --color=auto tail
    
       root@vagrant:~/test#  ls -l /proc/1302/fd            # Получаем список дескрипторов процесса
 
       total 0
       lrwx------ 1 root root 64 Jun 27 07:08 0 -> /dev/pts/0
       l-wx------ 1 root root 64 Jun 27 07:08 1 -> /root/test/trace
       lrwx------ 1 root root 64 Jun 27 07:08 2 -> /dev/pts/0
       lr-x------ 1 root root 64 Jun 27 07:08 3 -> /var/log/syslog
       lr-x------ 1 root root 64 Jun 27 07:08 4 -> anon_inode:inotify
  
       root@vagrant:~/test# lsof -p 1302                     # Ищем файл, в который пишется лог процесса tail
       COMMAND  PID USER   FD      TYPE DEVICE SIZE/OFF    NODE NAME
       tail    1302 root  cwd       DIR  253,0  1167360 1179762 /root/test
       tail    1302 root  rtd       DIR  253,0     4096       2 /
       tail    1302 root  txt       REG  253,0    72088 1051114 /usr/bin/tail
       tail    1302 root  mem       REG  253,0  3035952 1048854 /usr/lib/locale/locale-archive
       tail    1302 root  mem       REG  253,0  2029592 1049479 /usr/lib/x86_64-linux-gnu/libc-2.31.so
       tail    1302 root  mem       REG  253,0   191504 1049280 /usr/lib/x86_64-linux-gnu/ld-2.31.so
       tail    1302 root    0u      CHR  136,0      0t0       3 /dev/pts/0
       tail    1302 root    1w      REG  253,0     2968 1179656 /root/test/trace       # Файл , в который пишется лог
       tail    1302 root    2u      CHR  136,0      0t0       3 /dev/pts/0
       tail    1302 root    3r      REG  253,0   110984  131289 /var/log/syslog
       tail    1302 root    4r  a_inode  0,14        0   10385 inotify  

       root@vagrant:~/test#  gdb -p 1302  /usr/bin/tail   
       (gdb) p close(1)                                      # Закрываем  канал записи в несуществующий файл системным вызовом
       $1 = 0
       (gdb) p creat("/root/test/trace", 0600)               #  Cистемным вызовом пересоздаем  целевой файл trace 
       $2 = 1                                                # и перенаправляем вывод потока stdout команды tail в данный файл.
       (gdb) q                                               # Выходим из gdb  
       The program is running. Quit anyway (and detach it)? (y or n) y   # Оставляем программу tail запущенной 
       Detaching from program: /usr/bin/tail, process 1302       
 
       Итог: Файл trace очищенен без прерывания процесса логирования в него продожается писаться лог .       

4) Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

Ответ:

   Процессы-зомби в отличие от "сирот" не занимают ресурсы оперативной памяти (как процессы-сироты) и не грузят процессор .
   Но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом.

5) В iovisor BCC есть утилита opensnoop:
   root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
   /usr/sbin/opensnoop-bpfcc

Ответ:

   Утилита отслеживает системный вызов open(), показывая какие процессы пытаются открыть файлы и какие именно файлы.
   Это может быть полезно для определения местоположения конфигурационных и лог файлов, 
   или для траблшутинга приложений - что упало, особенно при запуске. 

    root@vagrant:~# /usr/sbin/opensnoop-bpfcc -d 1                        # Задаем ключем время работы команды 1 sec
    PID   COMM           FD ERR PATH
    1     systemd        12   0 /proc/606/cgroup                          # Процесс systemd обращается к файлу /proc/606/cgroup 
    865   vminfo          6   0 /var/run/utmp                             # Процесс vminfo обращается к файлу /var/run/utmp
    622   dbus-daemon    -1   2 /usr/local/share/dbus-1/system-services   # Процесс dbus-daemon обращается к несуществующему каталогу system-services
    622   dbus-daemon    20   0 /usr/share/dbus-1/system-services         # Процесс dbus-daemon обращается к каталогу system-services
    622   dbus-daemon    -1   2 /lib/dbus-1/system-services               # Процесс dbus-daemon обращается к несуществующему каталогу system-services  
    622   dbus-daemon    20   0 /var/lib/snapd/dbus-1/system-services/    # Процесс dbus-daemon обращается к пустому каталогу system-services

    
6) На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? 
   Воспользуйтесь пакетом bpfcc-tools для Ubuntu 20.04. Дополнительные сведения по установке.
   Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, 
   где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.
 
Ответ: 
   Вариант: 
      root@vagrant:~/test# uname -a

    Cиcтемный вызов uname - при запуске получает имя ядра и информацию о текущем ядре. 
 
   Вариант 2:

      root@vagrant:~/test# /usr/bin/lsb_release -a
      No LSB modules are available.
      Distributor ID: Ubuntu
      Description:    Ubuntu 20.04.4 LTS
      Release:        20.04
      Codename:       focal
   
   Вариант 3:
       Источник:  Manual page uname(2) line 58/76

      root@vagrant:/home/vagrant#  cat /proc/sys/kernel/ostype  /proc/sys/kernel/hostname  /proc/sys/kernel/osrelease
      /proc/sys/kernel/version  /proc/sys/kernel/domainname
      Linux
      vagrant
      5.4.0-110-generic
      #124-Ubuntu SMP Thu Apr 14 19:46:19 UTC 2022
      (none)
      
6) Чем отличается последовательность команд через ; и через && в bash? Например:

   Ответ:
   #  shell BASH просто выполнит эти команды последовательно:  

       root@netology1:~# test -d /tmp/some_dir; echo Hi
       Hi

  #  Shell BASH выполнит вторую команду поcле оператора оператор AND (&&)
  #  только в том случае, если при выполнении первой команды SUCCEEDS, 
  #  т.е. состояние выхода первой команды равно «0» — программа выполнена успешно.  
  #  Команда test проверила, что  файл /tmp/some_dir не существует 
  #  и не является каталогом и получила в выходной поток stdout значение ошибки - "1" .
  #  Поэтому последовательность команд был остановлена.

       root@netology1:~# test -d /tmp/some_dir && echo Hi   
       root@netology1:~#   

7) Есть ли смысл использовать в bash &&, если применить set -e?

    Из каких опций состоит режим bash set -euxo pipefail и почему его хорошо было бы использовать в сценариях?
    Используя -o stat для ps, определите, какой наиболее часто встречающийся статус у процессов в системе. 
    В man ps ознакомьтесь (/PROCESS STATE CODES) что значат дополнительные к основной заглавной буквы статуса процессов. 
    Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

Ответ:

   Это не имеет смысла, так как вторая команда никогда не будет выполнена.
   Если первая команда неуспешна (В выходной потоке stdout - "1") - работа конвейера будет завершена принудительно из-за set -e.
   Если первая команда успешна (В выходном потоке stdout -"0" ) - работа конвейера по правилам оператора "&&" прекратится. 
   

Опции режима bash set -euxo pipefail

   -e Прерывает процесс, если результат выполнения очередной команды не равен "0"(Успех) .
      В скриптах заставляет скрипт завершить работу, если любой из вызываемых им процессов 
      выдает ненулевой код возврата.Все, что не равно нулю, считается неудачей.

   -x Печатать команды и их аргументы по мере их выполнения.

   -o pipefail.  
      Статусом выхода из конвейера, в том случае, если не включена опция pipefail, 
      служит статус завершения последней команды конвейера. 
      Если опция pipefail включена — Статус выхода из конвейера равен статусу выхода последней (самой правой) 
      команды, завершённой с ненулевым статусом ( "Ошибка"), или "0" — если работа всех команд завершена успешно.

   -u Рассматривать неинициализированные переменные как ошибку при подстановке -1 ( "Ошибка").
      Неинициализированные переменные очень трудно обнаружить в реальном сценарии.
      При этом сообщение об ошибке не появляется. Остальная часть сценария продолжит выполняться.

  В сценариях удобно использовать вышеуказанные опции, потому что команды выводятся на экран одна за другой, 
  и последней выведенной команда и аргументами будет та команда, которая выполнена со статусом ошибки.
  Также можно легко посмотреть ее статус ошибки.
                           