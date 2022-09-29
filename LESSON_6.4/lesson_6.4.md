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

1) root@docker:/home/bes/backup# cd /home/bes

      root@docker:/home/bes/#  docker run -d -it    --name postgres12   -e POSTGRES_PASSWORD=mysecretpassword   -p 5432:5432  \ 
      -v $(pwd)/data:/var/lib/postgresql/data   -v $(pwd)/backup:/backup   postgres:12 

2) Входим в запущенный контейнер

             root@docker:/home/bes/data#  docker exec -it   dd8781c1393e  /bin/bash

3) Запускаем PostgreSQL интерактивно 
   
             root@docker:/home/bes/data# psql -U postgres

4) Создаем  БД test_db :
            
             postgres=# create database  test_db ;
             CREATE DATABASE
             postgres=#

5) Устанавливаем подключение к БД с помощью sql 

            root@docker:/home/bes/data#  psql test_db postgres;   ( или psql -Upostgres  -dtest_db )

6) Создаем таблицы в БД test_db

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

7) Смотрим итоги

              test_db=# \dt
              public | clients | table | postgres
              public | orders  | table | postgres
8) Выходим 
              test_db=# quit


---
### Задача 2
Используя psql создайте БД test_database.
Изучите бэкап БД.
Восстановите бэкап БД в test_database.
Перейдите в управляющую консоль psql внутри контейнера.
Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.
Используя таблицу pg_stats, найдите столбец таблицы orders с наибольшим средним значением размера элементов в байтах.
Приведите в ответе команду, которую вы использовали для вычисления и полученный результат.


---
### Ответ:


---
### Задача 3
- Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и поиск по ней 
- занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили провести разбиение таблицы 
- на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).
- Предложите SQL-транзакцию для проведения данной операции.
- Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?


---
### Ответ:


---
### Задача 4

- Используя утилиту pg_dump создайте бекап БД test_database.
- Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца title для таблиц test_database?


---
### Ответ:
