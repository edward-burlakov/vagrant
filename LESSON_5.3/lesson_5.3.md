# Домашнее задание к занятию "5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера"

## Задача 1

####  Сценарий выполнения задачи:
####  Cоздайте свой репозиторий на https://hub.docker.com;
####  Выберете любой образ, который содержит веб-сервер Nginx;
####  Создайте свой fork образа;
####  Реализуйте функциональность: запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
            <html>
            <head>
            Hey, Netology
            </head>
            <body>
            <h1>I’m DevOps Engineer!</h1>
            </body>
            </html>
####  Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.


## Ответ:

#### Входим на  сайт  https://hub.docker.com и ищем стабильную версию NGINX / В нашем случае это будет ubuntu/nginx:edge .

#### Скачиваем образ локально 

      root@docker:~/mysite# docker pull  ubuntu/nginx:edge

####  Для обновления образа  нужно создать из него контейнер, в который мы будем вносить изменения.
####  Создаем  контейнер и вносим в него изменения  

      root@docker:~/mysite#  docker run  -it  --name my_site ubuntu/nginx:edge  /bin/bash

####  Или входим внутрь запущенного контейнера с помощью команды exec 
      root@docker:~/mysite#   docker exec -it 3c523dca73d3  /bin/bash 

#### Устанавливаем  внутри контейнера  редактор nano
      root@3c523dca73d3 :~#     apt update && apt install nano

####  Внутри запущенного контейнера редактируем файл конфигурации /etc/nginx/sites-available/000-default.conf
      root@3c523dca73d3 :/etc/nginx/sites-available# cat 000-default.conf
            server {
                    listen 80;
                    listen [::]:80;

                    
                    root /home/site; #  Задаем новый путь к корню сайта . 
            
                    # Add index.php to the list if you are using PHP
                    index index.html index.htm
            
                    server_name mysite;
            
                    location / {
                            # First attempt to serve request as file, then
                            # as directory, then fall back to displaying a 404.
                            try_files $uri $uri/ =404;
                    }
            }
####  Делаем на него логическую ссылку  в каталоге  /etc/nginx/sites-enabled

      root@3c523dca73d3 :~#  ln -s  /etc/nginx/sites-available/000-default.conf 000-default.conf

####  Внутри запущенного контейнера создаем каталог ./home/site  и создаем файл  /home/site/index.html 

      root@3c523dca73d3 :~#   nano index.html

        <!DOCTYPE html>
           <html lang="ru">
           <head>
              <meta charset="utf-8">
              Hey, Netology
           </head>
           <body>
              <h1>I'am DevOps Engineer!</h1>
           </body>
        </html>      

####  Проверям конфигурацию NGINX 
   
        root@3c523dca73d3 :~#   nginx -t

####  Далее перечитаем конфигурацию nginx:

        root@3c523dca73d3 :~#  nginx -s reload


####   Выходим из контейнера 3c523dca73d3   
####   Главное - не останавливать его, чтобы не потерять внесенные изменения для нового образа !!!
 
    root@3c523dca73d3 :~# exit

    root@docker:~/home/bes# docker ps -a
    CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS        PORTS   NAMES
    3c523dca73d3   edwardburlakov/nginx:v1   "/docker-entrypoint.…"   6 minutes ago    Up 6 minutes  80/tcp  zealous_goodall

#### Cоздаем форк - новый образ "edwardburlakov/nginx:v2" со сделанными выше изменениями   
       
    root@docker:~# docker commit -m "Edited /root/mysite/index.html" -a "Edward Burlakov"   3c523dca73d3   edwardburlakov/nginx:v2
    sha256:b1f561e54e5ac13d489f28dfcc8239dcf4974dba40c32cf421c02b6b490400b9

####  Проверяем наличие созданного образа  "edwardburlakov/nginx:v2"

        root@docker:~# docker images
        REPOSITORY             TAG       IMAGE ID       CREATED          SIZE
        edwardburlakov/nginx   v2        3c523dca73d3   6 minutes ago    181MB
        ubuntu/nginx           edge      1589cd6fe298   8 days ago       143MB
        root@docker:~#

