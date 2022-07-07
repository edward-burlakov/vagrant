1) Узнайте о sparse (разряженных) файлах.

Ответ:

Разрежённый файл (англ. sparse file) — файл, в котором последовательности нулевых байтов[1] 
заменены на информацию об этих последовательностях (список дыр).
Дыра (англ. hole) — последовательность нулевых байт внутри файла, не записанная на диск. 
Информация о дырах (смещение от начала файла в байтах и количество байт) хранится в метаданных файловой системы.

ПРоверяем размер каталога /root

      root@vagrant:~# du -c -s -h /root
      56K     /root
      56K     total

Проверяем свободное место на корневом разделе до и после удаления

      root@vagrant:~# df /root
      Filesystem                        1K-blocks    Used Available Use% Mounted on
      /dev/mapper/ubuntu--vg-ubuntu--lv  32118592 3858784  26605232  13% /


Создаем разреженный файл  размером 200 Gb

        root@vagrant:~# truncate -s200G ./sparse-file
        root@vagrant:~# ls -la
        total 36
        drwx------  5 root root         4096 Jul  6 12:58 .
        drwxr-xr-x 19 root root         4096 Jun  7 11:49 ..
        -rw-------  1 root root          713 Jul  5 17:12 .bash_history
        -rw-r--r--  1 root root         3106 Dec  5  2019 .bashrc
        drwxr-xr-x  3 root root         4096 Jul  6 01:15 .local
        -rw-r--r--  1 root root          161 Dec  5  2019 .profile
        drwx------  3 root root         4096 Jun  7 11:50 snap
        -rw-r--r--  1 root root 214748364800 Jul  6 12:58 sparse-file
        drwx------  2 root root         4096 Jun  7 11:50 .ssh
        -rw-r--r--  1 root root          165 Jul  6 01:16 .wget-hsts
        root@vagrant:~# du -c -s -h /root
        56K     /root
        56K     total


Проверяем размер каталога /root - он не поменялся .

      root@vagrant:~# du -c -s -h /root
      56K     /root
      56K     total

Проверяем свободное место - оно не поменялось.

      root@vagrant:~# df /root
      Filesystem                        1K-blocks    Used Available Use% Mounted on
      /dev/mapper/ubuntu--vg-ubuntu--lv  32118592 3858784  26605232  13% /
  

2) Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

Нет, поскольку это лишь ссылки на один файловый объект на конкретном логическом разделе.

Создаем хардлинк на файл:

       root@vagrant:~# root@vagrant:~# ln testfile linkfile
       
       root@vagrant:~# root@vagrant:~# ls -la
       drwxr-xr-x  3 root root         4096 Jul  6 01:15 .local
       -rw-r--r--  1 root root          161 Dec  5  2019 .profile
       drwx------  3 root root         4096 Jun  7 11:50 snap
       -rw-r--r--  1 root root 214748364800 Jul  6 13:00 sparse-file
       drwx------  2 root root         4096 Jun  7 11:50 .ssh
       -rw-r--r--  2 root root            0 Jul  6 13:46 testfile
       -rw-r--r--  1 root root          165 Jul  6 01:16 .wget-hsts

Права доступа на оба хардлинка совпадают

        root@vagrant:~#  stat testfile ; stat linkfile
        File: testfile
        Size: 0               Blocks: 0          IO Block: 4096   regular empty file
        Device: fd00h/64768d    Inode: 1179744     Links: 2
        Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
        Access: 2022-07-06 13:46:50.114624803 +0000
        Modify: 2022-07-06 13:46:50.114624803 +0000
        Change: 2022-07-06 13:47:14.762942788 +0000
        Birth: -

        File: linkfile
        Size: 0               Blocks: 0          IO Block: 4096   regular empty file
        Device: fd00h/64768d    Inode: 1179744     Links: 2
        Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
        Access: 2022-07-06 13:46:50.114624803 +0000
        Modify: 2022-07-06 13:46:50.114624803 +0000
        Change: 2022-07-06 13:47:14.762942788 +0000
        Birth: -

