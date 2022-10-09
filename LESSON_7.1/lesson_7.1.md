## Домашнее задание к занятию "7.1. Инфраструктура как код"

---
### Задача 1. Выбор инструментов.
Легенда
Через час совещание на котором менеджер расскажет о новом проекте. 
Начать работу над которым надо будет уже сегодня. 
На данный момент известно, что это будет сервис, который ваша компания будет предоставлять внешним заказчикам. 
Первое время, скорее всего, будет один внешний клиент, со временем внешних клиентов станет больше.
Так же по разговорам в компании есть вероятность, что техническое задание еще не четкое, 
что приведет к большому количеству небольших релизов, тестирований интеграций, откатов, доработок, то есть скучно не будет.

Вам, как девопс инженеру, будет необходимо принять решение об инструментах для организации инфраструктуры. 
На данный момент в вашей компании уже используются следующие инструменты:

- остатки Сloud Formation,
- некоторые образы сделаны при помощи Packer,
- год назад начали активно использовать Terraform,
- разработчики привыкли использовать Docker,
- уже есть большая база Kubernetes конфигураций,
- для автоматизации процессов используется Teamcity,
- также есть совсем немного Ansible скриптов,
- и ряд bash скриптов для упрощения рутинных задач.

Для этого в рамках совещания надо будет выяснить подробности о проекте, что бы в итоге определиться с инструментами:
- Какой тип инфраструктуры будем использовать для этого проекта: изменяемый или не изменяемый?
- Будет ли центральный сервер для управления инфраструктурой?
- Будут ли агенты на серверах?
- Будут ли использованы средства для управления конфигурацией или инициализации ресурсов?
- В связи с тем, что проект стартует уже сегодня, в рамках совещания надо будет определиться со всеми этими вопросами.

В результате задачи необходимо:
- Ответить на четыре вопроса представленных в разделе "Легенда".
Какие инструменты из уже используемых вы хотели бы использовать для нового проекта?
Хотите ли рассмотреть возможность внедрения новых инструментов для этого проекта?
Если для ответа на эти вопросы недостаточно информации, то напишите какие моменты уточните на совещании.

---
### Ответ:



---
### Задача 2. Установка терраформ.
Официальный сайт: https://www.terraform.io/

Установите терраформ при помощи менеджера пакетов используемого в вашей операционной системе. 
В виде результата этой задачи приложите вывод команды terraform --version.

---
### Ответ:

- Находим  версию 1.2.9 и скачиваем ее c зеркала Yandex-Cloud

      root@docker:/home/bes/# wget  https://hashicorp-releases.yandexcloud.net/terraform/1.2.9/terraform_1.2.9_linux_amd64.zip

- Распаковываем и устанавливаем: 

      root@docker:/home/bes/#  unzip terraform_1.2.9_linux_amd64.zip  && rm terraform_1.2.9_linux_amd64.zip
      root@docker:/home/bes/#  mv  terraform  /usr/bin

- Проверяем установку

      root@docker:/home/bes/#  terraform --version
      Terraform v1.2.9
      on linux_amd64

      Your version of Terraform is out of date! The latest version
      is 1.3.2. You can update by downloading from https://www.terraform.io/downloads.html


---
### Задача 3. Поддержка легаси кода.
В какой-то момент вы обновили терраформ до новой версии, например с 0.12 до 0.13. 
А код одного из проектов настолько устарел, что не может работать с версией 0.13. 
В связи с этим необходимо сделать так, чтобы вы могли одновременно использовать последнюю версию терраформа установленную 
при помощи штатного менеджера пакетов и устаревшую версию 0.12.

В виде результата этой задачи приложите вывод --version двух версий терраформа доступных на вашем компьютере или виртуальной машине.

---
### Ответ:

Вариант 1

- Переносим в личный рабочий каталог старую версию terraform 12

      root@docker:/usr#   cd  &&  mkdir $HOME/.local/bin
      root@docker:#   PATH=$PATH:$HOME/.local/bin 
      root@docker:#   export PATH
      root@docker:# mv  terraform  /$HOME/.local/bin/tf12

- Находим свежую версию 1.3.2 и скачиваем ее c зеркала Yandex-Cloud 

      root@docker:/home/bes/# wget  https://hashicorp-releases.yandexcloud.net/terraform/1.3.2/terraform_1.3.2_linux_amd64.zip

- Распаковываем и устанавливаем: 

      root@docker:/home/bes/# unzip terraform_1.3.2_linux_amd64.zip  && rm terraform_1.3.2_linux_amd64.zip
      root@docker:/home/bes/# mv  terraform  /usr/bin

- Проверяем обе версии:
 
      Старая версия:

      root@docker:~# whereis  tf12
      tf12: /root/.local/bin/tf12

      root@docker:~# tf12 --version | grep v1
      Terraform v1.2.9

      Новая версия:

      root@docker:~# whereis  terraform
      terraform: /usr/bin/terraform

      root@docker:~# terraform --version
      Terraform v1.3.2
      on linux_amd64

Вариант 2

1) Установка приложения tfswitch с помощью  curl 

       root@docker:~# curl -L https://raw.githubusercontent.com/warrensbox/terraform-switcher/release/install.sh | bash
       % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
       100  9216  100  9216    0     0  21333      0 --:--:-- --:--:-- --:--:-- 21284
       warrensbox/terraform-switcher info checking GitHub for latest tag
       warrensbox/terraform-switcher info found version: 0.13.1288 for 0.13.1288/linux/amd64
       warrensbox/terraform-switcher info installed /usr/local/bin/tfswitch

 2) Выбираем и загружаем версии для использования  в каталог  /root/.terraform.versions ,указывая доступное  в Росси зеркало-репозиторий Yandex Cloud

        root@docker:~# tfswitch  -s 1.2.9 --mirror  https://hashicorp-releases.yandexcloud.net/terraform/  
        root@docker:~# tfswitch  -s 1.3.2 --mirror  https://hashicorp-releases.yandexcloud.net/terraform/  

 3) Запускаем tfswitch , указывая ту версию, которая в текущий момент необходима

        root@docker:~# tfswitch   1.2.9
        Switched terraform to version "1.2.9"

 4) Можно создать  файл в рабочем каталоге tfswitchrc , в котором указана желаемая версия

        root@docker:~#  echo "1.2.9" >> .tfswitchrc 

 5) Запускаем  tfswitch  заново  без аргументов - конфигурация будет считана из файла  .tfswitchrc . 

        root@docker:~/terraform-switcher-0.13.1288# tfswitch
        Reading file .tfswitchrc
        Switched terraform to version "1.2.9"

