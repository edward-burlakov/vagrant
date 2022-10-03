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
   
        RUN mkdir /usr/share/elasticsearch/snapshots &&\
        chown elasticsearch:elasticsearch /usr/share/elasticsearch/snapshots

        RUN mkdir /var/lib/logs \
        && chown elasticsearch:elasticsearch /var/lib/logs \
        && mkdir /var/lib/data \
        && chown elasticsearch:elasticsearch /var/lib/data
       
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


5) Запускаем задачу сборки образа  


6) Запускаем однонодовый кластер Elasticsearch

       root@docker:/home/bes#  docker network create elknetwork
       root@docker:/home/bes#  docker run -d --name netology_test  --net elknetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.0.0

7) Развертываем Kibana
       
       root@docker:/home/bes#   docker pull kibana:7.0.0
       root@docker:/home/bes#   docker run --name kibana --net elknetwork -p 5601:5601 kibana:7.0.0

8) Входим внутрь контейнера
   
       root@docker:/home/bes#  docker exec -it 7fab8c1cab18 /bin/bash

9) Проверяем работу сервиcа. Выполним к нему простой запрос о его статусе с помощью API-интерфейса:.

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

Важно
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

2) Получаем список индексов с помощью API-интерфейса::

       [elasticsearch@7fab8c1cab18 config]$   curl -X GET 'http://localhost:9200/_cat/indices?v'

       health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
       yellow open   ind-3 9q5YPJj3Q_W9F_ySt4EEig   4   2          0            0       920b           920b
       yellow open   ind-2 5uNM0UDYSRazAnZrO93Yyw   2   1          0            0       460b           460b
       green  open   ind-1 LHhtXTnWSNa7D-p9n-OUWw   1   0          0            0       230b           230b


3) Получаем статус индексов с помощью API-интерфейса::

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

       2 и 3 индексы  и кластер находятся  в состоянии yellow поскольку количество активных шардов на них приближается к 50% .


---
### Задача 3
В данном задании вы научитесь:
создавать бэкапы данных
восстанавливать индексы из бэкапов

- Создайте директорию {путь до корневой директории с elasticsearch в образе}/snapshots.
- Используя API зарегистрируйте данную директорию как snapshot repository c именем netology_backup.
- Приведите в ответе запрос API и результат вызова API для создания репозитория.
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


