## Домашнее задание к занятию "7.2. Облачные провайдеры и синтаксис Terraform."

Зачастую разбираться в новых инструментах гораздо интересней понимая то, как они работают изнутри. 
Поэтому в рамках первого необязательного задания предлагается завести 
свою учетную запись в AWS (Amazon Web Services) или Yandex.Cloud. 
Идеально будет познакомиться с обоими облаками, потому что они отличаются.

---
### Задача 1 

#### Вариант с AWS. 
Регистрация в aws и знакомство с основами (необязательно, но крайне желательно).

[https://aws.amazon.com/ru/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all]

Остальные задания можно будет выполнять и без этого аккаунта, но с ним можно будет увидеть полный цикл процессов.

AWS предоставляет достаточно много бесплатных ресурсов в первый год после регистрации, подробно описано здесь.

Создайте аккаут aws.
Установите c aws-cli 
[https://aws.amazon.com/cli/ ]
Выполните первичную настройку aws-sli 
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html.
Создайте IAM политику для терраформа c правами
AmazonEC2FullAccess
AmazonS3FullAccess
AmazonDynamoDBFullAccess
AmazonRDSFullAccess
CloudWatchFullAccess
IAMFullAccess
Добавьте переменные окружения
export AWS_ACCESS_KEY_ID=(your access key id)
export AWS_SECRET_ACCESS_KEY=(your secret access key)
Создайте, остановите и удалите ec2 инстанс (любой с пометкой free tier) через веб интерфейс.
В виде результата задания приложите вывод команды aws configure list.

#### Вариант с Yandex.Cloud. 

Регистрация в ЯО и знакомство с основами (необязательно, но крайне желательно).
Подробная инструкция на русском языке содержится здесь - 
[https://cloud.yandex.ru/docs/tutorials/infrastructure-management/terraform-quickstart]
- Обратите внимание на период бесплатного использования после регистрации аккаунта.
- Используйте раздел "Подготовьте облако к работе" для регистрации аккаунта. 
- Далее раздел "Настройте провайдер" для подготовки базового терраформ конфига.
- Воспользуйтесь инструкцией на сайте терраформа, что бы не указывать авторизационный токен в коде, 
  а терраформ провайдер брал его из переменных окружений.


---
### Задача 2. Создание aws ec2 или yandex_compute_instance через терраформ.

1) В каталоге terraform вашего основного репозитория, который был создан в начале курса, создайте файл main.tf и versions.tf.
2) Зарегистрируйте провайдер 
      1) для aws
         - В файл main.tf добавьте блок provider,а в versions.tf блок terraform с вложенным блоком required_providers. 
         - Укажите любой выбранный вами регион внутри блока provider.
     2)  Либо для yandex.cloud.
     [ https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs ]

     Подробную инструкцию можно найти здесь.
     [ https://cloud.yandex.ru/docs/solutions/infrastructure-management/terraform-quickstart ]

Внимание! В гит репозиторий нельзя пушить ваши личные ключи доступа к аккаунту. 
Поэтому в предыдущем задании мы указывали их в виде переменных окружения.
4) В файле main.tf воспользуйтесь блоком data "aws_ami для поиска ami образа последнего Ubuntu.
5) В файле main.tf создайте рессурс 
      - либо ec2 instance.
        [https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance]
        Постарайтесь указать как можно больше параметров для его определения. Минимальный набор параметров 
        указан в первом блоке Example Usage, но желательно, указать большее количество параметров.
   
      - либо yandex_compute_image.
        [https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs/resources/compute_image]
   
6) Также в случае использования aws:
    Добавьте data-блоки aws_caller_identity и aws_region.
    В файл outputs.tf поместить блоки output с данными об используемых в данный момент:
   - AWS account ID,
   - AWS user ID,
   - AWS регион, который используется в данный момент,
   - Приватный IP ec2 инстансы,
   - Идентификатор подсети в которой создан инстанс.
   
7) Если вы выполнили первый пункт, то добейтесь того, что бы команда terraform plan выполнялась без ошибок.

В качестве результата задания предоставьте:
Ответ на вопрос: при помощи какого инструмента (из разобранных на прошлом занятии) можно создать свой образ ami?
Ссылку на репозиторий с исходной конфигурацией терраформа.