Меняем права доступа на файл testfile  - права доступа на linkfile сменились аналогично.

        root@vagrant:~# chmod 770 testfile
        root@vagrant:~# stat testfile ; stat linkfile
        File: testfile
        Size: 0               Blocks: 0          IO Block: 4096   regular empty file
        Device: fd00h/64768d    Inode: 1179744     Links: 2
        Access: (0770/-rwxrwx---)  Uid: (    0/    root)   Gid: (    0/    root)
        Access: 2022-07-06 13:46:50.114624803 +0000
        Modify: 2022-07-06 13:46:50.114624803 +0000
        Change: 2022-07-06 13:48:27.711398795 +0000
        Birth: -

         File: linkfile
        Size: 0               Blocks: 0          IO Block: 4096   regular empty file
        Device: fd00h/64768d    Inode: 1179744     Links: 2
        Access: (0770/-rwxrwx---)  Uid: (    0/    root)   Gid: (    0/    root)
        Access: 2022-07-06 13:46:50.114624803 +0000
        Modify: 2022-07-06 13:46:50.114624803 +0000
        Change: 2022-07-06 13:48:27.711398795 +0000
        Birth: -

Сменив владельца на один из хардлинков, мы автоматически меняем и на второй хардлинк.       

        root@vagrant:~# chown vagrant testfile
        root@vagrant:~# ls -la | grep vagrant
        -rwxrwx---  2 vagrant root            0 Jul  6 13:46 linkfile
        -rwxrwx---  2 vagrant root            0 Jul  6 13:46 testfile

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

    root@vagrant:~# lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    loop0                       7:0    0 67.2M  1 loop /snap/lxd/21835
    loop1                       7:1    0 61.9M  1 loop /snap/core20/1328
    loop2                       7:2    0 43.6M  1 loop /snap/snapd/14978
    loop3                       7:3    0 61.9M  1 loop /snap/core20/1518
    loop4                       7:4    0   47M  1 loop /snap/snapd/16292
    loop5                       7:5    0 67.8M  1 loop /snap/lxd/22753
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0  1.5G  0 part /boot
    └─sda3                      8:3    0 62.5G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm  /
    sdb                         8:16   0  2.5G  0 disk
    └─sdb1                      8:17   0    2G  0 part 
    sdc                         8:32   0  2.5G  0 disk
    └─sdc1                      8:33   0    2G  0 part 

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

Копируем таблицу разделов первого дискового устройства /dev/sdb на втором /dev/sdc :

    root@vagrant:~# sfdisk --dump /dev/sdb | sfdisk --force /dev/sdc
    Checking that no-one is using this disk right now ... OK

    Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x555bdceb

    Old situation:

    >>> Script header accepted.
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Created a new DOS disklabel with disk identifier 0x555bdceb.
    /dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
    Partition #1 contains a ext2 signature.
    /dev/sdc2: Done.

    New situation:
    Disklabel type: dos
    Disk identifier: 0x555bdceb

    Device     Boot Start     End Sectors Size Id Type
    /dev/sdc1        2048 4196351 4194304   2G 83 Linux

    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.

Проверяем состояние дискового массива  dev/sdс . На нем появился аналогичный Linux раздел /dev/sdc1 .

    root@vagrant:~# fdisk -l /dev/sdc
    Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x555bdceb

    Device     Boot Start     End Sectors Size Id Type
    /dev/sdc1        2048 4196351 4194304   2G 83 Linux

6) Соберите mdadm RAID1 на паре разделов 2 Гб.

Ответ:
     
