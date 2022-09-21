## Домашнее задание к занятию "6.2. SQL"

### Задача 1
Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

----
### Ответ:

      root@docker:/home/bes/backup# cd /home/bes

      root@docker:/home/bes/#  docker run -d -it    --name postgres12   -e POSTGRES_PASSWORD=mysecretpassword   -p 5432:5432  \ 
      -v $(pwd)/data:/var/lib/postgresql/data   -v $(pwd)/backup:/backup   postgres:12 

### Задача 2
В БД из задачи 1:

- Cоздайте пользователя test-admin-user и БД test_db
  в БД test_db создайте таблицу orders и clients ( спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

        Таблица orders:
        id (serial primary key)    наименование (string)   цена (integer)

        Таблица clients:
        id (serial primary key)    фамилия (string)   страна проживания (string, index)    заказ (foreign key orders)

Приведите:
- Итоговый список БД после выполнения пунктов выше, 
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- Cписок пользователей с правами над таблицами test_db

----
### Ответ:

         1) Входим в запущенный контейнер 
             root@docker:/home/bes/data#  docker exec -it   dd8781c1393e  /bin/bash

         2) Запускаем PostgreSQL интерактивно 
             root@docker:/home/bes/data# psql -U postgres

         3) Создаем  БД test_db :
            
             postgres=# create database  test_db ;
             CREATE DATABASE
             postgres=#

         4) Устанавливаем подключение к БД
             root@docker:/home/bes/data#  psql test_db postgres;   ( или psql -Upostgres  -dtest_db )

         5) Создаем таблицы в БД test_db  
            CREATE TABLE orders ( 
                order_id      SERIAL PRIMARY KEY,  
                product_name  varchar(40) NOT NULL CHECK (product_name <> ''),  
                price         integer NOT NULL,
                );
        
            CREATE TABLE clients (
                id            SERIAL PRIMARY KEY,   
                surname       varchar(30),   
                country       varchar(20),    
                order_id      INT, 
                FOREIGN KEY (order_id) REFERENCES orders(order_id)                 
                );
           
            CREATE INDEX country_idx ON clients(country);

         6) Смотрим итоги
             test_db=# \dt
             public | clients | table | postgres
             public | orders  | table | postgres

            test_db=# \d clients
                                                Table "public.clients"
              Column  |         Type          | Collation | Nullable |               Default
            ----------+-----------------------+-----------+----------+-------------------------------------
             id       | integer               |           | not null | nextval('clients_id_seq'::regclass)
             surname  | character varying(30) |           |          |
             country  | character varying(20) |           |          |
             order_id | integer               |           |          |
            Indexes:
                "clients_pkey" PRIMARY KEY, btree (id)
                "country_idx" btree (country)
            Foreign-key constraints:
                "clients_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(order_id)


            tst_db-# \d orders
                                                     Table "public.orders"
                Column    |         Type          | Collation | Nullable |                 Default
            --------------+-----------------------+-----------+----------+------------------------------------------
             order_id     | integer               |           | not null | nextval('orders_order_id_seq'::regclass)
             product_name | character varying(40) |           | not null |
             price        | integer               |           | not null |
            Indexes:
                "orders_pkey" PRIMARY KEY, btree (order_id)
            Check constraints:
                "orders_product_name_check" CHECK (product_name::text <> ''::text)
            Referenced by:
                TABLE "clients" CONSTRAINT "clients_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(order_id)

         
         7) Создаем пользователя  test-admin-user 
             root@docker:/home/bes/data# sudo su - postgres -c "createuser test_admin_user with login password 'qwerty';"

             postgres=# create user  test_admin_user with login password 'qwerty';
             CREATE ROLE
             postgres=#

         8) Даем полные права для пользователя test-admin-user на БД test_db 

             postgres=# grant all privileges on database test_db to test_admin_user;
             GRANT
             postgres=#

         9) Проверяем наличие прав суперпользователя у пользователя test_admin_user

             postgres=# \l
                                        List of databases
                   Name    |  Owner   | Encoding |  Collate   |   Ctype    |      Access privileges
                -----------+----------+----------+------------+------------+------------------------------
                 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
                 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                 +
                           |          |          |            |            | postgres=CTc/postgres
                 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                 +
                           |          |          |            |            | postgres=CTc/postgres
                 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/postgres                +
                           |          |          |            |            | /postgres       +
                           |          |          |            |            | test_admin_user=CTc/postgres

         10)  Создаем пользователя  test_simple_user и выделяем права на таблицы clients и orders в БД test_db 

             test_db=# create user  test_simple_user with login password 'qwerty';
             CREATE ROLE
             test_db=# GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE clients TO test_simple_user;
             GRANT
             test_db=# GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE orders  TO test_simple_user;
             GRANT

         11) Проверяем наличие прав доступа для всех пользователей
               test_db=# \l
                                    List of databases
               Name    |  Owner   | Encoding |  Collate   |   Ctype    |      Access privileges
            -----------+----------+----------+------------+------------+------------------------------
             postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
             template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                 +
                       |          |          |            |            | postgres=CTc/postgres
             template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                 +
                       |          |          |            |            | postgres=CTc/postgres
             test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/postgres                +
                       |          |          |            |            | postgres=CTc/postgres       +
                       |          |          |            |            | test_admin_user=CTc/postgres+
                       |          |          |            |            | test_simple_user=c/postgres
            (4 rows)


         12) Выводим листинг всех пользователй и ролей 
             test_db-# \du
                                                   List of roles
                Role name     |                         Attributes                         | Member of
            ------------------+------------------------------------------------------------+-----------
             postgres         | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
             test_admin_user  |                                                            | {}
             test_simple_user |                                                            | {}



         13) Выводим список всех пользователей БД test_db c правами доступа  к таблицам с помощью  SQL- запроса

            test_db=# SELECT * from information_schema.table_privileges where grantee in ('test_admin_user','test_simple_user');

             grantor  |     grantee      | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy
            ----------+------------------+---------------+--------------+------------+----------------+--------------+----------------
             postgres | test_simple_user | test_db       | public       | clients    | INSERT         | NO           | NO
             postgres | test_simple_user | test_db       | public       | clients    | SELECT         | NO           | YES
             postgres | test_simple_user | test_db       | public       | clients    | UPDATE         | NO           | NO
             postgres | test_simple_user | test_db       | public       | clients    | DELETE         | NO           | NO
             postgres | test_simple_user | test_db       | public       | orders     | INSERT         | NO           | NO
             postgres | test_simple_user | test_db       | public       | orders     | SELECT         | NO           | YES
             postgres | test_simple_user | test_db       | public       | orders     | UPDATE         | NO           | NO
             postgres | test_simple_user | test_db       | public       | orders     | DELETE         | NO           | NO
            (8 rows)
     
            
