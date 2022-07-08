Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"


1) Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?

Ответ:

        Linux:   ifconfig -a   ;   ip -с -br link
        Windows: ipconfig /all

2) Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?

Ответ:
  
      Протоколы   
      LLDP - протокол с отрытым стандартом.
      CDP  - прориетарный протокол CISCO.

      root@docker/~#  apt install lldpd
      root@docker/~#  systemctl enable lldpd && systemctl start lldpd
      root@docker/~#  lldpctl
      LLDP neighbors
   
      Interface: eth0
       ChassisID: sw-b-48 (local)
       SysName:   sw-b-48
       SysDescr:
        cisco WS-C2960-48TT-L running on
        Cisco IOS Software, C2960 Software (C2960-LANBASE-M)
        Copyright (c) 1986-2007 by Cisco Systems, Inc.
        Compiled Thu 19-Jul-07 20:06 by nachen
       MgmtIP:    172.16.25.48
       Caps:      Bridge(E)
       PortID:    FastEthernet0/4 (ifName)
       PortDescr: FastEthernet0/4

3) Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.

Ответ:
      
      VLAN технология.  
      Пакет vlan
      
      root@docker/~#  apt install vlan
      root@docker/~#  nano /etc/network/interfaces

      auto vlan 1200
      iface vlan1200 inet static
         adrress 172.16.0.1
         netmask 255.255.255.0
         vlan_raw_device eth0

      auto eth1.200
      iface eth1.200 inet static
         adrress 172.16.1.1
         netmask 255.255.255.0
         vlan_raw_device eth1

4) Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.

Ответ:

      Агрегирование каналов может быть реализовано двумя способами:

      а) Агрегирование по протоколу LACP    ( или PAgP -Port Aggregation Protocol  проприетарный протокол Cisco ).
      б) Ручная настройка - агрегирование нескольких физических интерфейсов для балансировки нагрузки между ними;
        
      LAG динамический  - ( в IOS  Cisco mode active )
      LAG статический   - ( в IOS Cisco mode on  )  

      root@docker/~#  apt install ifenslave
      root@docker/~#  nano /etc/network/interfaces
 
      auto bond0

      iface bond0 inet static
          address 10.31.1.5
          netmask 255.255.255.0
          network 10.31.1.0
          gateway 10.31.1.254
          bond-slaves eth0 eth2
          bond-mode active-backup
          bond-miimon 100
          bond-downdelay 200
          bond-updelay 200     
      

5) Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. 
   Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.

Ответ:

         В сеть с маской /29  входит 8 адресов . 
         В сети с маской /24 можно организовать 32 подсети /29.

         Примеры :
     
         192.168.0.0 - 192.168.0.7 ;  192.168.0.8 - 192.168.0.15 ; 

6) Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. 
   Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.

Ответ:

        Берем адреса из диапазона 100.64.0.0 - 100.127.255.255   mask 255.192.0.0  ( иначе  /10 )

        100.64.0.1 - 10.64.0.62 / 255.255.255.192 (иначе /26 )


7) Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?

Ответ:

-Проверка ARP таблицы

        Linux   :  root@docker/~#  ip neigh  
        Windows :  arp -a
    
-Полная очистка ARP таблицы на рабочей станции
         
        Linux   :  root@docker/~#  sudo ip neigp flush all
        Windows :  netsh interface ip delete arpcache

-Удалить выбранную пару "mac - ip адрес".

        arp -d 192.168.1.1   



8) Задание для самостоятельной отработки (необязательно к выполнению)
   8*. Установите эмулятор EVE-ng.
   Инструкция по установке - https://github.com/svmyasnikov/eve-ng
   Выполните задания на lldp, vlan, bonding в эмуляторе EVE-ng.