Для создания RAID1 массива /dev/md1 выполняем команду:

    root@vagrant:~# mdadm --create --verbose /dev/md1 -l 1 -n 2 /dev/sd{b1,c1}
    mdadm: /dev/sdb1 appears to contain an ext2fs file system
           size=2097152K  mtime=Wed Jul  6 14:59:25 2022
    mdadm: Note: this array has metadata at the start and
        may not be suitable as a boot device.  If you plan to
        store '/boot' on this device please ensure that
        your boot-loader understands md/v1.x metadata, or use
        --metadata=0.90
    mdadm: /dev/sdc1 appears to contain an ext2fs file system
           size=2097152K  mtime=Wed Jul  6 14:59:32 2022
    mdadm: size set to 2094080K
    Continue creating array? y
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md1 started.  


7) Соберите mdadm RAID0 на второй паре маленьких разделов.

Ответ:

1. Для создания RAID0 массива  сначала создаем два раздела  /dev/sdb2 и  /dev/sdc2  по 511Mb

        root@vagrant:~# fdisk  /dev/sdb
        Welcome to fdisk (util-linux 2.34).
        Changes will remain in memory only, until you decide to write them.
        Be careful before using the write command.

        Command (m for help): n
        Partition type
           p   primary (1 primary, 0 extended, 3 free)
           e   extended (container for logical partitions)
        Select (default p): p
        Partition number (2-4, default 2):
        First sector (4196352-5242879, default 4196352):
        Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879):
        
        Created a new partition 2 of type 'Linux' and of size 511 MiB.
        
        Command (m for help): w
        The partition table has been altered.
        Syncing disks.
        
2.      root@vagrant:~# fdisk  /dev/sdc
        
        Welcome to fdisk (util-linux 2.34).
        Changes will remain in memory only, until you decide to write them.
        Be careful before using the write command.
        
        
        Command (m for help): n
        Partition type
           p   primary (1 primary, 0 extended, 3 free)
           e   extended (container for logical partitions)
        Select (default p): p
        Partition number (2-4, default 2):
        First sector (4196352-5242879, default 4196352):
        Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879):
        
        Created a new partition 2 of type 'Linux' and of size 511 MiB.
        
        Command (m for help): w
        The partition table has been altered.
        Syncing disks.

3. Создаем stripe массив :

        root@vagrant:~# mdadm --create --verbose /dev/md2 -l 0 -n 2 /dev/sd{b2,c2}
        mdadm: chunk size defaults to 512K
        mdadm: Defaulting to version 1.2 metadata
        mdadm: array /dev/md2 started.

4. Результат:
   
       root@vagrant:~#  lsblk
       NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
       loop0                       7:0    0 67.2M  1 loop  /snap/lxd/21835
       loop1                       7:1    0 61.9M  1 loop  /snap/core20/1328
       loop2                       7:2    0 43.6M  1 loop  /snap/snapd/14978
       loop3                       7:3    0 61.9M  1 loop  /snap/core20/1518
       loop4                       7:4    0   47M  1 loop  /snap/snapd/16292
       loop5                       7:5    0 67.8M  1 loop  /snap/lxd/22753
       sda                         8:0    0   64G  0 disk
       ├─sda1                      8:1    0    1M  0 part
       ├─sda2                      8:2    0  1.5G  0 part  /boot
       └─sda3                      8:3    0 62.5G  0 part
         └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
       sdb                         8:16   0  2.5G  0 disk
       ├─sdb1                      8:17   0    2G  0 part
       │ └─md1                     9:1    0    2G  0 raid1
       └─sdb2                      8:18   0  511M  0 part
         └─md2                     9:2    0 1018M  0 raid0
       sdc                         8:32   0  2.5G  0 disk
       ├─sdc1                      8:33   0    2G  0 part
       │ └─md1                     9:1    0    2G  0 raid1
       └─sdc2                      8:34   0  511M  0 part
         └─md2                     9:2    0 1018M  0 raid0

5. Записываем состояние рейд-массивов в конфигурационный файл
      
       root@vagrant:/etc/mdadm# mdadm --detail --scan >>  /etc/mdadm/mdadm.conf

