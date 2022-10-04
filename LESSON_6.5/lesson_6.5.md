## Домашнее задание к занятию "6.5. Elasticsearch"

---
### Задача 1
В этом задании вы потренируетесь в:
- Установке elasticsearch
- Первоначальном конфигурировании elasticsearch
- Запуске elasticsearch в docker

Используя докер образ elasticsearch:7 как базовый:
1) Составьте Dockerfile-манифест для elasticsearch
2) Соберите docker-образ и сделайте push в ваш docker.io репозиторий
3) запустите контейнер из получившегося образа и выполните запрос пути / c хост-машины

Требования к elasticsearch.yml:
  - Данные path должны сохраняться в /var/lib
  - Имя ноды должно быть netology_test

В ответе приведите:
  - текст Dockerfile манифеста
  - ссылку на образ в репозитории dockerhub
  - ответ elasticsearch на запрос пути / в json виде

#### Подсказки:

- При сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml   .
При некоторых проблемах вам поможет docker директива ulimit
Elasticsearch в логах обычно описывает проблему и пути ее решения

- Обратите внимание на настройки безопасности такие как xpack.security.enabled
если докер образ не запускается и падает с ошибкой 137 в этом случае может помочь настройка -e ES_HEAP_SIZE
при настройке path возможно потребуется настройка прав доступа на директорию
Далее мы будем работать с данным экземпляром elasticsearch.

---
### Ответ:

1) Создаем репозиторий  https://github.com/edward-burlakov/elasticsearch
2) Подключаем к нему runner на локальной машине с докером, в которой будет выполнен  build нового образа
3) В репозитории создаем следующий Dockerfile файл:

        FROM elasticsearch:7.0.0
   
        LABEL description="Netology_test"
   
        ENV PATH=/usr/lib:$PATH
   
        ADD elasticsearch.yml /usr/share/elasticsearch/config

        EXPOSE 9200

        USER elasticsearch

4) В репозитории создаем следующий elasticsearch.yml  файл:

          # ======================== Elasticsearch Configuration =========================
          #
          # ---------------------------------- Cluster -----------------------------------
          #
          # Use a descriptive name for your cluster:
          #
          cluster.name: netology_test
          discovery.type: single-node

          #
          # ------------------------------------ Node ------------------------------------
          #
          # Use a descriptive name for the node:
          #
          #node.name: node-1
          #
          # Add custom attributes to the node:
          #
          #node.attr.rack: r1
          #
          # ----------------------------------- Paths ------------------------------------
          #
          # Path to directory where to store the data (separate multiple locations by comma):
          #
           path.data: /var/lib/data
   
          #
          # Path to log files:
          #
          path.logs: /var/lib/logs

          # ----------------------------------- Memory -----------------------------------
          #
          # Lock the memory on startup:
          #
          #bootstrap.memory_lock: true
          #
          # Make sure that the heap size is set to about half the memory available
          # on the system and that the owner of the process is allowed to use this
          # limit.
          #
          # Elasticsearch performs poorly when the system is swapping the memory.
          #
          # ---------------------------------- Network -----------------------------------
          #
          # Set the bind address to a specific IP (IPv4 or IPv6):
          #
          network.host: 0.0.0.0
          #
          # Set a custom port for HTTP:
          #
          http.port: 9200
          #
          # For more information, consult the network module documentation.
          #
          # --------------------------------- Discovery ----------------------------------
          #
          # Pass an initial list of hosts to perform discovery when this node is started:
          # The default list of hosts is ["127.0.0.1", "[::1]"]
          #
          discovery.seed_hosts: ["127.0.0.1", "[::1]"]
   
          #
          # Bootstrap the cluster using an initial set of master-eligible nodes:
          #
          #cluster.initial_master_nodes: ["node-1", "node-2"]
          #
          # For more information, consult the discovery and cluster formation module documentation.
          #
          # ---------------------------------- Gateway -----------------------------------
          #
          # Block initial recovery after a full cluster restart until N nodes are started:
          #
          #gateway.recover_after_nodes: 3
          #
          # For more information, consult the gateway module documentation.
          #
          # ---------------------------------- Various -----------------------------------
          #
          # Require explicit names when deleting indices:
          #


