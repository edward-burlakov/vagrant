# Домашнее задание к занятию "5.2. Применение принципов IaaC в работе с виртуальными машинами"


## Задача 1
Опишите своими словами основные преимущества применения на практике IaaC паттернов.
Какой из принципов IaaC является основополагающим?

### Ответ:

        
        1) Методология CI/CD 
           - Ускоряет  выход минимально работоспособного программного продукта 
             в продакшен (сокращается time-to-market ). 
           - Использование методологии CI/CD позволяет командам разрабочиков часто вносить изменения в приложения 
             с надежным процессом поставки.
           - Повышает качество, позволяя отсеивать ошибки еще на этапе CI .   
           - Устраняет "дрейф конфигураций".  
          
        2) Основополагающим  принципом IaaC является создание условий для воспроизводимости окружения 
           и сохранения работоспособности программного продукта.

## Задача 2
Чем Ansible выгодно отличается от других систем управление конфигурациями?
Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

### Ответ:

        - Ansible проще в освоении. Язык плейбуков YAML максимально человекочитаем.
        - Использует, в отличие от других продуктов, сущеcтвущий "defacto" сервис sshd  
          и не требует установки PKI-окружения. 
        - Дополнительные модули можно докачать из официального репозитория налету.
        - Тысячи готовых плейбуков на портале Ansible Galaxy.
        - Легко вносить изменения в силу популярности PYTHON.
        - Есть графический интерфейс Ansible Tower, хотя и с багами.
        - Подробный ansible -h .
        - Можно использовать не только push-метод, но и pull.

        2) Более надежным является метод "pull", поскольку при использованиие метода "push"  
           нет гарантии, что вносимые изменения на целевом хосте применятся , 
           если он будет недоступен в момент исполнения  скрипта.   

## Задача 3
Установить на личный компьютер:
VirtualBox
Vagrant
Ansible
Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.

### Ответ:

#### VirtualBox на  Windows 10

![img.png](img.png)

---

#### Vagrant  на Windows 10

![img_1.png](img_1.png)

---
    $ vagrant ssh ...

    root@vagrant:/home/vagrant# cat /etc/*release
    DISTRIB_ID=Ubuntu
    DISTRIB_RELEASE=20.04
    DISTRIB_CODENAME=focal
    DISTRIB_DESCRIPTION="Ubuntu 20.04.4 LTS"
    NAME="Ubuntu"
    VERSION="20.04.4 LTS (Focal Fossa)"
    ID=ubuntu
    ID_LIKE=debian
    PRETTY_NAME="Ubuntu 20.04.4 LTS"
    VERSION_ID="20.04"
    HOME_URL="https://www.ubuntu.com/"
    SUPPORT_URL="https://help.ubuntu.com/"
    BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
    PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
    VERSION_CODENAME=focal
    UBUNTU_CODENAME=focal
    root@vagrant:/home/vagrant#


    root@vagrant:/home/vagrant# ip a | grep inet
        inet 127.0.0.1/8 scope host lo
        inet6 ::1/128 scope host
        inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
        inet6 fe80::a00:27ff:fea2:6bfd/64 scope link



#### Устанавливаем Ansible на экземпляре Ubuntu 20.04, запущенном в  VirtualBox c помощью Vagrant.

    Результат :

    root@vagrant:/home/vagrant# ansible --version
    ansible [core 2.12.8]
      config file = /etc/ansible/ansible.cfg
      configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
      ansible python module location = /usr/lib/python3/dist-packages/ansible
      ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
      executable location = /usr/bin/ansible
      python version = 3.8.10 (default, Mar 15 2022, 12:22:08) [GCC 9.4.0]
      jinja version = 2.10.1
      libyaml = True
    root@vagrant:/home/vagrant#

---

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.
Создать виртуальную машину.
Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды
docker ps


### Ответ:

===

 #### Развертываем виртуальную машину с помощью конфигурационного файла Vagrantfile/ 

        C:\Users\med1094\PycharmProjects\Vagrant>vagrant up
        Bringing machine 'server1.netology' up with 'virtualbox' provider...
        ==> server1.netology: Importing base box 'bento/ubuntu-20.04'...
        ==> server1.netology: Matching MAC address for NAT networking...
        ==> server1.netology: Checking if box 'bento/ubuntu-20.04' version '202206.03.0' is up to date...
        ==> server1.netology: There was a problem while downloading the metadata for your box
        ==> server1.netology: to check for updates. This is not an error, since it is usually due
        ==> server1.netology: to temporary network problems. This is just a warning. The problem
        ==> server1.netology: encountered was:
        ==> server1.netology:
        ==> server1.netology: Failed to connect to vagrantcloud.com port 443: Timed out
        ==> server1.netology:
        ==> server1.netology: If you want to check for box updates, verify your network connection
        ==> server1.netology: is valid and try again.
        ==> server1.netology: Setting the name of the VM: server1.netology
        ==> server1.netology: Clearing any previously set network interfaces...
        ==> server1.netology: Preparing network interfaces based on configuration...
        server1.netology: Adapter 1: nat
        server1.netology: Adapter 2: hostonly
        ==> server1.netology: Forwarding ports...
        server1.netology: 22 (guest) => 20011 (host) (adapter 1)
        ==> server1.netology: Running 'pre-boot' VM customizations...
        ==> server1.netology: Booting VM...
        ==> server1.netology: Waiting for machine to boot. This may take a few minutes...
        server1.netology: SSH address: 127.0.0.1:2222
        server1.netology: SSH username: vagrant
        server1.netology: SSH auth method: private key
        server1.netology: Warning: Connection reset. Retrying...
        server1.netology: Warning: Connection aborted. Retrying...
        server1.netology: Warning: Connection aborted. Retrying...
        server1.netology: Warning: Connection reset. Retrying...
        server1.netology:
        server1.netology: Vagrant insecure key detected. Vagrant will automatically replace
        server1.netology: this with a newly generated keypair for better security.
        server1.netology:
        server1.netology: Inserting generated public key within guest...
        server1.netology: Removing insecure key from the guest if it's present...
        server1.netology: Key inserted! Disconnecting and reconnecting using new SSH key...
        ==> server1.netology: Machine booted and ready!
        ==> server1.netology: Checking for guest additions in VM...
        ==> server1.netology: Setting hostname...
        ==> server1.netology: Configuring and enabling network interfaces...
        ==> server1.netology: Mounting shared folders...
        server1.netology: /vagrant => C:/Users/med1094/PycharmProjects/Vagrant
        C:\Users\med1094\PycharmProjects\Vagrant>