####  Используем новый образ "edwardburlakov/nginx:v2"   для запуска нового контейнера в фоновом режиме /
####  Останавливаем все запущенные ранее контейнеры, чтобы не было конфликта портов.  

       root@docker:~#  docker run -d  --name nginx-server  -p 8080:80  edwardburlakov/nginx:v2 

####  Открытие веб-страницы показало, что она сохранена внутри контейнера.

####  Авторизуемся в командной строке на https://hub.docker.com/ указав свой логин edwardburlakov.  
####  Запускаем процесс выгрузки  контейнера на hub.             

       root@docker:~# docker login && docker push edwardburlakov/nginx:v2
       Authenticating with existing credentials...
       WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
       Configure a credential helper to remove this warning. See
       https://docs.docker.com/engine/reference/commandline/login/#credentials-store
            
       Login Succeeded
       The push refers to repository [docker.io/edwardburlakov/nginx]
       67e88ef17645: Pushed
       e5bad10f7d54: Pushed
       d85c0bc2a850: Pushed
       ca141e230ffb: Mounted from ubuntu/nginx
       8d252ae2bf87: Mounted from ubuntu/nginx
       58a9a631c209: Mounted from ubuntu/nginx
       629d9dbab5ed: Mounted from ubuntu/nginx
       v1: digest: sha256:03441d01c34f736d18004ee16ee87bbbe33cb492b4274339879c25702e73494c size: 1782
       root@docker:~#

####  Ссылки на форк-образ

      https://hub.docker.com/layers/edwardburlakov/nginx/v2/images/sha256-7192894b1491d6c6b4ed955a9680dc85b1c63dfc734ca65b7921ac17f81b39c9?context=repo     
    
      docker pull edwardburlakov/nginx:v2



## Задача 2

###  Посмотрите на сценарий ниже и ответьте на вопрос: 
###  "Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет 
###  Виртуальная машина, физическая машина? Может быть возможны разные варианты?"
###  Детально опишите и обоснуйте свой выбор.
___

### Ответ:

### Сценарий:
-----------
#### Высоконагруженное монолитное java веб-приложение;
     - Рекомендую физический сервер.  
       Предполагается монолитная компоновка - следовательно микросервисной архитектура не применима без изменения кода. 
       Предполагается  высокая нагрузка  -  то необходим физический доступ к ресурсам (CPU и дискам), без использования слоя гипервизора.
---
#### Nodejs веб-приложение;
    - Это чистое веб-приложение, поэтому рекомендую контейнер в докере. 
      Контейнеризация позволит быстро развернуть приложение, включая  необходимые библиотеки.
---  
#### Мобильное приложение c версиями для Android и iOS;
    - Непонятно на чем реализована серверная часть приложения, а именно на какой платформе и языке. 
      Вполне вероятно, что используемый тип платформы не имеет подходящих образов docker-контейнеров. 
      Хотя С точки зрения масштабируемости ( огромное число пользователей) контейнеризация очень привлекательна. 

---
#### Шина данных на базе Apache Kafka;
    - Зависит от передаваемого трафика и типа сервера (тест-сервер или боевой сервер ).
      Для продуктовой среды - Виртуальная машина , или  Docker-контейнер, если потеря данных при потере контейнера не является критичной. 
      Для тестовой среды - Docker-контейнер.   

---
#### Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
    - Ноды Elasticsearch лучше развернуть на виртуальных хостах внутри отказоустойчивого кластера, например VMWARE VCenter,
      Все ноды kibana и logstash - в виртуальную машину  или развернуть на  docker-контейнерах, 
      т.к. существуют реализации в обоих исполнениях. 
   
---
#### Мониторинг-стек на базе Prometheus и Grafana;
    - Контейнеризация подходит.
      Данные  системы мониторинга не хранят данных, а являются системами визуализации данных,
      поэтому  данные сервисы можно развернуть в Докер-контейнерах .
   
---
#### MongoDB, как основное хранилище данных для java-приложения;
      Хотя у MongoDB даже есть официальный образ на Docker Hub и миллион скачиваний, я считаю, что контейнеризация не подходит,
      т.к. выключение контейнера приведет к потере всех изменённых данных, если не подключить внешнее хранилище-каталог в хост-системе  
       или не обеспечить корректные  права доступа. 
      Поэтому можно использовать либо физический, либо виртуальный хост.
      Первый вариант менее предпочтителен из-за неэффективного использования ресурсов.
      Хотя это зависит от области применения и нагрузки на БД.