5) В workflow  создаем новый job-сценарий сборки образа 
      [https://github.com/edward-burlakov/elasticsearch/blob/main/.github/workflows/docker-image.yml]
 
          name: Docker Image CI
    
        on:
        push:
            branches: [ "main" ]
        pull_request:
            branches: [ "main" ]
        jobs:
    
            build:
    
            runs-on: self-hosted
    
            steps:
            - uses: actions/checkout@v3
            - name: Build the Docker image
             run: docker build . --file Dockerfile --tag netology_test:$(date +%s)

6) Запускаем задачу сборки образа

7) Запускаем однонодовый кластер Elasticsearch

       root@docker:/home/bes#  docker network create elknetwork
       root@docker:/home/bes#  docker run -d --name netology_test  --net elknetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" netology_test:0.0.1

8) Развертываем Kibana
       
       root@docker:/home/bes#   docker pull kibana:7.0.0
       root@docker:/home/bes#   docker run --name kibana --net elknetwork -p 5601:5601 kibana:7.0.0

9) Входим внутрь контейнера
   
        root@docker:/home/bes#  docker exec -it 7fab8c1cab18 /bin/bash

10) Проверяем работу сервиса. Выполним к нему запрос о его статусе с помощью API-интерфейса:

        [elasticsearch@7fab8c1cab18 config]$ curl 127.0.0.1:9200
        {
           "name" : "7fab8c1cab18",
           "cluster_name" : "netology_test",
           "cluster_uuid" : "GUuB3C5YTnaLA1EZjBiaLg",
           "version" : {
             "number" : "7.0.0",
             "build_flavor" : "default",
             "build_type" : "docker",
             "build_hash" : "b7e28a7",
             "build_date" : "2019-04-05T22:55:32.697037Z",
             "build_snapshot" : false,
             "lucene_version" : "8.0.0",
             "minimum_wire_compatibility_version" : "6.7.0",
             "minimum_index_compatibility_version" : "6.0.0-beta1"
           },
           "tagline" : "You Know, for Search"
        }

---
### Задача 2
В этом задании вы научитесь:

- Создавать и удалять индексы
- Изучать состояние кластера
- Обосновывать причину деградации доступности данных

1) Ознакомьтесь с документацией и добавьте в elasticsearch 3 индекса, в соответствии со таблицей:

| Имя	     | Количество реплик | Количество шард  |
|-----------|-------------------|------------------|
| ind-1     | 0                 | 1                |
| ind-2  	 | 1                 | 2                |
| ind-3	 | 2                 | 4                |

2) Получите список индексов и их статусов, используя API и приведите в ответе на задание.
3) Получите состояние кластера elasticsearch, используя API.
   Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?
4) Удалите все индексы.

Важно!!!
При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард, 
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

---
### Ответ:

1) Создаем индексы с помощью API-интерфейса:

       [elasticsearch@7fab8c1cab18 config]$   curl -X PUT localhost:9200/ind-1 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
       {"acknowledged":true,"shards_acknowledged":true,"index":"ind-1"}

       [elasticsearch@7fab8c1cab18 config]$  curl -X PUT localhost:9200/ind-2 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 2,  "number_of_replicas": 1 }}'
       {"acknowledged":true,"shards_acknowledged":true,"index":"ind-2"}

       [elasticsearch@7fab8c1cab18 config]$  curl -X PUT localhost:9200/ind-3  -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 4,  "number_of_replicas": 2 }}'
       {"acknowledged":true,"shards_acknowledged":true,"index":"ind-3"}

