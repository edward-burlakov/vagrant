## Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

---
### 1) Работа c HTTP через телнет.
   - Подключитесь утилитой телнет к сайту stackoverflow.com telnet stackoverflow.com 80
   - отправьте HTTP запрос

         GET /questions HTTP/1.0
         HOST: stackoverflow.com
         [press enter]
         [press enter]
   В ответе укажите полученный HTTP код, что он означает?

---
### Ответ:  

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


    Произошло соединение с сервером stackoverflow.com. 
    Был отправлен запрос на открытие страницы  http://stackoverflow.com/questions.
    Удаленный сервер ответил ошибкой 301.  

    Код состояния HTTP 301. Moved Permanently — стандартный код ответа HTTP, получаемый в ответ от сервера в ситуации, 
    когда запрошенный ресурс был на постоянной основе перемещён в новое месторасположение.
 
    Затем сервер сообщил, что данная страница доступна только через подключение по протоколу https и закрыл соединение.


---
### 2) Повторите задание 1 в браузере, используя консоль разработчика F12. Откройте вкладку Network
   - Отправьте запрос http://stackoverflow.com
   - Найдите первый ответ HTTP сервера, откройте вкладку Headers
   - Укажите в ответе полученный HTTP код.
   - Проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?
   - Приложите скриншот консоли браузера в ответ.

---
### Ответ :

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


     Дольше всего обрабатывается  "Waiting for server response" -  176,05 мс

     Скрин консоли  Google Chrome:
    
       https://github.com/edward-burlakov/vagrant/blob/main/LESSON_3.6/Browser%20console.jpg

---
### 3) Какой IP адрес у вас в интернете?

---
### Ответ:

       https://github.com/edward-burlakov/vagrant/blob/main/LESSON_3.6/My_ip.jpg


---
### 4) Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой whois


---
### Ответ:  

       ...
       descr:          OJSC "Sibirtelecom"
       ...
       origin:         AS12389
       ...
       Information related to '212.20.0.0/18AS12389'
       ... 
  
---
### 5) Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой traceroute
    
---
### Ответ:
  
      Автономные системы указаны в квадратных скобках :

      [root@issabel1 ~]# traceroute -Ad 8.8.8.8
      traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
      1  gateway (192.168.1.1) [*]  0.308 ms  0.286 ms  0.218 ms
      2  100.82.0.1 (100.82.0.1) [*]  2.803 ms  2.826 ms  2.823 ms
      3  213.228.109.138 (213.228.109.138) [AS12389]  2.937 ms 213.228.109.146 (213.228.109.146) [AS12389]  3.013 ms  2.922 ms
      4  185.140.148.155 (185.140.148.155) [AS12389]  43.914 ms * *
      5  72.14.205.132 (72.14.205.132) [AS15169]  44.943 ms  44.932 ms  44.890 ms
      6  * * *
      7  66.249.95.40 (66.249.95.40) [AS15169]  41.292 ms 108.170.227.90 (108.170.227.90) [AS15169]  43.333 ms 108.170.250.33 (108.170.250.33) [AS15169]  44.263 ms
      8  108.170.250.146 (108.170.250.146) [AS15169]  43.194 ms 108.170.250.66 (108.170.250.66) [AS15169]  43.700 ms 108.170.250.83 (108.170.250.83) [AS15169]  41.85                                    5 ms
      9  * 142.250.239.64 (142.250.239.64) [AS15169]  55.220 ms *
      10  72.14.232.190 (72.14.232.190) [AS15169]  55.476 ms 142.251.237.146 (142.251.237.146) [AS15169]  56.096 ms 142.250.233.0 (142.250.233.0) [AS15169]  56.821 ms
      11  142.250.56.217 (142.250.56.217) [AS15169]  58.333 ms 142.250.57.7 (142.250.57.7) [AS15169]  58.911 ms 172.253.51.239 (172.253.51.239) [AS15169]  59.934 ms
      12  * * *
      13  * * *
      14  * * *
      15  * * *
      16  * * *
      17  * * *
      18  * * *
      19  * * *
      20  * * *
      21  dns.google (8.8.8.8) [AS15169]  59.522 ms  60.180 ms  60.110 ms
      [root@issabel1 ~]#
   


---
### 6) Повторите задание 5 в утилите mtr. На каком участке наибольшая задержка - delay?

---
### Ответ:

Устанавливаем и запускаем утилиту "My traceroute" :

      root@vagrant:~#  apt install mtr

      root@vagrant:~#  mtr -zn 8.8.8.8

      Вывод экрана :

[https://github.com/edward-burlakov/vagrant/blob/main/LESSON_3.6/My%20traceroute.jpg]

      Самая  большаЯ задержка на автономной системе AS15169 компании Google LLC и адресе  209.85.246.111

---
### 7) Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой dig

---
### Ответ:  

 DNS севера (севера имён):

      root@vagrant:~# dig -t NS dns.google | grep ns
      ; <<>> DiG 9.16.1-Ubuntu <<>> -t NS dns.google
      ;; global options: +cmd
      ;; Got answer:
      ;dns.google.                    IN      NS
      dns.google.             7182    IN      NS      ns1.zdns.google.
      dns.google.             7182    IN      NS      ns3.zdns.google.
      dns.google.             7182    IN      NS      ns2.zdns.google.
      dns.google.             7182    IN      NS      ns4.zdns.google.


A-записи доменной зоны указывают на адреса 8.8.4.4 и 8.8.8.8  :

    root@vagrant:~# dig dns.google.

    ; <<>> DiG 9.16.1-Ubuntu <<>> dns.google.
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41155
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 65494
    ;; QUESTION SECTION:
    ;dns.google.                    IN      A

    ;; ANSWER SECTION:
    dns.google.             796     IN      A       8.8.4.4
    dns.google.             796     IN      A       8.8.8.8

    ;; Query time: 3 msec
    ;; SERVER: 127.0.0.53#53(127.0.0.53)
    ;; WHEN: Thu Jul 07 17:44:23 UTC 2022
    ;; MSG SIZE  rcvd: 71
 
---
### 8) Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой dig

       root@vagrant:~# dig -x 8.8.8.8 | grep PTR
       ;8.8.8.8.in-addr.arpa.          IN      PTR
       8.8.8.8.in-addr.arpa.   7184    IN      PTR     dns.google.

       root@vagrant:~# dig -x 8.8.4.4 | grep PTR
       ;4.4.8.8.in-addr.arpa.          IN      PTR
       4.4.8.8.in-addr.arpa.   7092    IN      PTR     dns.google.


