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

####  Задаем новый путь к корню сайта  - /home/site 
                    root /home/site;
            
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

####  Внутри запущенного контейнера создаем каталог ./home/site  
####  и создаем файл  /home/site/index.html 

      root@3c523dca73d3 :~#   nano index.html

        <!DOCTYPE html>
           <html lang="ru">
           <head>
              <meta charset="utf-8">
              Hey, Netology
           </head>
           <body>
              <h1>I ^`^ym DevOps Engineer!</h1>
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
        CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS                      PORTS     NAMES
        3c523dca73d3   edwardburlakov/nginx:v1   "/docker-entrypoint.…"   6 minutes ago    Up 6 minutes                80/tcp    zealous_goodall

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

##  Посмотрите на сценарий ниже и ответьте на вопрос: 
##  "Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет 
##  Виртуальная машина, физическая машина? Может быть возможны разные варианты?"
##  Детально опишите и обоснуйте свой выбор.
___

Сценарий:
-----------

Высоконагруженное монолитное java веб-приложение;

---
Nodejs веб-приложение;

---
Мобильное приложение c версиями для Android и iOS;

---
Шина данных на базе Apache Kafka;

---
Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;

---
Мониторинг-стек на базе Prometheus и Grafana;

---
MongoDB, как основное хранилище данных для java-приложения;

---
Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.


###  Создаем  /root/mydockerbuild/Dockerfile

        root@docker:~/mydockerbuild# cat /root/mydockerbuild/Dockerfile
        FROM ubuntu/nginx:edge
        
        #RUN apk add nginx && \
        #    mkdir -p /run/nginx && \
        #    mkdir /src && \
        #    touch /run/nginx/nginx.pid
        
        EXPOSE 80 443
        
        CD /

        COPY ./mysite/default.conf /etc/nginx/conf.d/default.conf
        
        COPY ./mysite/index.html /var/www/html/index.html
        
        CMD ["nginx","-g","daemon off;"]
        
        root@docker:~/mydockerbuild#




## Задача 3

##  Запустите первый контейнер из образа centos c любым тэгом в фоновом режиме, подключив папку /data из текущей рабочей директории на хостовой машине в /data контейнера;
##  Запустите второй контейнер из образа debian в фоновом режиме, подключив папку /data из текущей рабочей директории на хостовой машине в /data контейнера;
##  Подключитесь к первому контейнеру с помощью docker exec и создайте текстовый файл любого содержания в /data;
##  Добавьте еще один файл в папку /data на хостовой машине;
##  Подключитесь во второй контейнер и отобразите листинг и содержание файлов в /data контейнера.


## Задача 4 (*)

### Воспроизвести практическую часть лекции самостоятельно.
### Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.