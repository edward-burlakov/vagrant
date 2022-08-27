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

    root@docker:/home/vagrant# hostname
    docker
    root@docker:/home/vagrant#


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

 #### Развертываем 2 виртуальных сервера Ubuntu с помощью конфигурационного файла Vagrantfile/ 

 <https://github.com/edward-burlakov/vagrant/blob/main/Vagrantfile>

  
 #### Запускаем обе виртуальных сервера ansible и docker


       C:\Users\bes\PycharmProjects\Netology_Lessons\vagrant>vagrant up
       Bringing machine 'ansible.netology' up with 'virtualbox' provider...
       Bringing machine 'docker.netology' up with 'virtualbox' provider...
       ==> ansible.netology: Importing base box 'bento/ubuntu-20.04'...
       ==> ansible.netology: Matching MAC address for NAT networking...
       ==> ansible.netology: Checking if box 'bento/ubuntu-20.04' version '202206.03.0' is up to date...
       ==> ansible.netology: Setting the name of the VM: ansible.netology
       ==> ansible.netology: Clearing any previously set network interfaces...
       ==> ansible.netology: Preparing network interfaces based on configuration...
           ansible.netology: Adapter 1: nat
           ansible.netology: Adapter 2: hostonly
       ==> ansible.netology: Forwarding ports...
           ansible.netology: 22 (guest) => 2222 (host) (adapter 1)
       ==> ansible.netology: Running 'pre-boot' VM customizations...
       ==> ansible.netology: Booting VM...
       ==> ansible.netology: Waiting for machine to boot. This may take a few minutes...
           ansible.netology: SSH address: 127.0.0.1:2222
           ansible.netology: SSH username: vagrant
           ansible.netology: SSH auth method: private key
           ansible.netology: Warning: Connection reset. Retrying...
           ansible.netology: Warning: Connection aborted. Retrying...
           ansible.netology:
           ansible.netology: Vagrant insecure key detected. Vagrant will automatically replace
           ansible.netology: this with a newly generated keypair for better security.
           ansible.netology:
           ansible.netology: Inserting generated public key within guest...
           ansible.netology: Removing insecure key from the guest if it's present...
           ansible.netology: Key inserted! Disconnecting and reconnecting using new SSH key...
       ==> ansible.netology: Machine booted and ready!
       ==> ansible.netology: Checking for guest additions in VM...
       ==> ansible.netology: Setting hostname...
       ==> ansible.netology: Configuring and enabling network interfaces...
       ==> ansible.netology: Mounting shared folders...
           ansible.netology: /vagrant => C:/Users/bes/PycharmProjects/Netology_Lessons/vagrant
       ==> docker.netology: Importing base box 'bento/ubuntu-20.04'...
       ==> docker.netology: Matching MAC address for NAT networking...
       ==> docker.netology: Checking if box 'bento/ubuntu-20.04' version '202206.03.0' is up to date...
       ==> docker.netology: There was a problem while downloading the metadata for your box
       ==> docker.netology: to check for updates. This is not an error, since it is usually due
       ==> docker.netology: to temporary network problems. This is just a warning. The problem
       ==> docker.netology: encountered was:
       ==> docker.netology:
       ==> docker.netology: The requested URL returned error: 404
       ==> docker.netology:
       ==> docker.netology: If you want to check for box updates, verify your network connection
       ==> docker.netology: is valid and try again.
       ==> docker.netology: Setting the name of the VM: docker.netology
       ==> docker.netology: Fixed port collision for 22 => 2222. Now on port 2200.
       ==> docker.netology: Clearing any previously set network interfaces...
       ==> docker.netology: Preparing network interfaces based on configuration...
           docker.netology: Adapter 1: nat
           docker.netology: Adapter 2: hostonly
       ==> docker.netology: Forwarding ports...
           docker.netology: 22 (guest) => 2200 (host) (adapter 1)
       ==> docker.netology: Running 'pre-boot' VM customizations...
       ==> docker.netology: Booting VM...
       ==> docker.netology: Waiting for machine to boot. This may take a few minutes...
           docker.netology: SSH address: 127.0.0.1:2200
           docker.netology: SSH username: vagrant
           docker.netology: SSH auth method: private key
           docker.netology: Warning: Connection reset. Retrying...
           docker.netology: Warning: Connection aborted. Retrying...
           docker.netology:
           docker.netology: Vagrant insecure key detected. Vagrant will automatically replace
           docker.netology: this with a newly generated keypair for better security.
           docker.netology:
           docker.netology: Inserting generated public key within guest...
           docker.netology: Removing insecure key from the guest if it's present...
           docker.netology: Key inserted! Disconnecting and reconnecting using new SSH key...
       ==> docker.netology: Machine booted and ready!
       ==> docker.netology: Checking for guest additions in VM...
       ==> docker.netology: Setting hostname...
       ==> docker.netology: Configuring and enabling network interfaces...
       ==> docker.netology: Mounting shared folders...
           docker.netology: /vagrant => C:/Users/bes/PycharmProjects/Netology_Lessons/vagrant
       C:\Users\med1094\PycharmProjects\Vagrant>

===

####   Входим в виртуалки. Проверяем версии ОС серверов: 
     
    Ansible : 
              
        root@ansible:/home/vagrant# cat /etc/*release | grep VERSION
        VERSION="20.04.4 LTS (Focal Fossa)"
        VERSION_ID="20.04"
        VERSION_CODENAME=focal
        root@ansible:/home/vagrant#

    Docker :

        root@docker:/home/vagrant# cat /etc/*release | grep VERSION
        VERSION="20.04.4 LTS (Focal Fossa)"
        VERSION_ID="20.04"
        VERSION_CODENAME=focal
        root@docker:/home/vagrant#

####  Проверяем статус интерфейсов обоих серверов
      
    Ansible :

        root@ansible:/home/vagrant# hostname -f
        ansible.netology
        root@ansible:/home/vagrant#

        root@ansible:/home/vagrant# ip a | grep inet | grep 192
          inet 192.168.192.11/24 brd 192.168.192.255 scope global eth1
        root@ansible:/home/vagrant#

    Docker :

        root@docker:/home/vagrant# hostname -f
        docker.netology
        root@docker:/home/vagrant#

        root@docker:/home/vagrant# ip a | grep inet | grep 192
          inet 192.168.192.12/24 brd 192.168.192.255 scope global eth1
        root@docker:/home/vagrant#

#### Устанавливаем Ansible на виртуалке ansible.netology.

        root@ansible:/home/vagrant# apt update
        root@ansible:/home/vagrant# apt install ansible

### Правим файл конфигурации

        root@ansible:/etc/ansible# cat /etc/ansible/hosts

        [servers]
        docker  ansible_host=192.168.192.12
        
        [all:vars]
        ansible_python_interpreter=/usr/bin/python3

### Устанавливаем программу для заупска процесса ssh неинтерактивно

        root@ansible:/etc/ansible# apt install sshpass

### Проверяем подключенние к сервер  docker.netology  по паролю

        root@ansible:/etc/ansible# ansible all -m ping -u vagrant --ask-pass
        SSH password:
        docker | SUCCESS => {
            "changed": false,
            "ping": "pong"
        }
        root@ansible:/etc/ansible#

