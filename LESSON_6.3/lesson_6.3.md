## Домашнее задание к занятию "6.3. MySQL"

---
### Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.
Изучите бэкап БД и восстановитесь из него.
Перейдите в управляющую консоль mysql внутри контейнера.
Используя команду \h получите список управляющих команд.
Найдите команду для выдачи статуса БД и приведите в ответе из ее вывода версию сервера БД.
Подключитесь к восстановленной БД и получите список таблиц из этой БД.
Приведите в ответе количество записей с price > 300.
В следующих заданиях мы будем продолжать работу с данным контейнером.

----
### Ответ:

  #### 1) Развертываем контейнер с СУБД MySQL версии 8
     
    root@docker:/home/bes/#  docker run -d -it  --name mysql1  -e MYSQL_ROOT_PASSWORD=my-secret-pw  -p 3306:3306  -v $(pwd)/mysql:/var/lib/mysql   mysql:8.0 

  #### 2) Сохраняем бэкап БД

    root@docker:/home/bes/#  docker exec mysql1  sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > $(pwd)/backup/all-databases.sql
    mysqldump: [Warning] Using a password on the command line interface can be insecure.
    root@docker:/home/bes#

  #### 3) Восстанавливаем БД

    root@docker:/home/bes/#  docker exec -i mysql1  sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < $(pwd)/backup/all-databases.sql
    mysql: [Warning] Using a password on the command line interface can be insecure.
    root@docker:/home/bes#

  #### 4) Входим в сессию интерфейса  mysql  с паролем  my-secret-pw .

    root@docker:/home/bes# docker exec -it 88d7769b4761   /bin/bash
    bash-4.4# mysql -u root -p my-secret-pw
         
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
        
    Connection id:          27
    Current database:
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
    Uptime:                 2 hours 5 min 50 sec
     
    Threads: 2  Questions: 941  Slow queries: 0  Opens: 240  Flush tables: 3  Open tables: 78  Queries per second avg: 0.124
    --------------
    
    mysql>

  #### 6) ddffdf 
      


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

----
### Ответ:



---
### Задача 3
Установите профилирование SET profiling = 1. Изучите вывод профилирования команд SHOW PROFILES;.
Исследуйте, какой engine используется в таблице БД test_db и приведите в ответе.
Измените engine и приведите время выполнения и запрос на изменения из профайлера в ответе:

на MyISAM
на InnoDB


---
### Задача 4
Изучите файл my.cnf в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб
 Приведите в ответе измененный файл my.cnf.

----
### Ответ:

