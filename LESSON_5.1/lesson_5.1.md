# Домашнее задание к занятию "5.1. Введение в виртуализацию. Типы и функции гипервизоров. Обзор рынка вендоров и областей применения."

-------------------------------------------------------------------------------------------------------------------------

## Задача 1
Опишите кратко, как вы поняли: в чем основное отличие полной (аппаратной) виртуализации, паравиртуализации 
и виртуализации на основе ОС.

## Ответ:
- При аппаратной виртуализации в слое гипервизора присутствует набор виртуальных устройств, с которыми работает гостевая ОС. 
  Тип гостевой ОС не зависит от ОС гипервизора потому, что виртуальные машины запускают свою собственную копию ОС 
  и приложений на виртуализированном оборудовании.
  При полной виртуализации немодифицированная ОС работает так же, как если бы она не была виртуализирована, 
  вызовы ОС перехватываются и транслируются с использованием двоичного преобразования.
  Гостевые машины полностью изолированы друг от друга и от ОС сервера
  (изоляция на уровне файловой системы, процессов, переменных sysctl) 
  Гостевые машины также полностью изолированы в нагрузке на железо.

- При паравиртуализации тип гостевой ОС не зависит от ОС гипервизора.
  Гостевые операционные системы подготавливаются для исполнения в виртуализированной среде, 
  для чего их ядро незначительно модифицируется. 
  Паравиртуализация, таким образом, обязательно требует изменения кода гостевой ОС для работы в гипервизоре.
  Гостевая ОС взаимодействует с программой гипервизора, который предоставляет ей гостевой API, 
  вместо использования напрямую аппаратных ресурсов физического сервера.  
  При паравиртуализации гостевая ОС знает, что она виртуализируется.
  Экземпляры гостевых машин полностью изолированы друг от друга и от ОС сервера.
 
- Виртуализация на уровне ОС (контейнеризация) позволяет виртуализировать серверы в виде контейнеров - исполняемых процессов 
  на уровне ядра операционной системы. 
  Тип ОС виртуальных машин соответствует типу ОС гипервизора. 
  Хотя между контейнерами и хостовой ОС присутствует слой виртуализации ОС,
  у гостевых машин нет полной изоляции в нагрузке на железо. 
  Но при этом нагрузка на железо (CPU, RAM) может ограничиваться.


-------------------------------------------------------------------------------------------------------------------------

## Задача 2
 Выберите один из вариантов использования организации физических серверов, в зависимости от условий использования.
 Организация серверов: - физические сервера, - паравиртуализация,- виртуализация уровня ОС.
 Условия использования:
 Высоконагруженная база данных, чувствительная к отказу.
 Различные web-приложения.
 Windows системы для использования бухгалтерским отделом.
 Системы, выполняющие высокопроизводительные расчеты на GPU.
 Опишите, почему вы выбрали к каждому целевому использованию такую организацию.

## Ответ:

      1) Высоконагруженная база данных, чувствительная к отказу.

      Аппаратная виртуализация. 
          Ключевое требование - исключительная стабильность  и жесткое выделение ресурсов гипервизора  для гостевой  машины.
          - При наличии денег у предприятия  -  VMWARE VSphere + VSphere Server с  High Availability. Обязательны снэпшоты.
          - При отсутствии денег у предприятия  - XEN ( форк Centos) 
              Если размещение БД спланировано в гостевой ОС POSIX-типа   - профиль с XEN HVM.
              Если размещение БД спланировано в гостевой ОС Windows-типа - профиль с XEN PV ( Лучше совместим с Windows) .      

      2) Различные web-приложения.

      Виртуализация на уровне ОС (контейнеризация). 
         Использовать DOCKER-образ  одной из POSIX-совместимых ОС  с мониторингом каждогого экземпляра dockera.
         В роли оркестратора - использовать Docker Swarm или Kubernetis (в зависимости от машстаба предприятия).
         Причины:
            1) Высокая степень унификации рабочего профиля виртуальных  машин ( NGINX или APACHE).
            2) Обеспечение легкости масштабирования из-за высокой вероятности массового роста количества WEB-сервисов 
               и роста требований к их производительности. 

      3) Windows системы для использования бухгалтерским отделом.

      Аппаратная виртуализация или паравиртуализация. 
         Ключевые требования:
         - Полная изоляция и безопасность хранения бухгалтерских данных внутри гостевой машины от гипервизора,
           управляемого как другим отделом ИТ, так и аутсорсерами и облачными сервисами.  
         - Возможности безболезненно пробросить  физические USB-токены с ключами внутрь 
           гостевых виртуалок бухгалтеров.
        Рекомендую  VMWARE VSphere  если не хотим выноса мозга бухгалтерами.
           При наличии денег у предприятия  -  использовать VMWARE VSphere. 
           При отсутствии денег у предприятия  - использовать  VMWARE ESXi. 
        При наличии аппаратной ключницы  USB Anywhere (и подобных) возможно  использование  Proxmox Virtual Environment + KVM .

      4) Системы, выполняющие высокопроизводительные расчеты на GPU 
       
        -  При отсутствии денег у предприятия ( SOHO )  - использовать  только физические сервера.
        -  При наличии денег у предприятия  -  Аппаратная виртуализация.
               Причины выбора :              
               Отсутствие необходимости модификации гостевой ОС и проброс ресурсов GPU прямо внутрь виртуалки.
               Распределение затрат на покупку GPU за счет агрегации  нескольких рабочих мест на одном сервере.
               Возможность гибко настроить несколько рабочих профилей нагрузки на каждый GPU 
               в зависимости от роли сотрудника в организации. 
               Рекомендую использовать  VMWARE Sphere + Horizon.  Отсутствие ограничений на тип гостевой ОС. 
               Наиболее продвинутая технология использования виртуальных машин совместно с GPU - VMWARE Horizon. 
  
