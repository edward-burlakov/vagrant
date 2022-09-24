## Домашнее задание к занятию "6.3. MySQL"

---
### Задача 1

    - Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.
    - Изучите бэкап БД и восстановитесь из него.
    - Перейдите в управляющую консоль mysql внутри контейнера.
    - Используя команду \h получите список управляющих команд.
    - Найдите команду для выдачи статуса БД и приведите в ответе из ее вывода версию сервера БД.
    - Подключитесь к восстановленной БД и получите список таблиц из этой БД.
    - Приведите в ответе количество записей с price > 300.
    - В следующих заданиях мы будем продолжать работу с данным контейнером.

---
### Ответ:

  #### 1) Развертываем контейнер с СУБД MySQL версии 8
     
    root@docker:/home/bes/#  docker run -d -it  --name mysql8  -e MYSQL_ROOT_PASSWORD=my-secret-pw  -p 3306:3306  -v $(pwd)/mysql:/var/lib/mysql   mysql:8.0 


  #### 2) Копируем БД из дампа на  докер-хост

    C:\scp test_dump.sql bes@192.168.1.16:/home/bes/mysql
    bes@192.168.1.16's password:
    test_dump.sql                                         100%  232KB   1.4MB/s   00:00


  #### 3) Входим в управляющую консоль mysql  с паролем  my-secret-pw  и создаем новую базу test_db.

    root@docker:/home/bes# docker exec -it 88d7769b4761   /bin/bash
    bash-4.4# mysql -u root -p 
    mysql> show databases;
        +--------------------+
        | Database           |
        +--------------------+
        | information_schema |
        | mysql              |
        | performance_schema |
        | sys                |
        +--------------------+
        4 rows in set (0.01 sec)
        
    mysql> CREATE DATABASE test_db;
    Query OK, 1 row affected (0.01 sec)
    mysql> 
      
  #### 3) Восстанавливаем БД test_db в контейнер  с mysql8.0, запуская процесс из домашнего каталога на докер-хосте

    root@docker:/home/bes/#  docker exec -i mysql8  sh -c 'exec mysql test_db -uroot -p"$MYSQL_ROOT_PASSWORD"' < $(pwd)/mysql/test_dump.sql
    mysql: [Warning] Using a password on the command line interface can be insecure.
    root@docker:/home/bes#

  #### 4) Сохраняем бэкап БД

    root@docker:/home/bes/#  docker exec mysql8  sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > /var/lib/mysql/all-databases.sql
    mysqldump: [Warning] Using a password on the command line interface can be insecure.
    root@docker:/home/bes#

  #### 5) Подключаемся к БД test_db через управляющую консоль  mysql  с паролем  my-secret-pw .

    root@docker:/home/bes# docker exec -it 88d7769b4761   /bin/bash
    bash-4.4# mysql -u root -p test_db
         
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 20
    Server version: 8.0.30 MySQL Community Server - GPL
    Copyright (c) 2000, 2022, Oracle and/or its affiliates.
     
    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.
     
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
       
    mysql>

  #### 5) Смотрим статус БД   

    mysql> \s
    --------------
    mysql  Ver 8.0.30 for Linux on x86_64 (MySQL Community Server - GPL)
    
    Connection id:          18
    Current database:       test_db
    Current user:           root@localhost
    SSL:                    Not in use
    Current pager:          stdout
    Using outfile:          ''
    Using delimiter:        ;
    Server version:         8.0.30 MySQL Community Server - GPL
    Protocol version:       10
    Connection:             Localhost via UNIX socket
    Server characterset:    utf8mb4
    Db     characterset:    utf8mb4
    Client characterset:    latin1
    Conn.  characterset:    latin1
    UNIX socket:            /var/run/mysqld/mysqld.sock
    Binary data as:         Hexadecimal
    Uptime:                 20 min 51 sec
    
    Threads: 2  Questions: 115  Slow queries: 0  Opens: 200  Flush tables: 3  Open tables: 117  Queries per second avg: 0.091
    --------------
  
  #### 6) Смотрим названия всех таблиц в конкретной базе данных test_db :

    mysql>  show tables;
    +-------------------+
    | Tables_in_test_db |
    +-------------------+
    | orders            |
    +-------------------+
    1 row in set (0.00 sec)

  #### 7) Выполняем выборку данных из  базы данных test_db :

    mysql> select * from orders where price>300 ;
    +----+----------------+-------+
    | id | title          | price |
    +----+----------------+-------+
    |  2 | My little pony |   500 |
    +----+----------------+-------+
    1 row in set (0.00 sec)
 


---
### Задача 2
Создайте пользователя test в БД c паролем test-pass, используя:

плагин авторизации mysql_native_password
срок истечения пароля - 180 дней
количество попыток авторизации - 3
максимальное количество запросов в час - 100
аттрибуты пользователя:
Фамилия "Pretty"
Имя "James"
Предоставьте привилегии пользователю test на операции SELECT базы test_db.

Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю test и приведите в ответе к задаче.

