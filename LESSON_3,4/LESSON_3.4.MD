1) На лекции мы познакомились с node_exporter. В демонстрации его исполняемый файл запускался в background.
   Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. 
   Используя знания из лекции по systemd, создайте самостоятельно простой unit-файл для node_exporter:
   поместите его в автозагрузку,
   предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на systemctl cat cron),
   удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается. 

Ответ :

1. Добавляем системного пользователя, от которого будет работать Node Exporter

       root@vagrant:/# sudo useradd -r -M -s /bin/false node_exporter

2. Скачиваем node_exporter-1.3.1

       root@vagrant:/# wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz    -P /tmp
       root@vagrant:/# cd /tmp

3. Распаковываем, переносим в каталог /usr/local/bin, назначаем владельца

       root@vagrant:/# tar -zxpvf node_exporter-1.3.1.linux-amd64.tar.gz
       root@vagrant:/# cd node_exporter-1.3.1.linux-amd64
       root@vagrant:/# sudo cp node_exporter /usr/local/bin
       root@vagrant:/# sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter

4. Создаем Systemd Unit
   
       root@vagrant:/# sudo nano /etc/systemd/system/node_exporter.service

       [Unit]
       Description=Prometheus Node Exporter
       Wants=network-online.target
       After=network-online.target
      
       [Service]
       User=node_exporter
       Group=node_exporter
       Type=simple
       ExecStart=/usr/local/bin/node_exporter
      
       [Install]
       WantedBy=multi-user.target

5. Добавляем сервис в автозагрузку, запускаем его, проверяем статус

       root@vagrant:/# sudo systemctl daemon-reload

       root@vagrant:/# sudo systemctl enable --now node_exporter

       root@vagrant:/# sudo systemctl status node_exporter | grep  active

       Active: active (running) since Fri 2022-07-01 23:27:05 +07; 19min ago

6. Проверяем работу сокета

     root@vagrant:/# sudo ss -pnltu | grep 9100

       tcp     LISTEN   0    4096     *:9100    *:*      users:(("node_exporter",pid=1529,fd=3))

7. Проверяем, что сервис добавлен в автозагрузку:

       root@vagrant:/# systemctl list-unit-files --type=service --state=enabled  | grep  node_exporter
       node_exporter.service     enabled enabled

8. Останавливаем сервис, проверяем его статус опять стартуем и проверяем:
      
        root@vagrant:/# systemctl stop  node_exporter.service
   
        root@vagrant:/# systemctl  status node_exporter.service | grep Active:

        Active: inactive (dead) since Sat 2022-07-02 00:11:40 +07; 2min 40s ago
     
        root@vagrant:/# systemctl  start node_exporter.service

     root@vagrant:/# systemctl  status node_exporter.service | grep Active:
 
       Active: active (running) since Sat 2022-07-02 00:20:12 +07; 36s ago
     

2) Ознакомьтесь с опциями node_exporter и выводом /metrics по-умолчанию. 
   Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.
   
Ответ: 
     
Проверяем работу метрик

      root@vagrant:~# curl http://localhost:9100/metrics
      # HELP go_gc_duration_seconds A summary of the pause duration of garbage collect                                                                                                              ion cycles.
      # TYPE go_gc_duration_seconds summary
      go_gc_duration_seconds{quantile="0"} 0
      go_gc_duration_seconds{quantile="0.25"} 0
      go_gc_duration_seconds{quantile="0.5"} 0
      go_gc_duration_seconds{quantile="0.75"} 0
      go_gc_duration_seconds{quantile="1"} 0
      go_gc_duration_seconds_sum 0
      go_gc_duration_seconds_count 0
      
      ... и т.д.

Рекомендованные опции для добавления в /etc/systemd/system/node_exporter.service  
помещаем в отдельный файл в /etc/.node_exporter.conf  :

         root@vagrant:/#  touch /etc/.node_exporter.conf   
         root@vagrant:/#  nano /etc/.node_exporter.conf
            ARG1=--collector.cpu
            ARG2=--collector.meminfo 
            ARG3=--collector.diskstats 
            ARG4=--collector.ethtool 
            ARG5=--web.telemetry-path="/metrics" '

Добавляем в раздел [Service]  файла /etc/systemd/system/node_exporter.service
  следующие строки :

         EnvironmentFile=/etc/.node_exporter.conf
         ExecStart = ExecStart=/usr/local/bin/node_exporter $ARG1 $ARG2 $ARG3 $ARG4 $ARG5

3) Установите в свою виртуальную машину Netdata. Воспользуйтесь готовыми пакетами для установки (sudo apt install -y netdata). 
   После успешной установки:
   в конфигурационном файле /etc/netdata/netdata.conf в секции [web] замените значение с localhost на bind to = 0.0.0.0, 
   добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте vagrant reload:
   config.vm.network "forwarded_port", guest: 19999, host: 19999

Ответ:   

    root@vagrant:~# sudo apt install -y netdata
    root@vagrant:~# echo /etc/netdata/netdata.conf
    ...
    [web]
    bind to = 0.0.0.0
    ...

   После успешной перезагрузки в браузере на своем ПК (не в виртуальной машине) вы должны суметь зайти на localhost:19999. 
   Ознакомьтесь с метриками, с которыми по умолчанию собираются Netdata и с комментариями, что даны к этим метрикам.

Ответ :    

      https://github.com/edward-burlakov/vagrant/blob/main/netdata_screenshot.jpg

      Готово. Впечатляет. 
      


4) Можно ли по выводу dmesg понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

Ответ:

     vagrant@vagrant:~$ dmesg | grep virtual
     [    0.007087] CPU MTRRs all blank - virtualized system.
     [    0.056585] Booting paravirtualized kernel on KVM
     [   31.151645] systemd[1]: Detected virtualization oracle.



