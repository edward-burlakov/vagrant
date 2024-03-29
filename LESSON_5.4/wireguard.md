## Руководство по настройке  WIREGUARD VPN-клиента на рабочей станции  Ubuntu.
## Бесплатная версия ограничена трафиком 300 Мб в сутки.
## Внимание!  Поднятие VPN-клиента  разрывает ssh сессию с Ubuntu-рабочей станцией, поднятую через NAT.
## Выполняйте все манипуляции только  c  ssh-клиента внутри той же локальной сети, что и рабочая станция Ubuntu !!!
### Основано  на оригинале  https://tokmakov.msk.ru/blog/item/535 . Muchas gracias автору.

---
### 1) Устанавливаем на машине с Ubuntu  пакет wireguard .
    Если другая ОС -  то пользуемся ссылкой https://www.wireguard.com/install/

    root@docker:~$ sudo apt install wireguard

---
### 2) Заходим на сайт https://securitykiss.com/download.html#clients .

    Из раздела "Choose tunnel location  and get client configuration"
    скачиваем настройки доступа к бесплатным VPN-серверам в виде файла .
    Например, для доступа к  VPN  серверу  Germany / Falkenstein   -  DE_Falkenstein.conf

---
### 3) Создаем файл настройки клиента Wireguard  /etc/wireguard/wg0.conf .

    Вставляем переменные, полученные из файла DE_Falkenstein.conf

    root@docker:~$ nano /etc/wireguard/wg0.conf

        [Interface]
        # ip-адрес клиента в виртуальной сети
        Address=10.240.99.61/12
        # приватный ключ  клиента
        PrivateKey=kE+JBOzIltMipWPUx6JxmL0RTp9qDPL3ZtnEKelCHV8=
        DNS=8.8.8.8

        [Peer]
        # публичный ключ сервера
        PublicKey=6HG6oOc5fOsmVq9CAfX0Y/nZCXMY048YZB+x5lzORGM=
        # ip-адрес и порт сервера
        Endpoint=49.12.98.129:7468
        # принимать пакеты с такими ip-адресами источника от сервера,
        # отправлять пакеты с такими ip-адресами назначения серверу
        AllowedIPs = 0.0.0.0/0::/0
        # поддерживать соединение в активном состоянии,
        # каждые 25 секунд отправлять пакет на сервер
        PersistentKeepalive = 25

https://securitykiss.com/download.html#clients

---
### 4)  Устанавливаем пакет для автоматической настройки DNS-сервера для туннеля

     root@docker:~$ sudo apt install resolvconf
---
### 5)  Правим файл  /etc/systemd/resolved.conf

    root@docker:~$ sudo nano /etc/systemd/resolved.conf

    [Resolve]
    DNS=8.8.8.8 8.8.4.4
    FallbackDNS=1.1.1.1 8.8.8.8 8.8.4.4
    Domains=mydomain.local
    LLMNR=yes
    #MulticastDNS=no
    #DNSSEC=no
    #DNSOverTLS=no
    Cache=no-negative
    #DNSStubListener=yes
    ReadEtcHosts=yes

---
### 6) Открываем и Правим файл /etc/nsswitch.conf

    Правим строку "hosts: files dns":

    root@docker:~# nano /etc/nsswitch.conf
    passwd:         files systemd
    group:          files systemd
    shadow:         files
    gshadow:        files

    hosts:          files resolve dns
---
### 7) Перезапускаем службу  systemd-resolved
 
    root@docker:~$ sudo systemctl stop   systemd-resolved &&  sudo systemctl start   systemd-resolved

---
### 8) Запускаем службу

    root@docker:~$ sudo systemctl start wg-quick@wg0.service

---
### 9) Добавляем службу в автозагрузку:

    root@docker:~$ sudo systemctl enable wg-quick@wg0.service
---
###  10)  Проверяем, что все работает
 
    Выполняем ping удаленного сервера (в файле конфигурации клиента поле AllowedIPs = 10.8.0.1):

    root@docker:~$ ping -c3 10.8.0.1
        PING 10.8.0.1 (10.8.0.1) 56(84) bytes of data.
        64 bytes from 10.8.0.1: icmp_seq=1 ttl=64 time=13.5 ms
        64 bytes from 10.8.0.1: icmp_seq=2 ttl=64 time=18.0 ms
        64 bytes from 10.8.0.1: icmp_seq=3 ttl=64 time=13.8 ms

        --- 10.8.0.1 ping statistics ---
        3 packets transmitted, 3 received, 0% packet loss, time 2003ms
        rtt min/avg/max/mdev = 13.510/15.073/17.960/2.043 ms
---
###  11)  Проверяем свой внешний IP  c помощью сервиса ifconfig.me. Он должен смениться.
 
        root@docker:~# curl ifconfig.me/ip
        49.12.98.129
        root@docker:~#
---
###  12)  Для остановки VPN-соединения используем
 
        root@docker:~# sudo systemctl stop wg-quick@wg0.service
---
###  13) Для исключения  сервиса VPN-соединения  из автозагрузки используем
        
        root@docker:~$ sudo systemctl disable wg-quick@wg0.service