---
### Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

    Таблица orders
        Наименование	цена
        Шоколад	10
        Принтер	3000
        Книга	500
        Монитор	7000
        Гитара	4000
    
    Таблица clients
        ФИО	Страна проживания
        Иванов Иван Иванович	USA
        Петров Петр Петрович	Canada
        Иоганн Себастьян Бах	Japan
        Ронни Джеймс Дио	Russia
        Ritchie Blackmore	Russia

Используя SQL синтаксис:
Вычислите количество записей для каждой таблицы
приведите в ответе:
запросы
результаты их выполнения.

----
### Ответ:

   1) Вставляем значения в таблицу orders  и проверяем результат 

           test_db=# INSERT INTO orders (product_name, price) VALUES ( 'Шоколад', 10), ( 'Принтер', 3000) ,  \ 
           ( 'Книга', 500),( 'Монитор', 7000), ( 'Гитара', 4000);
           INSERT 0 5
           test_db=# select * from orders;
                 order_id | product_name | price
                ----------+--------------+-------
                        1 | Шоколад      |    10
                        2 | Принтер      |  3000
                        3 | Книга        |   500
                        4 | Монитор      |  7000
                        5 | Гитара       |  4000
                (5 rows)

   2) Вставляем значения в таблицу clients (учитывая наличие индексов)  и проверяем результат

          test_db=# INSERT INTO clients (surname, country) VALUES ( 'Иванов Иван Иванович', 'USA') , ( 'Петров Петр Петрович', 'Canada') , \ 
          ( 'Иоганн Себастьян Бах', 'Japan') , ( 'Ронни Джеймс Дио', 'Russia') , ( 'Ritchie Blackmore', 'Russia') ON CONFLICT DO NOTHING;
          INSERT 0 4
          test_db=# select * from clients;
             id |       surname        | country | order_id
            ----+----------------------+---------+----------
              6 | Иванов Иван Иванович | USA     |
              7 | Петров Петр Петрович | Canada  |
              8 | Иоганн Себастьян Бах | Japan   |
              9 | Ронни Джеймс Дио     | Russia  |
            (4 rows)
            
   3) Вычисляем количество записей для каждой таблицы

          test_db=# select count (*) from orders;
          count
          -------
          5
          (1 row)

          test_db=# select count (*) from clients;
          count
          -------
          4
          (1 row)


---
### Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

    ФИО                  	Заказ
    Иванов Иван Иванович	Книга
    Петров Петр Петрович	Монитор
    Иоганн Себастьян Бах	Гитара

Приведите SQL-запросы для выполнения данных операций.
Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
Подсказка - используйте директиву UPDATE.

----
### Ответ:

      Используя foreign keys связываем записи из таблиц:
      
            UPDATE clients  SET order_id = 3 WHERE id = 6;
            UPDATE clients  SET order_id = 4 WHERE id = 7;
            UPDATE clients  SET order_id = 5 WHERE id = 8;

      Получаем список клиентов, имеющих записи в таблице заказов:

            test_db=# SELECT * from clients  c  where exists (select order_id from orders as o where c.order_id = o.order_id) ;
             id |       surname        | country | order_id
            ----+----------------------+---------+----------
              6 | Иванов Иван Иванович | USA     |        3
              7 | Петров Петр Петрович | Canada  |        4
              8 | Иоганн Себастьян Бах | Japan   |        5
            (3 rows)


      Еще вариант 2 :
            test_db=# select * from clients where order_id is not null ;
             id |       surname        | country | order_id
            ----+----------------------+---------+----------
              6 | Иванов Иван Иванович | USA     |        3
              7 | Петров Петр Петрович | Canada  |        4
              8 | Иоганн Себастьян Бах | Japan   |        5
            (3 rows)