6. Результат

         root@vagrant:/etc/mdadm# cat  /etc/mdadm/mdadm.conf

         //     # mdadm.conf
         //     #
         //     # !NB! Run update-initramfs -u after updating this file.
         //     # !NB! This will ensure that initramfs has an uptodate copy.
         //     #
         //     # Please refer to mdadm.conf(5) for information about this file.
         //     #
         //     
         //     # by default (built-in), scan all partitions (/proc/partitions) and all
         //     # containers for MD superblocks. alternatively, specify devices to scan, using
         //     # wildcards if desired.
         //     #DEVICE partitions containers
         //     # automatically tag new arrays as belonging to the local system HOMEHOST <system>
         //     # instruct the monitoring daemon where to send mail alerts
                MAILADDR root
      
         //     # definitions of existing MD arrays
      
         //     # This configuration was auto-generated on Wed, 23 Feb 2022 08:54:41 +0000 by mkconf
                ARRAY /dev/md1 metadata=1.2 name=vagrant:1 UUID=cbcbc76b:db79ac9b:f16e45d0:80596d3b
                ARRAY /dev/md2 metadata=1.2 name=vagrant:2 UUID=80425bc1:54275659:7f7523b8:608d8a66
   
7. Обязательное требование,чтобы сгенерировать свежий образ initramfs вй каталоге  boot:  

       root@vagrant:/etc/mdadm# update-initramfs -u
       update-initramfs: Generating /boot/initrd.img-5.4.0-110-generic

8) Создайте 2 независимых PV на получившихся md-устройствах.

Ответ:

      root@vagrant:/etc/mdadm# pvcreate /dev/md1 /dev/md2
      Physical volume "/dev/md1" successfully created.
      Physical volume "/dev/md2" successfully created.

9) Создайте общую volume-group на этих двух PV.

Ответ:

Создаем группу:

      root@vagrant:/etc/mdadm# vgcreate vg00 /dev/md1 /dev/md2
      Volume group "vg00" successfully created

Активируем группу:

      root@vagrant:/etc/mdadm# vgchange -a y vg00
      0 logical volume(s) in volume group "vg00" now active

Проверяем созданную volume-группу :

      root@vagrant:/etc/mdadm# vgs
      VG        #PV #LV #SN Attr   VSize   VFree
      ubuntu-vg   1   1   0 wz--n- <62.50g 31.25g
      vg00        2   1   0 wz--n-  <2.99g  2.89g


10) Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

Ответ:

Создаем логический том с именем LogicalVolume размером 100Mb 
на физическом рейд-массиве RAID0, входящем в volume-группу vg00. 

      root@vagrant:~# lvcreate  -L100M -nLogicalVolume00 vg00 /dev/md2
      Logical volume "LogicalVolume00" created.

Проверяем созданную логическую группу:  

      root@vagrant:~# lvs 
      LV              VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
      ubuntu-lv       ubuntu-vg -wi-ao---- <31.25g                                                 
      LogicalVolume00 vg00      -wi-a----- 100.00m    

11) Создайте mkfs.ext4 ФС на получившемся LV.

Ответ:

Находим дескриптор, ссылающийся на логическую группу LogicalVolume00 

      root@vagrant:~# fdisk -l  | grep LogicalVolume00
      Disk /dev/mapper/vg00-LogicalVolume00: 100 MiB, 104857600 bytes, 204800 sectors

Используем его при форматировании ( или /dev/vg00/LogicalVolume00 ) :

      root@vagrant:~# mkfs.ext4 /dev/mapper/vg00-LogicalVolume00
      mke2fs 1.45.5 (07-Jan-2020)
      Creating filesystem with 25600 4k blocks and 25600 inodes
      
      Allocating group tables: done
      Writing inode tables: done
      Creating journal (1024 blocks): done
      Writing superblocks and filesystem accounting information: done


12) Смонтируйте этот раздел в любую директорию, например, /tmp/new.