3) Получаем список индексов с помощью API-интерфейса:

       [elasticsearch@7fab8c1cab18 config]$   curl -X GET 'http://localhost:9200/_cat/indices?v'

       health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
       yellow open   ind-3 9q5YPJj3Q_W9F_ySt4EEig   4   2          0            0       920b           920b
       yellow open   ind-2 5uNM0UDYSRazAnZrO93Yyw   2   1          0            0       460b           460b
       green  open   ind-1 LHhtXTnWSNa7D-p9n-OUWw   1   0          0            0       230b           230b


3) Получаем статус кластера,нод  и  индексов с помощью API-интерфейса:

   - Статус однонодового кластера 

         [elasticsearch@7fab8c1cab18 ~]$ curl http://localhost:9200/_cat/health?v
         epoch      timestamp cluster       status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
         1664861748 05:35:48  netology_test yellow          1         1      7   7    0    0       10             0                  -                 41.2%

             
   - Статус нод кластера
   
         [elasticsearch@7fab8c1cab18 ~]$  curl  http://localhost:9200/_cat/nodes?v
         ip         heap.percent ram.percent cpu load_1m load_5m load_15m node.role master name
         172.18.0.2           19          96   0    0.00    0.00     0.00 mdi       *      7fab8c1cab18
     
   - Статус первого индекса 

         [elasticsearch@7fab8c1cab18 config]$  curl -X GET 'http://localhost:9200/_cluster/health/ind-1?pretty'
   
         {
         "cluster_name" : "netology_test",
         "status" : "green",
         "timed_out" : false,
         "number_of_nodes" : 1,
         "number_of_data_nodes" : 1,
         "active_primary_shards" : 1,
         "active_shards" : 1,
         "relocating_shards" : 0,
         "initializing_shards" : 0,
         "unassigned_shards" : 0,
         "delayed_unassigned_shards" : 0,
         "number_of_pending_tasks" : 0,
         "number_of_in_flight_fetch" : 0,
         "task_max_waiting_in_queue_millis" : 0,
         "active_shards_percent_as_number" : 100.0

         }

   - Статус второго  индекса

         [elasticsearch@7fab8c1cab18 config]$  curl -X GET 'http://localhost:9200/_cluster/health/ind-2?pretty'

         {
         "cluster_name" : "netology_test",
         "status" : "yellow",
         "timed_out" : false,
         "number_of_nodes" : 1,
         "number_of_data_nodes" : 1,
         "active_primary_shards" : 2,
         "active_shards" : 2,
         "relocating_shards" : 0,
         "initializing_shards" : 0,
         "unassigned_shards" : 2,
         "delayed_unassigned_shards" : 0,
         "number_of_pending_tasks" : 0,
         "number_of_in_flight_fetch" : 0,
         "task_max_waiting_in_queue_millis" : 0,
         "active_shards_percent_as_number" : 41.17647058823529
         }

   - Статус третьего индекса 
  
         [elasticsearch@7fab8c1cab18 config]$  curl -X GET 'http://localhost:9200/_cluster/health/ind-3?pretty'
         {
         "cluster_name" : "netology_test",
         "status" : "yellow",
         "timed_out" : false,
         "number_of_nodes" : 1,
         "number_of_data_nodes" : 1,
         "active_primary_shards" : 4,
         "active_shards" : 4,
         "relocating_shards" : 0,
         "initializing_shards" : 0,
         "unassigned_shards" : 8,
         "delayed_unassigned_shards" : 0,
         "number_of_pending_tasks" : 0,
         "number_of_in_flight_fetch" : 0,
         "task_max_waiting_in_queue_millis" : 0,
         "active_shards_percent_as_number" : 41.17647058823529
         }

5) Удаляем индексы с помощью API-интерфейса:

       [elasticsearch@7fab8c1cab18 config]$  curl -X DELETE 'http://localhost:9200/ind-1?pretty' 
       {    
             "acknowledged" : true   
       }

       [elasticsearch@7fab8c1cab18 config]$  curl -X DELETE 'http://localhost:9200/ind-2?pretty' 
       {     
             "acknowledged" : true   
       }

       [elasticsearch@7fab8c1cab18 config]$  curl -X DELETE 'http://localhost:9200/ind-3?pretty' 
       {     
             "acknowledged" : true   
       }

