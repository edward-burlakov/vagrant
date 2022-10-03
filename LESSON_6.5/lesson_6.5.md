## Домашнее задание к занятию "6.5. Elasticsearch"

---
### Задача 1
В этом задании вы потренируетесь в:
- Установке elasticsearch
- Первоначальном конфигурировании elastcisearch
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

---
### Ответ:

       1)  Запускаем однонодовый кластер Elasticsearch
       root@docker:/home/bes# docker network create elknetwork
       root@docker:/home/bes#   docker run -d --name netology_test  -v $(pwd)/elkconfig:/usr/share/elasticsearch/config --net elknetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.0.0

       2) Развертываем Kibana
       
          root@docker:/home/bes#   docker pull kibana:7.0.0
          root@docker:/home/bes#   docker run --name kibana --net elknetwork -p 5601:5601 kibana:7.0.0

       3) Входим внутрь контейнера
   
          root@docker:/home/bes#  docker exec -it beff9542333d /bin/bash

       4) Проверяем работу сервиcа . Выполним к нему простой запрос о его статусе.

         [root@beff9542333delasticsearch]# curl 127.0.0.1:9200
            {
              "name" : "beff9542333d",
              "cluster_name" : "docker-cluster",
              "cluster_uuid" : "gvtb-gTUSk-i7CqBrkKwtA",
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


----
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


---
### Задача 2
В этом задании вы научитесь:

- Создавать и удалять индексы
- Изучать состояние кластера
- Обосновывать причину деградации доступности данных

1) Ознакомьтесь с документацией и добавьте в elasticsearch 3 индекса, в соответствии со таблицей:

| Имя	    | Количество реплик | Количество шард  |
|-----------|-------------------|------------------|-
| ind-1     | 0                 | 1                |
| ind-2  	| 1                 | 2                |
| ind-3	    | 2                 | 4                |

2) Получите список индексов и их статусов, используя API и приведите в ответе на задание.
3) Получите состояние кластера elasticsearch, используя API.
4) Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

- Удалите все индексы.

Важно
При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард, 
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

---
### Ответ:

            1) Создаем индексы с помощью API-интерфейса:

            [root@beff9542333delasticsearch]#   curl -X PUT localhost:9200/ind-1 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
                   {"acknowledged":true,"shards_acknowledged":true,"index":"ind-1"}
            [root@beff9542333d elasticsearch]# curl -X PUT localhost:9200/ind-2 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 2,  "number_of_replicas": 1 }}'
                   {"acknowledged":true,"shards_acknowledged":true,"index":"ind-2"}
            [root@beff9542333d elasticsearch]# curl -X PUT localhost:9200/ind-3 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 4,  "number_of_replicas": 2 }}'
                   {"acknowledged":true,"shards_acknowledged":true,"index":"ind-3"}

             2) Получаем список индексов:

             [root@beff9542333d elasticsearch]# curl -X GET 'http://localhost:9200/_cat/indices?v'
             health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
             yellow open   ind-2 ZY2oN0jtTUqpDoOQ07_guA   2   1          0            0       460b           460b
             green  open   ind-1 YkmstG24TxKM0QaMwtRS0w   1   0          0            0       283b           283b
             yellow open   ind-3 t6imTK8ATOWzlncJbd2-2g   4   2          0            0       920b           920b

            3) Получаем статус индексов:

- Статус первого индекса 

             [root@beff9542333delasticsearch]# curl -X GET 'http://localhost:9200/_cluster/health/ind-1?pretty'
   
             {
             "cluster_name" : "docker-cluster",
             "status" : "red",
             "timed_out" : true,
             "number_of_nodes" : 1,
             "number_of_data_nodes" : 1,
             "active_primary_shards" : 0,
             "active_shards" : 0,
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

            [root@beff9542333d elasticsearch]# curl -X GET 'http://localhost:9200/_cluster/health/ind-2?pretty'

            {
            "cluster_name" : "docker-cluster",
            "status" : "red",
            "timed_out" : true,
            "number_of_nodes" : 1,
            "number_of_data_nodes" : 1,
            "active_primary_shards" : 0,
            "active_shards" : 0,
            "relocating_shards" : 0,
            "initializing_shards" : 0,
            "unassigned_shards" : 0,
            "delayed_unassigned_shards" : 0,
            "number_of_pending_tasks" : 0,
            "number_of_in_flight_fetch" : 0,
            "task_max_waiting_in_queue_millis" : 0,
            "active_shards_percent_as_number" : 100.0
            }

- Статус третьего индекса 
  
        [root@beff9542333d elasticsearch]# curl -X GET 'http://localhost:9200/_cluster/health/ind-3?pretty'
        {
          "cluster_name" : "docker-cluster",
          "status" : "red",
          "timed_out" : true,
          "number_of_nodes" : 1,
          "number_of_data_nodes" : 1,
          "active_primary_shards" : 0,
          "active_shards" : 0,
          "relocating_shards" : 0,
          "initializing_shards" : 0,
          "unassigned_shards" : 0,
          "delayed_unassigned_shards" : 0,
          "number_of_pending_tasks" : 0,
          "number_of_in_flight_fetch" : 0,
          "task_max_waiting_in_queue_millis" : 0,
          "active_shards_percent_as_number" : 100.0
        }























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