Ответ:

      root@vagrant:~# mkdir /tmp/new
      root@vagrant:~# mount /dev/mapper/vg00-LogicalVolume00  /tmp/new           



13) Поместите туда тестовый файл, например wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz

Ответ:

      root@vagrant:/tmp# wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
      --2022-07-06 16:39:03--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
      Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
      Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
      HTTP request sent, awaiting response... 200 OK
      Length: 23815737 (23M) [application/octet-stream]
      Saving to: ‘/tmp/new/test.gz’

      /tmp/new/test.gz        100%[==============================>]  22.71M  2.84MB/s    in 9.7s

      2022-07-06 16:39:14 (2.34 MB/s) - ‘/tmp/new/test.gz’ saved [23815737/23815737]

14) Прикрепите вывод lsblk.

Ответ:

      root@vagrant:/dev/vg00# lsblk
      NAME                       MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
      loop0                        7:0    0 67.2M  1 loop  /snap/lxd/21835
      loop1                        7:1    0 43.6M  1 loop  /snap/snapd/14978
      loop2                        7:2    0 61.9M  1 loop  /snap/core20/1328
      loop3                        7:3    0 61.9M  1 loop  /snap/core20/1518
      loop4                        7:4    0   47M  1 loop  /snap/snapd/16292
      loop5                        7:5    0 67.8M  1 loop  /snap/lxd/22753
      sda                          8:0    0   64G  0 disk
      ├─sda1                       8:1    0    1M  0 part
      ├─sda2                       8:2    0  1.5G  0 part  /boot
      └─sda3                       8:3    0 62.5G  0 part
      └─ubuntu--vg-ubuntu--lv  253:0    0 31.3G  0 lvm   /
      sdb                          8:16   0  2.5G  0 disk
      ├─sdb1                       8:17   0    2G  0 part
      │ └─md1                      9:1    0    2G  0 raid1
      └─sdb2                       8:18   0  511M  0 part
      └─md2                      9:2    0 1018M  0 raid0
      └─vg00-LogicalVolume00 253:1    0  100M  0 lvm   /tmp/new
      sdc                          8:32   0  2.5G  0 disk
      ├─sdc1                       8:33   0    2G  0 part
      │ └─md1                      9:1    0    2G  0 raid1
      └─sdc2                       8:34   0  511M  0 part
      └─md2                      9:2    0 1018M  0 raid0
      └─vg00-LogicalVolume00 253:1    0  100M  0 lvm   /tmp/new



15) Протестируйте целостность файла:

Ответ:

Тестируем архив с помощью ключа -t

         root@vagrant:~# gzip -t /tmp/new/test.gz
         root@vagrant:~# echo $?
         0

Последняя команда возвращает статус предыдущей команды. 
Поскольку ошибок в архиве не обнаружено, возвращен 0.

16) Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

Ответ:
     
ПРоверяем состояние физических томов - PV

      root@vagrant:/dev/vg00# pvscan
      PV /dev/sda3   VG ubuntu-vg       lvm2 [<62.50 GiB / 31.25 GiB free]
      PV /dev/md1    VG vg00            lvm2 [<2.00 GiB / <2.00 GiB free]
      PV /dev/md2    VG vg00            lvm2 [1016.00 MiB / 916.00 MiB free]
      Total: 3 [65.48 GiB] / in use: 3 [65.48 GiB] / in no VG: 0 [0   ]

И логических томов - LV

      root@vagrant:/dev/vg00# lvscan
      ACTIVE            '/dev/ubuntu-vg/ubuntu-lv' [<31.25 GiB] inherit
      ACTIVE            '/dev/vg00/LogicalVolume00' [100.00 MiB] inherit

Выполняем команду:

       root@vagrant:/dev/vg00# pvmove /dev/md2
      /dev/md2: Moved: 12.00%
      /dev/md2: Moved: 100.00%