----------------------------------------------------------------------------------------------------------

## Задача 3
Выберите подходящую систему управления виртуализацией для предложенного сценария. Детально опишите ваш выбор.

Сценарии:

Сценарий_1 100 виртуальных машин на базе Linux и Windows, общие задачи, нет особых требований. 
Преимущественно Windows based инфраструктура, требуется реализация программных балансировщиков нагрузки, 
репликации данных и автоматизированного механизма создания резервных копий.

Сценарий_2 Требуется наиболее производительное бесплатное open source решение для виртуализации небольшой (20-30 серверов) 
инфраструктуры на базе Linux и Windows виртуальных машин.

Сценарий_3 Необходимо бесплатное, максимально совместимое и производительное решение для виртуализации Windows инфраструктуры.
Необходимо рабочее окружение для тестирования программного продукта на нескольких дистрибутивах Linux.


## Ответ:

### Сценарий 1

    Выбор:  HYPER-V кластер на базе гипервизоров с ОС Windows 2019 Datacenter
            (при условии отсутствия в списке гостевых ОС, являющихся форками BSD).

        - В данном гипервизоре имеется HYPER-V Failover Cluster - теневая репликация копий 
          с двумя режимами восстановления работоспособности - Quick Migration и Live Migration.
        - Есть встроенная система снэпшотов гостевых машин.   
        - Присутствует программный балансировщик нагрузки от Windows,
          анализирующий два параметра - 
          а) Память — наиболее распространенное ограничение ресурсов на узле Hyper-V.
          б) Загрузка ЦП .

### Сценарий 2 

    Выбор:   Proxmox Virtual Environment + KVM

        Бесплатное open source решение.
        Гипервизор KVM - самый  производительный гипервизор.
        Низкий порог входа с точки зрения квалификации сисадмина такой маленькой организации. 
        Поддержка всех типов виртуальных машин .
        Обязательно создание нескольких кластеров, если есть несколько типов профилей нагрузки.  
    

### Сценарий 3 

    Выбор :     XEN

        Бесплатное open source решение.
        XEN - универсальный гипервизор, максимально совместимый . 
        Благодаря профилям рабочей нагрузки отсутствует вероятность "noisy neighbour".
        Поскольку требуется поддержка двух типов ОС - Windows и Linux,
        Если гостевая ОС POSIX-типа   - создаем профиль с XEN HVM.
        Если гостевая ОС Windows-типа - создаем профиль с XEN PV ( Лучше совместим с Windows).
        Выбор между KVM и XEN сделан в пользу XEN исходя из следующих предпосылок: 
        - Влияние работы высокостабильного гипервизора исключается из списка факторов, влиящих на устойчивость тестовых виртуалок.
        - Не рекомендуется тестовые витуалки запускать в  гипервизоре, использующем паравиртуализацию ( KVM),
          поскольку нет полной изоляции железа и влияния соседей.      




-------------------------------------------------------------------------------------------------------------
## Задача 4
Опишите возможные проблемы и недостатки гетерогенной среды виртуализации (использования нескольких систем управления 
виртуализации одновременно) и что необходимо сделать для минимизации этих рисков и проблем. 
Если бы у вас был выбор, то создавали бы вы гетерогенную среду или нет? Мотивируйте ваш ответ примерами.

## Ответ:
Я не рекомендую создавать гетерогенную среду виртуализации.
Причины:
- Отсутствие возможности миграции налету между географически или логически разделенными кластерами сред виртуализации разных типов.  

- При постановке от бизнеса задачи отказа от одной из систем управления  гетерогенной среды с разными вендорами 
  потребуется воссоздать рабочее окружение и выполнить перенос виртуальных машин на среду виртуализации другого типа.
  Это чревато возникновением целого ряда проблем:
   - Длительный простой на время конвертации при переносе сервисов, особенно при огромных объемах виртуальных машин.
   - Возможное полное отсутствие приложений для процедуры конвертации исполняемого образа гостевой виртуальной машины 
     в образ нового гипервизора или универсальный образ, независимый от гипервизора.
   - Отсутствие поддержки виртуальных драйверов, предлагаемых новым гипервизором, для ОС системы переносимой гостевой виртуалки.
   - Возможно критичное снижение скорости работы бизнес-приложений, в силу отсутствия предварительного тестирования 
     работы сервисов на гипервизоре другого типа и, как следствие, необходимость переписывать ПО гостевой виртуальной машины.

- При настройке систем мониторинга нагрузки на общедоступные аппаратные ресурсы (CPU, RAM, СХД ) со стороны гетерогенных сред 
  сложно установить цельную картину нагрузки в силу необходимости использования разных подходов к параметрам мониторинга у разных решений.
  На эффективность мониторинга влияет принципиально разный способ получения показателей:
    - в системах с паравиртуализацией  показатели искажаются  из-за наличия промежуточного слоя между гостевой ВМ и железом в виде гостевой API. 
    - в системах с контейнеризацией  показатели искажаются  из-за принципа совместного использования ресурсов, доступных ядру хостовой ОС.
    - в системах с аппаратной виртуализацией - практически адекватная оценка нагрузки виртуалки на аппаратные ресурсы.

  Где нет мониторинга (обратной связи)- там нет управляемости.

- Высокая ТСО - совокупная стоимость владения (включая стоимость технической поддержки).
  Необходимость для технического персонала обладать глубокими навыками эксплуатации разных типов сред виртуализации. 

-------------------------------------------------------------------------------------------------------------

