1) Узнайте о sparse (разряженных) файлах.

Ответ:

2) Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

3) Сделайте vagrant destroy на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

Ответ: Готово

4) Используя fdisk, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.

Ответ:

    Имеем в распоряжении  три дисковых устройства

    root@vagrant:/home/vagrant# dmesg | grep sda
    [    6.824670] sd 2:0:0:0: [sda] 134217728 512-byte logical blocks: (68.7 GB/64.0 GiB)
    [    6.825085] sd 2:0:0:0: [sda] Write Protect is off
    [    6.831744] sd 2:0:0:0: [sda] Mode Sense: 00 3a 00 00
    [    6.832016] sd 2:0:0:0: [sda] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
    [    6.961958]  sda: sda1 sda2 sda3
    [    7.078495] sd 2:0:0:0: [sda] Attached SCSI disk
    [   50.515988] EXT4-fs (sda2): mounted filesystem with ordered data mode. Opts: (null)
 
    root@vagrant:/home/vagrant# dmesg | grep sdb
    [    7.203279] sd 3:0:0:0: [sdb] 5242880 512-byte logical blocks: (2.68 GB/2.50 GiB)
    [    7.221101] sd 3:0:0:0: [sdb] Write Protect is off
    [    7.229998] sd 3:0:0:0: [sdb] Mode Sense: 00 3a 00 00
    [    7.239454] sd 3:0:0:0: [sdb] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
    [    7.927712] sd 3:0:0:0: [sdb] Attached SCSI disk

    root@vagrant:/home/vagrant# dmesg | grep sdc
    [    7.980016] sd 4:0:0:0: [sdc] 5242880 512-byte logical blocks: (2.68 GB/2.50 GiB)
    [    8.000156] sd 4:0:0:0: [sdc] Write Protect is off
    [    8.009820] sd 4:0:0:0: [sdc] Mode Sense: 00 3a 00 00
    [    8.009872] sd 4:0:0:0: [sdc] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
    [    8.321314] sd 4:0:0:0: [sdc] Attached SCSI disk

Создаем логический диск на втором дисковом устройстве:
     
    root@vagrant:/home/vagrant# fdisk /dev/sdb
    
    Command (m for help): n
    Partition type
       p   primary (0 primary, 0 extended, 4 free)
       e   extended (container for logical partitions)
    Select (default p): p
    Partition number (1-4, default 1): 1
    First sector (2048-5242879, default 2048):
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G
    
    Created a new partition 1 of type 'Linux' and of size 2 GiB.
    
    Command (m for help): w
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.

Проверяем наличие раздела 

    root@vagrant:/home/vagrant# fdisk -l /dev/sdb
    Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x555bdceb
    
    Device     Boot Start     End Sectors Size Id Type
    /dev/sdb1        2048 4196351 4194304   2G 83 Linux
     root@vagrant:/home/vagrant# 


5) Используя sfdisk, перенесите данную таблицу разделов на второй диск.

Ответ:

Создаем аналогичный по размеру раздел на втором устройстве /dev/sdc

    root@vagrant:/home/vagrant# fdisk  /dev/sdc

    Welcome to fdisk (util-linux 2.34).
    Changes will remain in memory only, until you decide to write them.
    Be careful before using the write command.
    
    Device does not contain a recognized partition table.
    Created a new DOS disklabel with disk identifier 0x1acb580f.
    
    Command (m for help): n
    Partition type
       p   primary (0 primary, 0 extended, 4 free)
       e   extended (container for logical partitions)
    Select (default p): p
    Partition number (1-4, default 1):
    First sector (2048-5242879, default 2048):
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G
    
    Created a new partition 1 of type 'Linux' and of size 2 GiB.
    
    Command (m for help): w
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.

Копируем целиком первого дисковое устройство /dev/sbd на второе /dev/sdc :

    root@vagrant:/home/vagrant# sfdisk -d  /dev/sdb /dev/sdc

Проверяем наличие логического раздела Linux dev/sdc1 на втором устройстве dev/sdc 
    root@vagrant:/home/vagrant# fdisk -l /dev/sdc
    Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x1acb580f
    
    Device     Boot Start     End Sectors Size Id Type
    /dev/sdc1        2048 4196351 4194304   2G 83 Linux

6) Соберите mdadm RAID1 на паре разделов 2 Гб.

Ответ:





7) Соберите mdadm RAID0 на второй паре маленьких разделов.

Ответ:

8) Создайте 2 независимых PV на получившихся md-устройствах.

Ответ:

9) Создайте общую volume-group на этих двух PV.

Ответ:

10) Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

Ответ:

11) Создайте mkfs.ext4 ФС на получившемся LV.

Ответ:

12) Смонтируйте этот раздел в любую директорию, например, /tmp/new.

Ответ:

13) Поместите туда тестовый файл, например wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz.

Ответ:

14) Прикрепите вывод lsblk.

Ответ:

15) Протестируйте целостность файла:

         root@vagrant:~# gzip -t /tmp/new/test.gz
         root@vagrant:~# echo $?
          0
Ответ:


16) Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

Ответ:

17) Сделайте --fail на устройство в вашем RAID1 md.

Ответ:

18) Подтвердите выводом dmesg, что RAID1 работает в деградированном состоянии.

Ответ:

19) Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

         root@vagrant:~# gzip -t /tmp/new/test.gz
         root@vagrant:~# echo $?
         0

Ответ:

20) Погасите тестовый хост, vagrant destroy.

Ответ: Готово.