---
### Ответ:

1) Создаем пользователя  test c паролем test-pass

          mysql> CREATE USER 'test'@'localhost' IDENTIFIED BY 'test-pass';
          Query OK, 0 rows affected (0.22 sec)
          mysql>

2) Изменяем имя  и фамилию пользователя на указанные 

          mysql> ALTER USER 'test'@'localhost' ATTRIBUTE '{"fname":"James", "lname":"Pretty"}';
          Query OK, 0 rows affected (0.16 sec)
          mysql> 

3) Меняем параметры пользователя в интерактивном режиме 

          mysql> ALTER USER 'test'@'localhost' 
              -> IDENTIFIED BY 'test-pass' 
              -> WITH
              -> MAX_QUERIES_PER_HOUR 100
              -> PASSWORD EXPIRE INTERVAL 180 DAY
              -> FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 2;
          Query OK, 0 rows affected (0.12 sec)
          mysql>

4) Выдаем права пользователю test на выполнение операции SELECT на таблицу orders в БД test_db

          mysql> GRANT Select ON test_db.orders TO 'test'@'localhost';
          Query OK, 0 rows affected, 1 warning (0.14 sec)      
          mysql> 

5) Получаем информацию из системной таблицы INFORMATION_SCHEMA.USER_ATTRIBUTES

          mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES WHERE USER='test';
          +------+-----------+---------------------------------------+
          | USER | HOST      | ATTRIBUTE                             |
          +------+-----------+---------------------------------------+
          | test | localhost | {"fname": "James", "lname": "Pretty"} |
          +------+-----------+---------------------------------------+
          1 row in set (0.03 sec)


---
### Задача 3
Установите профилирование SET profiling = 1. Изучите вывод профилирования команд SHOW PROFILES;.
Исследуйте, какой engine используется в таблице БД test_db и приведите в ответе.
Измените engine и приведите время выполнения и запрос на изменения из профайлера в ответе:

на MyISAM
на InnoDB

----
### Ответ:

1) Устанавливаем профилирование 

        mysql> SET profiling = 1;
        Query OK, 0 rows affected, 1 warning (0.00 sec)

        mysql> SHOW PROFILES;
        +----------+------------+---------------------------------------------------------------------------------------------------------------------+
        | Query_ID | Duration   | Query                                                                                                               |
        +----------+------------+---------------------------------------------------------------------------------------------------------------------+
        |        1 | 0.00073425 | select DATABASE(), USER() limit 1                                                                                   |
        |        2 | 0.00023375 | select @@character_set_client, @@character_set_connection, @@character_set_server, @@character_set_database limit 1 |
        |        3 | 0.00012775 | mysql> SET profiling = 1                                                                                            |
        |        4 | 0.00011550 | Query OK, 0 rows affected, 1 warning (0.00 sec)
    
        SHOW PROFILES                                                      |
        +----------+------------+---------------------------------------------------------------------------------------------------------------------+
        4 rows in set, 1 warning (0.00 sec)
    
2) Выводим список доступных движков

         mysql> SHOW ENGINES\G ;
         *************************** 1. row ***************************
                Engine: FEDERATED
               Support: NO
              Comment: Federated MySQL storage engine
         Transactions: NULL
                  XA: NULL
           Savepoints: NULL
         *************************** 2. row ***************************
               Engine: MEMORY
              Support: YES
              Comment: Hash based, stored in memory, useful for temporary tables
         Transactions: NO
                   XA: NO
           Savepoints: NO
         *************************** 3. row ***************************
              Engine: InnoDB
             Support: DEFAULT
             Comment: Supports transactions, row-level locking, and foreign keys
         Transactions: YES
                   XA: YES
           Savepoints: YES
         *************************** 4. row ***************************
               Engine: PERFORMANCE_SCHEMA
              Support: YES
              Comment: Performance Schema
         Transactions: NO
                   XA: NO
           Savepoints: NO
         *************************** 5. row ***************************
              Engine: MyISAM
             Support: YES
             Comment: MyISAM storage engine
         Transactions: NO
                   XA: NO
           Savepoints: NO
         *************************** 6. row ***************************
               Engine: MRG_MYISAM
              Support: YES
              Comment: Collection of identical MyISAM tables
         Transactions: NO
                   XA: NO
           Savepoints: NO
         *************************** 7. row ***************************
               Engine: BLACKHOLE
              Support: YES
              Comment: /dev/null storage engine (anything you write to it disappears)
         Transactions: NO
                   XA: NO
           Savepoints: NO
         *************************** 8. row ***************************
               Engine: CSV
              Support: YES
              Comment: CSV storage engine
         Transactions: NO
                   XA: NO
           Savepoints: NO
         *************************** 9. row ***************************
               Engine: ARCHIVE
              Support: YES
              Comment: Archive storage engine
         Transactions: NO
                   XA: NO
           Savepoints: NO
         9 rows in set (0.00 sec)

    Видим, что текущий набор  использует  INNO_DB как дефолтовый движок хранения.
 
