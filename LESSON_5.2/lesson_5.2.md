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

---

### Ответ:

####  1. Устанавливаем  VirtualBox на  Windows 10

![img.png](img.png)


####  2. Устанавливаем  Hashi-Corp Vagrant на  Windows 10

![img_1.png](img_1.png)

#### Устанавливаем виртуальную машину c ОС Ubuntu 20.04 в гипервизоре Oracle VirtualBox с помощью 
#### cледующего файла конфигурации Vagrantfile

     ISO = "bento/ubuntu-20.04"
     NET = "192.168.192."
     DOMAIN = ".netology"
     HOST_PREFIX = "ansible"
     INVENTORY_PATH = "../ansible/inventory"
     servers = [  
       {    
         :hostname => HOST_PREFIX + DOMAIN,    
         :ip => NET + "11",    
         :ssh_host => "20011",    
         :ssh_vm => "22",    
         :ram => 1024,    
         :core => 1  
       }
     ]
     
     Vagrant.configure(2) do |config|  
         config.vm.synced_folder ".", "/vagrant", disabled: false  
         servers.each do |machine|    
         config.vm.define machine[:hostname] do |node|      
         node.vm.box = ISO      
         node.vm.hostname = machine[:hostname]      
         node.vm.network "private_network", ip: machine[:ip]      
         node.vm.network :forwarded_port, guest: machine[:ssh_vm],host: machine[:ssh_host]      
                 node.vm.provider "virtualbox" do |vb|
                     vb.customize ["modifyvm", :id, "--memory", machine[:ram]]        
                     vb.customize ["modifyvm", :id, "--cpus", machine[:core]]        
                     vb.name = machine[:hostname]      
                 end
             end  
         end
     end

---

####  Проверяем конфигурацию сервера

    $ vagrant ssh ansible.netology

    root@ansible:~# hostname
    ansible.netology
    root@ansible:~#

    root@ansible:~# cat /etc/*release
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

    root@ansible:~# ip a | grep inet
        inet 127.0.0.1/8 scope host lo
        inet6 ::1/128 scope host
        inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
        inet6 fe80::a00:27ff:fea2:6bfd/64 scope link



#### Устанавливаем Ansible на сервере ansible.netology  c ОС Ubuntu 20.04, запущенном в  VirtualBox.

    root@ansible:~# sudo apt update
    root@ansible:~# apt-get update
    root@ansible:~# apt-get install ansible -y

---
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

---

### Ответ:

#### Развертываем  виртуальный сервер c Ansible на нашей рабочей станции Windows10 с помощью "Windows Subsystem for Linux"
#### Скачиваем и устанавливаем c Microsoft Store  образ Ubuntu 22.04.1 LTS и пакет Ansible.  
#### В качестве пользователя указываем  vagrant  c паролем vagrant

#### Задаем имя сервера  в файле  /etc/.wsl.conf и перезагружаем сервер
     ...
     [network]
     hostname = ansible.netology 
     ...

     root@EDWARD:/etc# shutdown -r

#### Проверяем имя и версию ОС сервера: 
     root@ansible:~# cat hostname
     ansible.netology
     
     root@ansible:~# cat /etc/*release | grep VERSION
     root@ansible.netology:/# cat /etc/*release | grep VERSION
     VERSION_ID="22.04"
     VERSION="22.04.1 LTS (Jammy Jellyfish)"
     VERSION_CODENAME=jammy
     root@ansible:~# 

#### Устанавливаем Ansible на виртуалке ansible.netology.     
     root@ansible:~# sudo apt update
     root@ansible:~# apt-get update
     root@ansible:~# apt-get install ansible -y

#### Проверяем результат

     root@ansible:~# ansible --version
     ansible 2.10.8
       config file = None
       configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
       ansible python module location = /usr/lib/python3/dist-packages/ansible
       executable location = /usr/bin/ansible
       python version = 3.10.4 (main, Jun 29 2022, 12:14:53) [GCC 11.2.0]
     root@ansible:~#

####

 #### с помощью следующего конфигурационного файла Vagrantfile : 

 <https://github.com/edward-burlakov/vagrant/blob/main/Vagrantfile>

  
 #### Запускаем обе виртуальный сервер docker.netology

       root@ansible:/~# vagrant up

       Bringing machine 'docker.netology' up with 'virtualbox' provider...
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

