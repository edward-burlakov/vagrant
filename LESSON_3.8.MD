Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"

1) Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP
   telnet route-views.routeviews.org
   Username: rviews
   show ip route x.x.x.x/32
   show bgp x.x.x.x/32

       route-views>show ip route 212.20.48.100

       Routing entry for 212.20.0.0/18, supernet
       Known via "bgp 6447", distance 20, metric 0
       Tag 2497, type external
       Last update from 202.232.0.2 7w0d ago
       Routing Descriptor Blocks:
       * 202.232.0.2, from 202.232.0.2, 7w0d ago
       Route metric is 0, traffic share count is 1
       AS Hops 2

       Route tag 2497
       MPLS label: none
       route-views>

       route-views>ping  hwinfo.org

       Type escape sequence to abort.
       Sending 5, 100-byte ICMP Echos to 162.255.119.150, timeout is 2 seconds: !!!!!
       Success rate is 100 percent (5/5), round-trip min/avg/max = 44/44/45 ms

       route-views>show bgp 162.255.119.150

       _BGP routing table entry for 162.255.119.0/24, version 2343588541
       Paths: (23 available, best #14, table default)
       Not advertised to any peer
       Refresh Epoch 1
       20912 3257 19551 19551 19551 19551 22612
       212.66.96.126 from 212.66.96.126 (212.66.96.126)
       Origin IGP, localpref 100, valid, external
       Community: 3257:4000 3257:8908 3257:50002 3257:50122 3257:51300 3257:51303 20912:65004
       path 7FE0FC1C0ED0 RPKI State not found
       rx pathid: 0, tx pathid: 0
       Refresh Epoch 1
       3333 1103 19551 22612
       193.0.0.56 from 193.0.0.56 (193.0.0.56)
       Origin IGP, localpref 100, valid, external
       path 7FE0B6EFC540 RPKI State not found
       rx pathid: 0, tx pathid: 0
       Refresh Epoch 1
       4901 6079 19551 22612
       ....
       ....
       ....
       Refresh Epoch 1
       1221 4637 6762 19551 22612
       203.62.252.83 from 203.62.252.83 (203.62.252.83)
       Origin IGP, localpref 100, valid, external
       path 7FE0E6D16AB0 RPKI State not found
       rx pathid: 0, tx pathid: 0
       Refresh Epoch 1
       3257 19551 19551 19551 19551 22612
       89.149.178.10 from 89.149.178.10 (213.200.83.26)
       Origin IGP, metric 10, localpref 100, valid, external
       Community: 3257:4000 3257:8908 3257:50002 3257:50122 3257:51300 3257:51303
       path 7FE0B60BE4B0 RPKI State not found
       rx pathid: 0, tx pathid: 0
       route-views>

2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.

Вариант 1:

Анализируем текущее состояние:

      root@vagrant:/home/vagrant# ip addr

      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
      valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host
      valid_lft forever preferred_lft forever
      2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
      link/ether 08:00:27:a2:6b:fd brd ff:ff:ff:ff:ff:ff
      inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
      valid_lft 58325sec preferred_lft 58325sec
      inet6 fe80::a00:27ff:fea2:6bfd/64 scope link
      valid_lft forever preferred_lft forever

Состояние маршрутов до изменения:

      root@vagrant:/home/vagrant# ip ro
      default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100
      10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
      10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100
      192.168.100.0/24 dev dummy0 proto kernel scope link src 192.168.100.1
      root@vagrant:/home/vagrant#


Создаем dummy0 интерфейс:

      root@vagrant:/home/vagrant# ip link add dummy0 type dummy

Проверяем список интерфейсов: 

      root@vagrant:/home/vagrant# ip addr

      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
      valid_lft forever preferred_lft forever
      inet6 ::1/128 scope host
      valid_lft forever preferred_lft forever
      2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
      link/ether 08:00:27:a2:6b:fd brd ff:ff:ff:ff:ff:ff
      inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
      valid_lft 58093sec preferred_lft 58093sec
      inet6 fe80::a00:27ff:fea2:6bfd/64 scope link
      valid_lft forever preferred_lft forever
      3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 1000
      link/ether e6:2b:c4:48:96:9a brd ff:ff:ff:ff:ff:ff
      root@vagrant:/home/vagrant#

Назначаем ip адрес созданному интерфейсу dummy0 :

      root@vagrant:~# ip addr add 192.168.100.1/24 dev dummy0

Поднимаем интерфейс dummy0 :
    
      root@vagrant:~# ip link set dummy0 up

Для постоянного существования интерфейса dummy0 создаем два файла со следующим содержимым:

      root@vagrant:~# cat /etc/systemd/network/10-dummy.netdev
      [NetDev]
      Name=dummy0
 
      root@vagrant:~# cat /etc/systemd/network/20-dummy.network
      [NetDev]
      Name=dummy0
      Kind=dummyroot@vagrant:/etc/systemd/network# cat 20-dummy0.network
      [Match]
      Name=dummy0

      [Network]
      Address=192.168.100.1/24
      Address=fe80::e42b:c4ff:fe48:969a/64



Вариант 2 :

      Начиная с версии Ubuntu 18.04 LTS и выше, 
      операционная система использует файлы netplan YAML для настройки сети — они находятся в каталоге /etc/netplan.
      Редактируем файлы системы netplan - централизованного управления сетевыми настройками 

        root@vagrant:~# cat /etc/netplan/00-installer-config.yaml
        # This is the network config written by 'subiquity'
        network:
            ethernets:
                eth0:
                    dhcp4: yes
                    nameservers:
                                addresses: [8.8.8.8, 192.168.48.1]
            version: 2

        root@vagrant:~# cat /etc/netplan/01-netcfg.yaml
        network:
            ethernets:
              dummy0:
                  dhcp4: no
                  addresses: [192.168.100.1/24]
           version: 2
      

Добавляем постоянный статический маршрут в  файл /etc/netplan/01-netcfg.yaml  через интерфейс dummy0 :

        root@vagrant:~# cat /etc/netplan/01-netcfg.yaml
        network:
            ethernets:
               dummy0:
               dhcp4: no
               addresses: [192.168.100.1/24]
               routes:
               - to: 192.168.205.0/24
                 via: 192.168.100.254
           version: 2

Смотрим результат:

     root@vagrant:~# ip ro
     default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100
     10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
     10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100
     192.168.100.0/24 dev dummy0 proto kernel scope link src 192.168.100.1
     192.168.205.0/24 via 192.168.100.254 dev dummy0 proto static


3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.

       root@vagrant:~# ss -tap
       State        Recv-Q     Send-Q    Local Address:Port      Peer Address:Port    Process
       LISTEN       0          4096      127.0.0.53%lo:domain    0.0.0.0:*            users:(("systemd-resolve",pid=815,fd=13))
       LISTEN       0          128       0.0.0.0:ssh             0.0.0.0:*            users:(("sshd",pid=884,fd=3))
       ESTAB        0          0         10.0.2.15:ssh           10.0.2.2:51671       users:(("sshd",pid=1247,fd=4),("sshd",pid=1193,fd=4))
       LISTEN       0          128       [::]:ssh                [::]:*               users:(("sshd",pid=884,fd=4))

       Здесь используются следующие протоколы:
         
       domain 53 - Первый открытый порт - Domain Name System port 53
       ssh 22 - Второй открытый порт - Служба удаленного доступа к консоли unix.

4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?

       root@vagrant:~# ss -uanp
       State      Recv-Q     Send-Q     Local Address:Port       Peer Address:Port     Process
       UNCONN     0          0          127.0.0.53%lo:domain     0.0.0.0:*             users:(("systemd-resolve",pid=815,fd=12))
       UNCONN     0          0          10.0.2.15%eth0:bootpc    0.0.0.0:*             users:(("systemd-network",pid=810,fd=17))
                                                 
       53- Первый открытый порт - Domain Name System port 53 - Используется процессом systemd-resolve
       DNS (англ. Domain Name System «система доменных имён») .

       68 - Второй открытый порт - BOOTP (от англ. bootstrap protocol)   - Используется процессом systemd-network
       Сетевой протокол, используемый для автоматического получения клиентом IP-адреса. Это обычно происходит во время загрузки компьютера.
       BOOTP определён в RFC 951.


5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали.

      ![Диаграмма L3 домашней сети](https://github.com/edward-burlakov/vagrant/blob/main/Home%20network.png "Home network")

Задание для самостоятельной отработки (необязательно к выполнению)

   6*. Установите Nginx, настройте в режиме балансировщика TCP или UDP.
   
   7*. Установите bird2, настройте динамический протокол маршрутизации RIP.
   
   8*. Установите Netbox, создайте несколько IP префиксов, используя curl проверьте работу API.