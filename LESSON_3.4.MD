Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

1) На лекции мы познакомились с node_exporter. В демонстрации его исполняемый файл запускался в background. 
   Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. 
   Используя знания из лекции по systemd, создайте самостоятельно простой unit-файл для node_exporter:
   - поместите его в автозагрузку
   - предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на systemctl cat cron),
   - удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.


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

8. Останавливаем сервис, проверяем его статус м опять стартуем и проверяем :
      
       root@vagrant:/# systemctl stop  node_exporter.service
   
       root@vagrant:/# systemctl  status node_exporter.service | grep Active:

       Active: inactive (dead) since Sat 2022-07-02 00:11:40 +07; 2min 40s ago
     
       root@vagrant:/# systemctl  start node_exporter.service

       root@vagrant:/# systemctl  status node_exporter.service | grep Active:
 
       Active: active (running) since Sat 2022-07-02 00:20:12 +07; 36s ago

     

2) Ознакомьтесь с опциями node_exporter и выводом /metrics по-умолчанию. 
   Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.
    
Ответ: Рекомендованные опции для добавления  в  /etc/systemd/system/node_exporter.service :

    root@vagrant:/etc/systemd/system# cat /etc/systemd/system/node_exporter.service  | grep ExecStart

    ExecStart=/usr/local/bin/node_exporter  --collector.cpu  --collector.meminfo --collector.diskstats --collector.ethtool --web.telemetry-path="/metrics"

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
       
       root@vagrant:/home/vagrant# sysctl fs.nr_open
       fs.nr_open = 1048576

    или 
    
       root@vagrant:/etc/sysctl.d# cat /proc/sys/fs/nr_open
       1048576

    Утилита ulimit позволяет модифицировать ресурсы оболочки. 
    Обеспечивает ограничение ресурсов, доступных оболочке bash и запускаемым в ней процессам.  

    Ниже указан лимит на максимальное количество одлновременно открытых файлов  в bash

       root@vagrant:/etc/sysctl.d# ulimit -a | grep open
       open files                      (-n) 1024

    Для подсчета общего числа файлов ,откырытых в текущее время в системе  используем
    первое значение в выводе команды "cat /proc/sys/fs/file-nr"

       root@vagrant:/etc/sysctl.d# cat /proc/sys/fs/file-nr
       1472    0       9223372036854775807


6) Запустите любой долгоживущий процесс (не ls, который отработает мгновенно, а, например, sleep 1h) в отдельном неймспейсе процессов; 
   покажите, что ваш процесс работает под PID 1 через nsenter. Для простоты работайте в данном задании под root (sudo -i). 
   Под обычным пользователем требуются дополнительные опции (--map-root-user) и т.д.


7) Найдите информацию о том, что такое :(){ :|:& };:. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04
   (это важно, поведение в других ОС не проверялось). Некоторое время все будет "плохо", 
   после чего (минуты) – ОС должна стабилизироваться. 
   Вызов dmesg расскажет, какой механизм помог автоматической стабилизации. 
   Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?