7) Проверяем наличие индексов с помощью API-интерфейса:

       [elasticsearch@7fab8c1cab18 config]$  curl -X GET 'http://localhost:9200/_cat/indices?v'
       health status index uuid pri rep docs.count docs.deleted store.size pri.store.size
     

 2 и 3 индексы  и кластер находятся  в состоянии yellow, поскольку  при создании этих индексов 
 количество запланированных реплик  для обоих индексов больше 1, 
 но в рамках однонодового кластера реплики  не могут быть распределены на соседние ноды.


---
### Задача 3
В данном задании вы научитесь:
создавать бэкапы данных
восстанавливать индексы из бэкапов

- Создайте директорию {путь до корневой директории с elasticsearch в образе}/snapshots.
- Используя API зарегистрируйте данную директорию как snapshot repository c именем netology_backup.
  Приведите в ответе запрос API и результат вызова API для создания репозитория.
- Создайте индекс test с 0 реплик и 1 шардом и приведите в ответе список индексов.
- Создайте snapshot состояния кластера elasticsearch.
- Приведите в ответе список файлов в директории со snapshotами.
- Удалите индекс test и создайте индекс test-2. Приведите в ответе список индексов.
- Восстановите состояние кластера elasticsearch из snapshot, созданного ранее.
- Приведите в ответе запрос к API восстановления и итоговый список индексов.

----
 #### Подсказки:
Возможно вам понадобится доработать elasticsearch.yml в части директивы path.repo и перезапустить elasticsearch

---
### Ответ:

1) Добавляем в файл Dockerfile   следующие строки  для создания снэпшотов внутри кластера

         ...
         RUN mkdir /usr/share/elasticsearch/snapshots &&\
               chown elasticsearch:elasticsearch /usr/share/elasticsearch/snapshots
         RUN mkdir /var/lib/logs \
               && chown elasticsearch:elasticsearch /var/lib/logs \
               && mkdir /var/lib/data \
               && chown elasticsearch:elasticsearch /var/lib/data
         ...

2) Добавляем в файл  elasticsearch.yml следующую строку  и пересобираем docker-образ

          path.repo: ["/usr/share/elasticsearch/snapshots"]

3) Используя API регистрируем данную директорию как snapshot repository c именем netology_backup.
   
         curl "localhost:9200/_snapshot/netology_backup?pretty" -X PUT  -H 'Content-Type: application/json' -d' {  "type": "fs",  "settings": {  "location": "/usr/share/elasticsearch/snapshots"   }  }'
         {
              "acknowledged" : true
         }


4) Чтобы подтвердить успешное создание репозитория снэпшотов, используем запрос GET с конечной точкой _snapshot :
       
        curl -X GET "http://localhost:9200/_snapshot/netology_backup?pretty"
        {
          "netology_backup" : {
            "type" : "fs",
            "settings" : {
              "location" : "/usr/share/elasticsearch/snapshots"
            }
          }
        }

5) Создаем индекс test с 0 реплик и 1 шардом .

        curl -X PUT localhost:9200/test -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
        {
            "acknowledged":true,
            "shards_acknowledged":true,
            "index":"test"
        }

6) Выводим список индексов

        curl -X GET 'http://localhost:9200/_cat/indices?v'
        health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
        green  open   test  w9HVsgDQR7aqgO-x68s2gA   1   0          0            0       230b           230b