5) Как настроен sysctl fs.nr_open на системе по-умолчанию? Узнайте, что означает этот параметр. 
   Какой другой существующий лимит не позволит достичь такого числа (ulimit --help)?

Ответ:
  
    Параметр nr_open - жесткий лимит на  количество открытых дескрипторов в системе.
       
       root@vagrant:~# sysctl fs.nr_open
       fs.nr_open = 1048576

    или 
    
       root@vagrant:~# cat /proc/sys/fs/nr_open
       1048576

    Утилита ulimit позволяет модифицировать ресурсы оболочки. 
    Обеспечивает ограничение ресурсов, доступных оболочке bash и запускаемым в ней процессам.  

    Ниже указан лимит на максимальное количество одновременно открытых файловых дескрипторов  в bash

       root@vagrant:~# ulimit -a | grep open
       open files                      (-n) 1024

       root@vagrant:~# ulimit -Sn
       1024

    - мягкий лимит "soft" (так же ulimit -n)на пользователя (может быть увеличен самими процессами при выполнении)

       root@vagrant:~# ulimit -Hn
       1048576

    - жесткий лимит "hard" на пользователя (не может быть увеличен, только уменьшен)

     Оба ulimit -n НЕ могут превысить системный параметр fs.nr_open
     
     Для подсчета общего числа файлов, открытых в ТЕКУЩИЙ МОМЕНТ  в системе  используем
     первое значение в выводе команды "cat /proc/sys/fs/file-nr" :

       root@vagrant:~# cat /proc/sys/fs/file-nr
       1472    0       9223372036854775807


6) Запустите любой долгоживущий процесс (не ls, который отработает мгновенно, а, например, sleep 1h ) 
   в отдельном неймспейсе процессов; 
   покажите, что ваш процесс работает под PID 1 через nsenter. 
   Для простоты работайте в данном задании под root (sudo -i). 
   Под обычным пользователем требуются дополнительные опции (--map-root-user) и т.д.

Ответ:
 
Запускаем два идентичных процесса в разных пространствах-namespace: 

        root@vagrant:/home/vagrant# which sleep
        /usr/bin/sleep

        root@vagrant:/home/vagrant# sleep 1h  &
        [1] 142268

        root@vagrant:/home/vagrant# ps -aux | grep sleep
        root      142268  0.0  0.0   5476   580 pts/0    S    22:48   0:00 sleep 1h
        root      142271  0.0  0.0   6432   720 pts/0    S+   22:48   0:00 grep --color=auto sleep

        root@vagrant:/home/vagrant# unshare -f --pid --mount-proc /usr/bin/sleep 1h &
        [2] 142299

        root@vagrant:/home/vagrant# ps -aux | grep sleep
        root      142268  0.0  0.0   5476   580 pts/0    S    22:48   0:00 sleep 1h
        root      142298  0.0  0.0   5476   580 pts/0    S    22:55   0:00 /usr/bin/sleep 1h
        root      142299  0.0  0.0   5480   580 pts/0    S    22:55   0:00 unshare -f --pid --mount-proc /usr/bin/sleep 1h
        root      142300  0.0  0.0   5476   516 pts/0    S    22:55   0:00 /usr/bin/sleep 1h
        root      142316  0.0  0.0   6432   656 pts/0    S+   22:58   0:00 grep --color=auto sleep


... где 142268 -  Первый процесс sleep:

            142268 pts/0    S    22:55   0:00 /usr/bin/sleep 1h

... а  142300   - Второй процесс sleep, запущенный в изолированном по PID неймспейсе:

            142300  pts/0    S    22:55   0:00 /usr/bin/sleep 1h

Входим внутрь пространства-namespace с PID 142300  :

        root@vagrant:~#  nsenter --target 142300 --pid --mount
        root@vagrant:/#

Убедимся, что процесс sleep имеет родительский номер PID, равный 1 :

        root@vagrant:/# ps  aux
        USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
        root           1  0.0  0.0   5476   516 pts/0    S    22:55   0:00 /usr/bin/sleep 1h
        root           4  0.0  0.2   7356  4124 pts/0    S    23:21   0:00 -bash
        root          15  0.0  0.1   8888  3284 pts/0    R+   23:21   0:00 ps aux


7) Найдите информацию о том, что такое :(){ :|:& };:. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04
   (это важно, поведение в других ОС не проверялось). Некоторое время все будет "плохо", 
   после чего (минуты) – ОС должна стабилизироваться. 
   Вызов dmesg расскажет, какой механизм помог автоматической стабилизации. 
   Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

   Идут непрерывно сообщения 
   bash: fork: retry: Resource temporarily unavailable.

   Это форк-бомба.

   Источник:

   https://itsecforu.ru/2021/12/21/%F0%9F%92%A3-%D1%84%D0%BE%D1%80%D0%BA-%D0%B1%D0%BE%D0%BC%D0%B1%D0%B0-%D0%BD%D0%B0-linux/
  
        : – это имя функции
        :|: вызывает саму функцию и порождает другой процесс
        & переводит процесс в фоновый режим, чтобы его нельзя было легко убить
        ; отмечает конец функции
        : снова вызывает функцию

   Лучший способ наложить ограничение на количество процессов, которые может порождать пользователь, 
   – это отредактировать файл /etc/security/limits.conf. 
   В нем мы можем указать как на отдельного пользователя, так и на группу.
   Например, для root ставим ограничение на 100 процессов - добавляем запись

        root@vagrant:~# vim  /etc/security/limits.conf
        >  root hard nproc 100

   Или устанавливаем лимит числа процессов с помощью ulimit для пользователя:
   
       ulimit -u 100 число процессов будет ограничено 100. 