===

####   Входим в виртуалку / Проверяем версию виртуальной машины. 

        root@server1:/home/vagrant# cat /etc/*release
        DISTRIB_ID=Ubuntu
        DISTRIB_RELEASE=20.04
        DISTRIB_CODENAME=focal
        DISTRIB_DESCRIPTION="Ubuntu 20.04.4 LTS"
        NAME="Ubuntu"
        VERSION="20.04.4 LTS (Focal Fossa)"
        ID=ubuntu
        ID_LIKE=debian
        PRETTY_NAME="Ubuntu 20.04.4 LTS"
        VERSION_ID="20.04"
        HOME_URL="https://www.ubuntu.com/"
        SUPPORT_URL="https://help.ubuntu.com/"
        BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
        PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
        VERSION_CODENAME=focal
        UBUNTU_CODENAME=focal
        root@server1:/home/vagrant#

####  Проверяем статус интрерфейсов
 
        root@server1:/home/vagrant# ip a
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
        valid_lft forever preferred_lft forever
        2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 08:00:27:a2:6b:fd brd ff:ff:ff:ff:ff:ff
        inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
        valid_lft 86157sec preferred_lft 86157sec
        inet6 fe80::a00:27ff:fea2:6bfd/64 scope link
        valid_lft forever preferred_lft forever
        3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 08:00:27:51:eb:58 brd ff:ff:ff:ff:ff:ff
        inet 192.168.192.11/24 brd 192.168.192.255 scope global eth1
        valid_lft forever preferred_lft forever
        inet6 fe80::a00:27ff:fe51:eb58/64 scope link
        valid_lft forever preferred_lft forever

        root@server1:/home/vagrant# ip a | grep inet | grep 192
        inet 192.168.192.11/24 brd 192.168.192.255 scope global eth1clear

###   Смотрим активные соединения
        root@server1:/home/vagrant#  sudo lsof -nP -i
        COMMAND    PID            USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
        systemd-n  607 systemd-network   20u  IPv4  20289      0t0  UDP 10.0.2.15:68
        systemd-r  609 systemd-resolve   12u  IPv4  20308      0t0  UDP 127.0.0.53:53
        systemd-r  609 systemd-resolve   13u  IPv4  20309      0t0  TCP 127.0.0.53:53 (LISTEN)
        sshd       819            root    3u  IPv4  24052      0t0  TCP *:22 (LISTEN)
        sshd       819            root    4u  IPv6  24063      0t0  TCP *:22 (LISTEN)
        sshd      1060            root    4u  IPv4  26463      0t0  TCP 10.0.2.15:22->10.0.2.2:65462 (ESTABLISHED)
        sshd      1113         vagrant    4u  IPv4  26463      0t0  TCP 10.0.2.15:22->10.0.2.2:65462 (ESTABLISHED)
        

        root@server1:/home/vagrant# hostname -f

        root@server1:/home/vagrant# free
        total        used        free      shared  buff/cache   available
        Mem:        2030968      149588      954020         988      927360     1728292
        Swap:       1999868           0     1999868

### Выключаем сервер
        C:\Users\med1094\PycharmProjects\Vagrant>vagrant halt
        ==> server1.netology: Attempting graceful shutdown of VM...

### Проверяем статус сервера

        C:\Users\med1094\PycharmProjects\Vagrant>vagrant status
        Current machine states:

        server1.netology          poweroff (virtualbox)

        The VM is powered off. To restart the VM, simply run `vagrant up`

### Удаляем выбранный экземпляр сервера

        C:\Users\med1094\PycharmProjects\Vagrant>vagrant destroy
        server1.netology: Are you sure you want to destroy the 'server1.netology' VM? [y/N] y
        ==> server1.netology: Destroying VM and associated drives...

### Проверяем статус сервера

        C:\Users\med1094\PycharmProjects\Vagrant>vagrant status
        Current machine states:

        server1.netology          not created (virtualbox)
