## Домашнее задание к занятию "6.4. PostgreSQL"

---
### Задача 1

- Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.
- Подключитесь к БД PostgreSQL используя psql.
- Воспользуйтесь командой \? для вывода подсказки по имеющимся в psql управляющим командам.
- Найдите и приведите управляющие команды для:
    вывода списка БД
    подключения к БД
    вывода списка таблиц
    вывода описания содержимого таблиц
    выхода из psql

---
### Ответ:

1) Поднимаем инстанс PostreSQL         

            root@docker:/home/bes/#  docker run -d -it    --name postgres13   -e POSTGRES_PASSWORD=mysecretpassword   -p 5432:5432  \ 
            -v $(pwd)/data:/var/lib/postgresql/data   postgres:13 

2) Входим в запущенный контейнер

             root@docker:/home/bes/data#  docker exec -it   cd864a17ac58  /bin/bash

3) Устанавливаем подключение к БД с помощью psql 

            root@cd864a17ac58:/#  psql postgres postgres;   ( или psql -Upostgres  -dpostgres )

4) Выводим список команд  
                        
            postgres=# \?
            ...
          
5) Выводим список БД

             postgres=# \l
                                   List of databases
                 Name      |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
             ---------------+----------+----------+------------+------------+-----------------------
             postgres      | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
             template0     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
                           |          |          |            |            | postgres=CTc/postgres
             template1     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
                           |          |          |            |            | postgres=CTc/postgres
             test_database | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
             (4 rows)


6) Подключаемся к БД                     \c  {db_name}   или \connect {db_name}

            postgres=#  \с  test_database

7) Выводим список таблиц 

            test_database=# \dt ;
                    List of relations
            Schema |  Name  | Type  |  Owner
            --------+--------+-------+----------
            public | orders | table | postgres
           (1 row)
   
8) Выводим описание содержимого таблиц      \d  {table_name}
       
            test_database-# \d orders
                                    Table "public.orders"
             Column |         Type          | Collation | Nullable |              Default
            --------+-----------------------+-----------+----------+------------------------------------
             id     | integer               |           | not null | nextval('orders_id_seq'::regclass)
             title  | character varying(80) |           | not null |
             price  | integer               |           |          | 0
            Indexes:
            "orders_pkey" PRIMARY KEY, btree (id)

       

9) Выходим  из psql   -  \q или  quit 

            postgres=# quit


---
### Задача 2
- Используя psql создайте БД test_database.
- Изучите бэкап БД.
- Восстановите бэкап БД в test_database.
- Перейдите в управляющую консоль psql внутри контейнера.
- Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.
- Используя таблицу pg_stats, найдите столбец таблицы orders с наибольшим средним значением размера элементов в байтах.
- Приведите в ответе команду, которую вы использовали для вычисления и полученный результат.


---
### Ответ:

1) Создаем  БД test_database :
            
         postgres=# create database test_database ;
         CREATE DATABASE
         postgres=#

2) Подключаемся к БД

        postgres=# \c test_database ;
        You are now connected to database "test_database" as user "postgres".
        test_database=#

3) Скачиваем и восстанавливаем бэкап

        root@cd864a17ac58:/#  psql -Upostgres test_database  < test_dump.sql

4) Входим в интерфейс  управляющей консоли psql  внутри контейнера и проводим анализ таблицы в БД

        root@cd864a17ac58:/#  psql test_database  postgres; 

        test_database=# ANALYZE  VERBOSE  orders ;
        INFO:  analyzing "public.orders"
        INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 8 dead rows; 8 rows in sample, 8 estimated total rows
        ANALYZE
        test_database=#

5) Смотрим текущую активность работы с БД  и закрываем  ненужные соединения 
   
        test_database=#  SELECT datname,usename,client_addr,client_port FROM pg_stat_activity ;
        test_database=#  SELECT pg_terminate_backend(7408);


6) C помощью таблицы pg_stats ищем столбец таблицы orders с наибольшим средним значением размера элементов в байтах. 
 
       test_database=# SELECT attname, avg_width FROM pg_stats  WHERE tablename = 'orders' ORDER BY avg_width DESC;
       attname | avg_width
       ---------+-----------
       title   |        16
       id      |         4
       price   |         4
       (3 rows)
      
       test_database=#


---
### Задача 3
- Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и поиск по ней 
- занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили провести разбиение таблицы 
- на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).
- Предложите SQL-транзакцию для проведения данной операции.
- Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

---
### Ответ:

1) Шардируем основную таблицу на две дочерние c помощью SQL запросов:

         CREATE table orders_1 (
            CHECK  ( price > 499)
         ) INHERITS (orders) ;

         CREATE table orders_2 (
            CHECK  ( price <= 499)
         ) INHERITS (orders) ;

2) Для исключения дальнейшего "ручного" разбиения добавляем 2 правила на основную таблицу, 
  которые записывают все результаты выполнения операнда INSERT над таблицей orders  в дочерние таблицы orders_1  и orders_2  


         CREATE OR REPLACE RULE orders_insert_to_1 AS
             ON INSERT TO public.orders
             WHERE (new.price > 499)
             DO INSTEAD
         (INSERT INTO orders_1 (id, title, price)
           VALUES (new.id, new.title, new.price));
         
         
         
         CREATE OR REPLACE RULE orders_insert_to_2 AS
             ON INSERT TO public.orders
             WHERE (new.price <= 499)
             DO INSTEAD
         (INSERT INTO orders_2 (id, title, price)
           VALUES (new.id, new.title, new.price));

  3) Изначально при проектировании необходимо было создавать исходный код,
     включающий запросы c  оператором INSERT  c условием WHERE для наполнения двух таблиц 
     и формирования вертикального шардирования. 

---
### Задача 4
- Используя утилиту pg_dump создайте бекап БД test_database.
- Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца title для таблиц test_database?

  
---
### Ответ: 

1) Создаем бэкап БД
            
          root@cd864a17ac58:/#   pg_dump -U postgres -d  test_database  > test_database_dump.sql

2) Открываем файл в test_database_dump.sql на редатирование и для задания уникальности столбцу title добавляем аттрибут UNIQUE  в виде CONSTRAINTS 

          ...
          CREATE TABLE public.order (
            id integer NOT NULL ,
            title character varying(80) NOT NULL  UNIQUE ,
            price integer DEFAULT 0
          );
          ...

3) Если мы не ходим создавать БД  с нуля можно создать  копию существующей таблицы (н-р, orders5 )  с наложением ограничения.

          CREATE TABLE IF NOT EXISTS public.orders5
           (   CONSTRAINT orders5_title_key UNIQUE (id)  )
          INHERITS (public.orders)
          TABLESPACE pg_default;
          ALTER TABLE IF EXISTS public.orders4  OWNER to postgres;