---
#### Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.
     Для организации Gitlab сервер подойдет  при условии хранения данных на внешнем подключаемом ресурсе .
     Плюсом будет легкость реализации запуска runner-сервисов  для пользователей .

     Для организации приватный (закрытый) Docker Registry  контейнеризация  не подойдет. Причины:  
      1) низкий уровень  изоляции контейнеров от хоста не обеспечит полной безопасности хранения docker-образов .
      2) Выключение контейнера приведет к потере всех изменённых данных.

## Задача 3

####  Запустите первый контейнер из образа centos c любым тэгом в фоновом режиме, подключив папку /data из текущей рабочей директории на хостовой машине в /data контейнера;
####  Запустите второй контейнер из образа debian в фоновом режиме, подключив папку /data из текущей рабочей директории на хостовой машине в /data контейнера;
####  Подключитесь к первому контейнеру с помощью docker exec и создайте текстовый файл любого содержания в /data;
####  Добавьте еще один файл в папку /data на хостовой машине;
####  Подключитесь во второй контейнер и отобразите листинг и содержание файлов в /data контейнера.

---
###  Ответ:

#### Создаем каталог  /root/data на сервере с докером 
    root@docker2:~# cd /root && mkdir data

#### Запускаем образы а машине docker2

    root@docker2:~# docker run -it --rm -d --name centos1  -v /root/data/:/data/  centos:centos7  
    62b7447127c732d48230855402a13806848505946cebab9db6312cb9ced496b0
    
    root@docker2:~# docker run -it --rm -d --name debian1   -v /root/data/:/data/  debian:stable 
    5791c56824b4243576df1ab00c5ec005774cac77440e985d2a11b31c3ad26bb4

    root@docker2:~# docker ps -a
    CONTAINER ID   IMAGE            COMMAND       CREATED              STATUS              PORTS     NAMES
    c2d78b2b776d   centos:centos7   "/bin/bash"   4 seconds ago        Up 2 seconds                  centos1
    9d02ce103606   debian:stable    "bash"        About a minute ago   Up About a minute             debian1
    root@docker2:~#

#### Входим внутрь контейнера centos1

     root@docker2:~#  docker exec -it  c2d78b2b776d  /bin/bash
   
#### Создаем файл, заполняем его и проверяем содержимое
     [root@c2d78b2b776d /]# cd / && touch /data/newfile.txt

     [root@c2d78b2b776d data]#  echo 'Thats all right, baby!' > /data/newfile.txt
     
     [root@c2d78b2b776d /]# cat  /data/newfile.txt
     Thats all right, baby!
     root@docker2:~#

#### Создаем файл на хостовой машине docker2
     root@docker2:~# cd /root/data/ && touch newfile2.txt
     root@docker2:~#  echo 'I am your baby tonight!' > ./root/data/newfile2.txt
     root@docker2:~# cat ./root/data/newfile2.txt
     I am your baby tonight!
     root@docker2:~#


#### Проверяем содержимое  каталога  ./data на контейнере с debian1

    root@docker2:~#  docker exec -it  debian1  /bin/bash
    root@9d02ce103606:~# cd /data  &&  ls -la
    drwxr-xr-x 2 root root 4096 Sep  1 20:28 .
    drwxr-xr-x 1 root root 4096 Sep  1 20:04 ..
    -rw-r--r-- 1 root root   23 Sep  1 20:12 newfile.txt
    -rw-r--r-- 1 root root   24 Sep  1 20:24 newfile2.txt

#### Проверяем содержимое  файлов в каталоге  ./data на контейнере с debian1    
    root@9d02ce103606:/data# cat /data/newfile.txt && cat /data/newfile2.txt
    Thats all right, baby!
    I am your baby tonight!
    root@9d02ce103606:/data#



---

#### Задача 4 (*)

#### Воспроизвести практическую часть лекции самостоятельно.
#### Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.