---

####   Входим в созданные виртуалки. Проверяем версии ОС серверов: 
     
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

####  Проверяем имена серверов и наличие сетевых интерфейсов на обоих серверах.
      
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



        root@ansible:/etc/ansible# ansible --version
        ansible 2.9.6
          config file = /etc/ansible/ansible.cfg
          configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
          ansible python module location = /usr/lib/python3/dist-packages/ansible
          executable location = /usr/bin/ansible
          python version = 3.8.10 (default, Mar 15 2022, 12:22:08) [GCC 9.4.0]
        root@ansible:/etc/ansible#

#### Создаем файл inventory - списка хостов

        root@ansible:/etc/ansible# cat /etc/ansible/inventory

        [nodes:children]
        manager
        
        [manager]
        docker.netology ansible_host=192.168.192.12 ansible_port=22 ansible_user=vagrant ansible_password=vagrant
        
        [all:vars]
        ansible_python_interpreter=/usr/bin/python3

#### Правим файл конфигурации ansible.cfg, указывая на созданный выше файл inventory

       [defaults]
       
       inventory=./inventory
       deprecation_warnings=
       Falsecommand_warnings=False
       ansible_port=22
       interpreter_python=/usr/bin/python3

#### Проверяем корректность конфигурации хостов, перечисленных в файле inventory

       root@ansible:/etc/ansible# ansible-inventory --list -y
       all:
         children:
           nodes:
             children:
               manager:
                 hosts:
                   docker.netology:
                     ansible_host: 192.168.192.12
                     ansible_password: vagrant
                     ansible_port: 22
                     ansible_python_interpreter: /usr/bin/python3
                     ansible_user: vagrant
           ungrouped: {}
       root@ansible:/etc/ansible#

#### Устанавливаем программу для запуска процесса ssh неинтерактивно

        root@ansible:/etc/ansible# apt install sshpass

#### Проверяем подключение к docker.netology с помощью иcполнения на удаленном сервере команды ping  

        root@ansible:/etc/ansible# ansible all -m ping 
        SSH password:
        docker | SUCCESS => {
            "changed": false,
            "ping": "pong"
        }
        root@ansible:/etc/ansible#

####  Создаем файл плейбука provision.yml в каталоге /etc/ansible

       ---  
         — hosts: nodes    
           become: yes    
           become_user: root    
           remote_user: vagrant    
         
           tasks:      
             — name: Create directory for ssh-keys        
               file: state=directory  mode=0700   dest=/root/.ssh/
       
             — name: Adding rsa-key in /root/.ssh/authorized_keys        
               copy: src=~/.ssh/id_rsa.pub dest=/root/.ssh/authorized_keys  owner=root mode=0600        
               ignore_errors: yes
       
             — name: Checking DNS        
               command: host -t A google.com

             — name: Installing tools        
               apt: >
                 package={{ item }}          
                 state=present
                 update_cache=yes        
               with_items:
                 — git          
                 — curl

             — name: Installing docker        
               shell: curl -fsSL get.docker.com -o get-docker.sh && chmod +x get-docker.sh && ./get-docker.sh      

             — name: Add the current user to docker group        
               user: name=vagrant append=yes groups=docker


####  Создаем логическую ссылку на файл inventory в HOME-каталоге пользователя vagrant

       root@ansible:/home/vagrant# ln -s /etc/ansible/inventory inventory
       root@ansible:/home/vagrant# ls -la | grep inventory
       lrwxrwxrwx 1 root    root      22 Aug 28 03:43 inventory -> /etc/ansible/inventory


####  Подключаем Ansible playbook к нашей Vagrant конфигурации - добавляем записи в файл Vagrantfile:

      INVENTORY_PATH = "$HOME/inventory"

      node.vm.provision "ansible" do |setup| 
        setup.inventory_path = INVENTORY_PATH 
        setup.playbook = "$HOME/provision.yml" 
        setup.become = true setup.extra_vars = { ansible_user: 'vagrant' }
      end

####  Удаляем и создаем сервер docker.netology заново
     vagrant destroy docker.netology  --force
     vagrant up docker.netology
























 1Help      2Save      3Mark      4Replac    5Copy      6Move      7Search    8Delete    9PullDn   10Quit