---
### Задача  5
Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 (используя директиву EXPLAIN).
Приведите получившийся результат и объясните что значат полученные значения.
 
----
### Ответ:

    Вариант 1

      test_db=# EXPLAIN SELECT * from clients  c  where exists (select order_id from orders as o where c.order_id = o.order_id) ;
                                    QUERY PLAN
      -----------------------------------------------------------------------
       Hash Join  (cost=23.50..39.44 rows=470 width=144)
         Hash Cond: (c.order_id = o.order_id)
         ->  Seq Scan on clients c  (cost=0.00..14.70 rows=470 width=144)
         ->  Hash  (cost=16.00..16.00 rows=600 width=4)
               ->  Seq Scan on orders o  (cost=0.00..16.00 rows=600 width=4)
      (5 rows)



    Вариант 2

      test_db=# EXPLAIN select * from clients where order_id is not null ;
                               QUERY PLAN
      ------------------------------------------------------------
       Seq Scan on clients  (cost=0.00..14.70 rows=468 width=144)
         Filter: (order_id IS NOT NULL)
      (2 rows)
      
     EXPLAIN отображает  - последовательность узлов -шагов при выполении плана запроса , 
     - Приблизительная стоимость запуска узла 
     - Приблизительная общая стоимость 
     - Ожидаемое число  обработанных строк на каждом узле плана. 
     - Ожидаемый средний размер строк, выводимых этим узлом плана (в байтах)   

    Второй вариант будет работать быстрее. 


---
### Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).
Остановите контейнер с PostgreSQL (но не удаляйте volumes).
Поднимите новый пустой контейнер с PostgreSQL.
Восстановите БД test_db в новом контейнере.
Приведите список операций, который вы применяли для бэкапа данных и восстановления.

----
### Ответ:

      1) Выполняем бэкап БД из старого контейнера, включая информацию о ролях и табличных пространствах: 
     
         Либо внутри докер-контейнера 

         root@dd8781c1393e:/backup# pg_dumpall -U postgres  -f /backup/dump_test1.sql
         root@dd8781c1393e:/backup# ls -la
         total 16
         drwxr-xr-x 2 root root 4096 Sep 21 08:38 .
         drwxr-xr-x 1 root root 4096 Sep 20 16:01 ..
         -rw-r--r-- 1 root root 4419 Sep 21 08:38 dump_test1.sql

         Либо на докер-хосте 

         docker exec -t postgres12  pg_dumpall -U postgres -f /backup/dump_test1.sql

      2) Создаем абсолютно новый контейнер на базе образа postgres:12, находясь в рабочем каталоге и подключая каталог с бэкапами

         root@docker:/home/bes/backup# cd /home/bes
         root@docker:/home/bes/#  docker run -d -it  --name postgres12.v1  -e POSTGRES_PASSWORD=mysecretpassword  \ 
         -p 5434:5432  -v $(pwd)/backup:/backup   postgres12:v1
      
      3) Восстанавливаем образ, созданный с помощью pg_dumpall
      
            root@docker:/home/bes# docker exec -u postgres -t postgres12.v1  psql -f /backup/dump_test1.sql postgres
            SET
            SET
            SET
            ALTER ROLE
            CREATE ROLE
            ALTER ROLE
            CREATE ROLE
            ALTER ROLE
            You are now connected to database "template1" as user "postgres".
            SET
            SET
            SET
            SET
            SET
             set_config
            ------------
            
            (1 row)
            
            SET
            SET
            SET
            SET
            You are now connected to database "postgres" as user "postgres".
            SET
            SET
            SET
            SET
            SET
             set_config
            ------------
            
            (1 row)
            
            SET
            SET
            SET
            SET
            SET
            SET
            SET
            SET
            SET
             set_config
            ------------
            
            (1 row)
            
            SET
            SET
            SET
            SET
            CREATE DATABASE
            ALTER DATABASE
            You are now connected to database "test_db" as user "postgres".
            SET
            SET
            SET
            SET
            SET
             set_config
            ------------
            
            (1 row)
            
            SET
            SET
            SET
            SET
            SET
            SET
            CREATE TABLE
            ALTER TABLE
            CREATE SEQUENCE
            ALTER TABLE
            ALTER SEQUENCE
            CREATE TABLE
            ALTER TABLE
            CREATE SEQUENCE
            ALTER TABLE
            ALTER SEQUENCE
            ALTER TABLE
            ALTER TABLE
            COPY 4
            COPY 5
             setval
            --------
                 10
            (1 row)
            
             setval
            --------
                  5
            (1 row)
            
            ALTER TABLE
            ALTER TABLE
            CREATE INDEX
            ALTER TABLE
            GRANT
            GRANT
            GRANT
            GRANT
            
            #