7) Проверяем содержимое папки с снэпшотами
 
        ls -la /usr/share/elasticsearch/snapshots

        total 32
        drwxr-xr-x 1 elasticsearch elasticsearch 4096 Oct  4 09:41 .
        drwxrwxr-x 1 elasticsearch root          4096 Oct  4 09:28 ..
        -rw-rw-r-- 1 elasticsearch elasticsearch   29 Oct  4 09:31 incompatible-snapshots
        -rw-rw-r-- 1 elasticsearch elasticsearch  169 Oct  4 09:34 index-2
        -rw-rw-r-- 1 elasticsearch elasticsearch   29 Oct  4 09:41 index-3
        -rw-rw-r-- 1 elasticsearch elasticsearch    8 Oct  4 09:41 index.latest
        drwxrwxr-x 2 elasticsearch elasticsearch 4096 Oct  4 09:41 indices


8) Создаем снэпшот 

        curl -X PUT  "http://localhost:9200/_snapshot/netology_backup/snapshot_1?wait_for_completion=true&pretty"

        {
          "snapshot" : {
            "snapshot" : "snapshot_1",
            "uuid" : "UCAuXTLoTV2bQHA0wf4VGg",
            "version_id" : 7000099,
            "version" : "7.0.0",
            "indices" : [
              "test"
            ],
            "include_global_state" : true,
            "state" : "SUCCESS",
            "start_time" : "2022-10-04T09:46:25.031Z",
            "start_time_in_millis" : 1664876785031,
            "end_time" : "2022-10-04T09:46:25.090Z",
            "end_time_in_millis" : 1664876785090,
            "duration_in_millis" : 59,
            "failures" : [ ],
            "shards" : {
              "total" : 1,
              "failed" : 0,
              "successful" : 1
            }
          }
       }

9) Повторно проверяем содержимое папки с снэпшотами
 
       ls -la /usr/share/elasticsearch/snapshots

       total 60
       drwxr-xr-x 1 elasticsearch elasticsearch  4096 Oct  4 09:46 .
       drwxrwxr-x 1 elasticsearch root           4096 Oct  4 09:28 ..
       -rw-rw-r-- 1 elasticsearch elasticsearch    29 Oct  4 09:31 incompatible-snapshots
       -rw-rw-r-- 1 elasticsearch elasticsearch    29 Oct  4 09:41 index-3
       -rw-rw-r-- 1 elasticsearch elasticsearch   169 Oct  4 09:46 index-4
       -rw-rw-r-- 1 elasticsearch elasticsearch     8 Oct  4 09:46 index.latest
       drwxrwxr-x 3 elasticsearch elasticsearch  4096 Oct  4 09:46 indices
       -rw-rw-r-- 1 elasticsearch elasticsearch 21192 Oct  4 09:46 meta-UCAuXTLoTV2bQHA0wf4VGg.dat
       -rw-rw-r-- 1 elasticsearch elasticsearch   241 Oct  4 09:46 snap-UCAuXTLoTV2bQHA0wf4VGg.dat
  

10) Удаляем индекс test        

        curl -X DELETE "localhost:9200/test?pretty"
        {
            "acknowledged" : true
        }

11) Создаем индекс test-2    

        curl -X PUT localhost:9200/test-2 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
        {   
             "acknowledged":true,
             "shards_acknowledged":true,
             "index":"test-2"
        }

12) Выводим список индексов

        curl -X GET 'http://localhost:9200/_cat/indices?v'
        health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
        green  open   test-2 y0p9ufxRQ_iahcEsVNcVcg   1   0          0            0       230b           230b


13) Восставливаем снэпшот

        curl -X POST "localhost:9200/_snapshot/netology_backup/snapshot_1/_restore?pretty"
        {
              "accepted" : true
        }

14) Выводим список индексов после восстановления снэпшота

        curl -X GET 'http://localhost:9200/_cat/indices?v'
        health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
        green  open   test-2 y0p9ufxRQ_iahcEsVNcVcg   1   0          0            0       283b           283b
        green  open   test   91GvX-BOR9-LFks-U6THkw   1   0          0            0       283b           283b

15) Удаляем снэпшот 

        curl -X DELETE "localhost:9200/_snapshot/netology_backup/snapshot_1?pretty"