3)  Выполняем запросы на update
 
       mysql> UPDATE orders  SET price = 4000 WHERE id=2 ;
       Query OK, 1 row affected (0.00 sec)
       Rows matched: 1  Changed: 1  Warnings: 0

    
4) Меняем дефолтовый движок хранения на MyISAM и Конвертируем таблицу orders в базе данных  test_db 

       mysql> SET default_storage_engine=MyISAM;
       Query OK, 0 rows affected (0.00 sec)
  
       mysql> ALTER TABLE orders ENGINE = MyISAM;
       Query OK, 5 rows affected (0.02 sec)
       Records: 5  Duplicates: 0  Warnings: 0
 
5) Выполняем повторный запрос на update и смотрим оценку времени выполнения 

       mysql> UPDATE orders  SET price = 3000 WHERE id=2 ;
       Query OK, 1 row affected (0.00 sec)
       Rows matched: 1  Changed: 1  Warnings: 0

    
       mysql> SHOW PROFILES;
       +----------+------------+------------------------------------------------------------------------------------+
       | Query_ID | Duration   | Query                                                                              |
       +----------+------------+------------------------------------------------------------------------------------+
       |        1 | 0.00049600 | select * from orders                                                               |
       |        2 | 0.00050625 | SHOW ENGINES                                                                       |
       |        3 | 0.00051400 | SHOW ENGINES                                                                       |
       |        4 | 0.00007675 | | grep 'DEFAULT'                                                                   | 
       |        5 | 0.00232050 | UPDATE orders SET price = 4000 WHERE id=2                                          |
       |        6 | 0.00035850 | SET default_storage_engine=MyISAM                                                  |
       |        7 | 0.00010700 | mysql> SET default_storage_engine=MyISAM                                           |     
       |        8 | 0.02303750 | ALTER TABLE orders ENGINE = MyISAM                                                 |
       |        9 | 0.00161925 | UPDATE orders SET price = 3000 WHERE id=2                                          |                                                                                                                                                                                                                                                  
       |                                                                                                            |
       |                                                                                                            |
       +----------+------------+------------------------------------------------------------------------------------+
       9 rows in set, 1 warning (0.00 sec)
 
       Движок InnoDB показал результат для операции UPDATE   
           5 | 0.00232050 | UPDATE orders SET price = 4000 WHERE id=2 

       Движок MyISAM показал результат для операции UPDATE   
           9 | 0.00161925 | UPDATE orders SET price = 3000 WHERE id=2 
  
       Это говорит о том, быстродействие двух движков InnoDB и MyISAM примерно одинаковое. 
 
---
### Задача 4
Изучите файл my.cnf в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буфера с незакомиченными транзакциями 1 Мб
- Буфер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб
- 
 Приведите в ответе измененный файл my.cnf.

----
### Ответ:

bash-4.4# cat my.cnf
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/8.0/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
innodb_buffer_pool_size = 3G       # Default  value  134217728 (128Mb)
innodb_log_file_size = 100M        # Default  value  50331648   (48Mb)
innodb_flush_log_at_trx_commit=0   # Default value 1 . Не сбрасывать буфер  UPDATE-транзакций на диск . Скорость важнее сохранности данных.

# Compression of table enabled / The Compression applies to new-creating tables only .
# При создании новых таблиц c помощью оператора CREATE  необходимо использовать опцию ROW_FORMAT=COMPRESSED
innodb_file_per_table = ON     # Default value ON 

# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M

# Remove leading # to revert to previous value for default_authentication_plugin                               ,
# this will increase compatibility with older clients. For background, see:
# https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_de                               fault_authentication_plugin
# default-authentication-plugin=mysql_native_password
skip-host-cache
skip-name-resolve
datadir=/var/lib/mysql
socket=/var/run/mysqld/mysqld.sock
secure-file-priv=/var/lib/mysql-files
user=mysql

pid-file=/var/run/mysqld/mysqld.pid
[client]
socket=/var/run/mysqld/mysqld.sock

!includedir /etc/mysql/conf.d/


2) Смотрим текущие значения переменных

      mysql> show variables like "join_buffer_size%";
      +------------------+--------+
      | Variable_name    | Value  |
      +------------------+--------+
      | join_buffer_size | 262144 |
      +------------------+--------+
      1 row in set (0.00 sec)
      
      mysql> show global variables like 'join_buffer_size';
      +------------------+--------+
      | Variable_name    | Value  |
      +------------------+--------+
      | join_buffer_size | 262144 |
      +------------------+--------+
      1 row in set (0.01 sec)