Результат:

     root@vagrant:/dev/vg00# lsblk
      NAME                       MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
      loop0                        7:0    0 67.2M  1 loop  /snap/lxd/21835
      loop1                        7:1    0 43.6M  1 loop  /snap/snapd/14978
      loop2                        7:2    0 61.9M  1 loop  /snap/core20/1328
      loop3                        7:3    0 61.9M  1 loop  /snap/core20/1518
      loop4                        7:4    0   47M  1 loop  /snap/snapd/16292
      loop5                        7:5    0 67.8M  1 loop  /snap/lxd/22753
      sda                          8:0    0   64G  0 disk
      ├─sda1                       8:1    0    1M  0 part
      ├─sda2                       8:2    0  1.5G  0 part  /boot
      └─sda3                       8:3    0 62.5G  0 part
      └─ubuntu--vg-ubuntu--lv  253:0    0 31.3G  0 lvm   /
      sdb                          8:16   0  2.5G  0 disk
      ├─sdb1                       8:17   0    2G  0 part
      │ └─md1                      9:1    0    2G  0 raid1
      │   └─vg00-LogicalVolume00 253:1    0  100M  0 lvm   /tmp/new
      └─sdb2                       8:18   0  511M  0 part
      └─md2                      9:2    0 1018M  0 raid0
      sdc                          8:32   0  2.5G  0 disk
      ├─sdc1                       8:33   0    2G  0 part
      │ └─md1                      9:1    0    2G  0 raid1
      │   └─vg00-LogicalVolume00 253:1    0  100M  0 lvm   /tmp/new
      └─sdc2                       8:34   0  511M  0 part
      └─md2                      9:2    0 1018M  0 raid0



17) Сделайте --fail на устройство в вашем RAID1 md.

Ответ:

      root@vagrant:/dev/vg00# mdadm /dev/md1 --fail /dev/sdb1
      mdadm: set /dev/sdb1 faulty in /dev/md1

Смотрим детализированный статус RAID массива: /dev/sdb1 - диск вышел из строя.

      root@vagrant:/dev/vg00# mdadm -D -t /dev/md1
      /dev/md1:
      Version : 1.2
      Creation Time : Thu Jul  7 04:04:45 2022
      Raid Level : raid1
      Array Size : 2094080 (2045.00 MiB 2144.34 MB)
      Used Dev Size : 2094080 (2045.00 MiB 2144.34 MB)
      Raid Devices : 2
      Total Devices : 2
      Persistence : Superblock is persistent
      
             Update Time : Thu Jul  7 05:16:31 2022
                   State : clean, degraded
          Active Devices : 1
      Working Devices : 1
      Failed Devices : 1
      Spare Devices : 0
      
      Consistency Policy : resync
      
                    Name : vagrant:1  (local to host vagrant)
                    UUID : 96522feb:cc97852c:2cc89d3d:7c39bcb7
                  Events : 19
      
      Number   Major   Minor   RaidDevice State
      -       0        0        0      removed
      1       8       33        1      active sync   /dev/sdc1
      0       8       17        -      faulty   /dev/sdb1

18) Подтвердите выводом dmesg, что RAID1 работает в деградированном состоянии.

Ответ:

      root@vagrant:/dev/vg00# dmesg |grep md1
      [  714.193953] md/raid1:md1: not clean -- starting background reconstruction
      [  714.193954] md/raid1:md1: active with 2 out of 2 mirrors
      [  714.193965] md1: detected capacity change from 0 to 2144337920
      [  714.194604] md: resync of RAID array md1
      [  724.427271] md: md1: resync done.
      [ 5019.030517] md/raid1:md1: Disk failure on sdb1, disabling device.
      md/raid1:md1: Operation continuing on 1 devices.


19) Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

        root@vagrant:~# gzip -t /tmp/new/test.gz
        root@vagrant:~# echo $?
        0

Ответ:  Состояние  0 .


20) Погасите тестовый хост, vagrant destroy.

Ответ:  Готово.