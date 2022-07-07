Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

1) Работа c HTTP через телнет.
   Подключитесь утилитой телнет к сайту stackoverflow.com telnet stackoverflow.com 80
   отправьте HTTP запрос

         GET /questions HTTP/1.0
         HOST: stackoverflow.com
         [press enter]
         [press enter]
   В ответе укажите полученный HTTP код, что он означает?



Ответ:  

       root@vagrant:/home/vagrant# telnet stackoverflow.com 80
       Trying 151.101.129.69...
       Connected to stackoverflow.com.
       Escape character is '^]'.
       GET /questions HTTP/1.0
       HOST: stackoverflow.com
   
       HTTP/1.1 301 Moved Permanently
       cache-control: no-cache, no-store, must-revalidate
       location: https://stackoverflow.com/questions
       x-request-guid: 75e5605b-e09c-4df2-836d-cf37bb44e099
       feature-policy: microphone 'none'; speaker 'none'
       content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
       Accept-Ranges: bytes
       Date: Thu, 07 Jul 2022 16:34:33 GMT
       Via: 1.1 varnish
       Connection: close
       X-Served-By: cache-fra19160-FRA
       X-Cache: MISS
       X-Cache-Hits: 0
       X-Timer: S1657211673.482238,VS0,VE93
       Vary: Fastly-SSL
       X-DNS-Prefetch-Control: off
       Set-Cookie: prov=8b76cd94-af96-df13-00d3-2c3be7619fd1; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly
   
       Connection closed by foreign host.


   Произошло соединение с сервером stackoverflow.com. Был отправлен запрос на открытие страницы  http://stackoverflow.com/questions.
   Но удаленный сервер ответил ошибкой 301. 
   Код состояния HTTP 301. Moved Permanently — стандартный код ответа HTTP, получаемый в ответ от сервера в ситуации, 
   когда запрошенный ресурс был на постоянной основе перемещён в новое месторасположение.
   Затем сервер сообщил, что данная страница доступна только через подключение по протоколу https и закрыл соединение.

2) Повторите задание 1 в браузере, используя консоль разработчика F12.
   откройте вкладку Network
   отправьте запрос http://stackoverflow.com
   найдите первый ответ HTTP сервера, откройте вкладку Headers
   укажите в ответе полученный HTTP код.
   проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?
   приложите скриншот консоли браузера в ответ.

Ответ :

      Первый ответ HTTP сервера 
      stackoverflow.com
 
      Заголовки:
 
      Общие :

      URL запроса: http://stackoverflow.com/
      Метод запроса: GET
      Код статуса: 307 Internal Redirect
      Правило для URL перехода: strict-origin-when-cross-origin
    
      Заголовки ответов:
    
      Cross-Origin-Resource-Policy: Cross-Origin
      Cross-Origin-Resource-Policy: Cross-Origin
      Location: https://stackoverflow.com/
      Non-Authoritative-Reason: HSTS
 
      Заголовки запросов:
 
      Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
      Upgrade-Insecure-Requests: 1
      User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36





3) Какой IP адрес у вас в интернете?
   

4) Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой whois

  
5) Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой traceroute


6) Повторите задание 5 в утилите mtr. На каком участке наибольшая задержка - delay?


7) Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой dig


8) Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой dig











Как сдавать задания
Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в Google Docs и отправить в личном кабинете на проверку ссылку на ваш документ. Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

Как предоставить доступ к файлам и папкам на Google Диске

Как запустить chrome в режиме инкогнито

Как запустить Safari в режиме инкогнито