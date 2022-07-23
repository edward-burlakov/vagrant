# Домашнее задание к занятию "3.9. Элементы безопасности информационных систем"

## 1. Установите Bitwarden плагин для браузера. Зарегистрируйтесь и сохраните несколько паролей.

Ответ:
    
![Bitwarden](https://github.com/edward-burlakov/vagrant/blob/main/bitwarden.png "Bitwarden wallet"))


## 2. Установите Google authenticator на мобильный телефон. Настройте вход в Bitwarden аккаунт через Google authenticator OTP.

Ответ:

![Google_2fa](https://github.com/edward-burlakov/vagrant/blob/main/google_2FA.png "Google_2fa"))

   
## 3. Установите apache2, сгенерируйте самоподписанный сертификат, настройте тестовый сайт для работы по HTTPS.

Ответ:

 1) Определяемся с именем хоста, для которого генерим сертификат. 

        root@vagrant:/usr/share/doc/apache2# cat /etc/hosts
        127.0.0.1 localhost
        127.0.1.1 vagrant


 2) Устанавливаем apache2

        root@vagrant:/home/vagrant# apt install apache2
        Reading package lists... Done
        Building dependency tree
        Reading state information... Done
        ...
        Created symlink /etc/systemd/system/multi-user.target.wants/apache-htcacheclean.service → /lib/systemd/system/apache-htcacheclean.service.
        Processing triggers for ufw (0.36-6ubuntu1) ...
        Processing triggers for systemd (245.4-4ubuntu3.17) ...
        Processing triggers for man-db (2.9.1-1) ...
        Processing triggers for libc-bin (2.31-0ubuntu9.9) ...
        root@vagrant:/home/vagrant#

 3) Проверяем статус сервиса 

        root@vagrant:~#  systemctl status apache2 / grep active
        root@vagrant:# systemctl status apache2 | grep active
        Active: active (running) since Fri 2022-07-22 13:33:32 UTC; 11min ago
        root@vagrant:~#

 4) Включаем модуль ssl и сайт по-умолчанию.

        root@vagrant:~# a2ensite default-ssl
        Enabling site default-ssl.
        To activate the new configuration, you need to run:
        systemctl reload apache2

        root@vagrant:~# a2enmod
        Considering dependency setenvif for ssl:
        Module setenvif already enabled
        Considering dependency mime for ssl:
        Module mime already enabled
        Considering dependency socache_shmcb for ssl:
        Enabling module socache_shmcb.
        Enabling module ssl.
        See /usr/share/doc/apache2/README.Debian.gz on how to configure SSL and create self-signed certificates.
        To activate the new configuration, you need to run:
        systemctl restart apache2
        root@vagrant:~#

 5) Проверяем, что установлен пакет ssl-cert   

        root@vagrant:~# apt list | grep ssl-cert
        WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
        ssl-cert-check/focal 4.14-1 all
        ssl-cert/focal,now 1.0.39 all [installed]


 6) Генерим самоподписанный сертификат -
   файлы /etc/ssl/certs/ssl-cert-snakeoil.pem и  /etc/ssl/private/ssl-cert-snakeoil.key.

        root@vagrant:~# make-ssl-cert generate-default-snakeoil --forceoverwrite   

 7) Перезапускаем apache2  

        root@vagrant:~#  systemctl restart apache2

    1) Тестируем сертификат по умолчанию.
 
           Тестирование показало, что на сервере APACHE2 успешно установлен сертификат, самоподписанный 
           для имени issuer=CN = vagrant и устанавливается тестовая HTTPS-сессия.
           c использованием протокола шифрования SSLv3/TLS. 
           Попытка клиента установить сессию HTTP отвергается.  
   
           root@vagrant:/home/vagrant# openssl s_client -connect localhost:443 -state -debug
           CONNECTED(00000003)
           SSL_connect:before SSL initialization
           write to 0x555fea3547c0 [0x555fea366f00] (283 bytes => 283 (0x11B))
           0000 - 16 03 01 01 16 01 00 01-12 03 03 c7 6f 2d 7c a5   ............o-|.
           0010 - 63 df 16 0a 45 c9 7a 6e-b3 5b 83 d4 06 a5 96 85   c...E.zn.[......
           0020 - 56 44 00 4e ca d0 22 f4-a4 87 d7 20 ff ee 46 81   VD.N..".... ..F.
           0030 - 25 17 93 fb c1 16 3d e3-78 55 52 38 49 e2 9e 22   %.....=.xUR8I.."
           0040 - 0c 2b f6 21 0b b8 48 43-93 44 e9 c8 00 3e 13 02   .+.!..HC.D...>..
           0050 - 13 03 13 01 c0 2c c0 30-00 9f cc a9 cc a8 cc aa   .....,.0........
           0060 - c0 2b c0 2f 00 9e c0 24-c0 28 00 6b c0 23 c0 27   .+./...$.(.k.#.'
           0070 - 00 67 c0 0a c0 14 00 39-c0 09 c0 13 00 33 00 9d   .g.....9.....3..
           0080 - 00 9c 00 3d 00 3c 00 35-00 2f 00 ff 01 00 00 8b   ...=.<.5./......
           0090 - 00 0b 00 04 03 00 01 02-00 0a 00 0c 00 0a 00 1d   ................
           00a0 - 00 17 00 1e 00 19 00 18-00 23 00 00 00 16 00 00   .........#......
           00b0 - 00 17 00 00 00 0d 00 2a-00 28 04 03 05 03 06 03   .......*.(......
           00c0 - 08 07 08 08 08 09 08 0a-08 0b 08 04 08 05 08 06   ................
           00d0 - 04 01 05 01 06 01 03 03-03 01 03 02 04 02 05 02   ................
           00e0 - 06 02 00 2b 00 05 04 03-04 03 03 00 2d 00 02 01   ...+........-...
           00f0 - 01 00 33 00 26 00 24 00-1d 00 20 31 7d db fb 9c   ..3.&.$... 1}...
           0100 - 32 4d 72 d7 7a e0 a1 8e-fa 05 af 8b 82 51 9b bb   2Mr.z........Q..
           0110 - 82 54 3b 21 20 cd 72 fc-a2 23 25                  .T;! .r..#%
           SSL_connect:SSLv3/TLS write client hello
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 16 03 03 00 7a                                    ....z
           read from 0x555fea3547c0 [0x555fea35dce8] (122 bytes => 122 (0x7A))
           0000 - 02 00 00 76 03 03 09 3d-96 33 80 ed 1e d7 90 9e   ...v...=.3......
           0010 - 15 2e f3 c2 66 cb 25 4c-6b cd 86 5f d2 80 27 36   ....f.%Lk.._..'6
           0020 - 57 ff 55 f9 42 36 20 ff-ee 46 81 25 17 93 fb c1   W.U.B6 ..F.%....
           0030 - 16 3d e3 78 55 52 38 49-e2 9e 22 0c 2b f6 21 0b   .=.xUR8I..".+.!.
           0040 - b8 48 43 93 44 e9 c8 13-02 00 00 2e 00 2b 00 02   .HC.D........+..
           0050 - 03 04 00 33 00 24 00 1d-00 20 de d6 d4 5c 27 ca   ...3.$... ...\'.
           0060 - 7d 47 54 14 3b 81 76 ba-e2 d3 0a 54 a8 c7 a0 a7   }GT.;.v....T....
           0070 - 86 cb 61 65 4a 37 29 39-6d 6c                     ..aeJ7)9ml
           SSL_connect:SSLv3/TLS write client hello
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 14 03 03 00 01                                    .....
           read from 0x555fea3547c0 [0x555fea35dce8] (1 bytes => 1 (0x1))
           0000 - 01                                                .
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 17 03 03 00 17                                    .....
           read from 0x555fea3547c0 [0x555fea35dce8] (23 bytes => 23 (0x17))
           0000 - ee 7c 08 d7 5a 75 c9 42-2e c7 cd 2a 77 a3 88 51   .|..Zu.B...*w..Q
           0010 - 71 74 53 09 ca ce e1                              qtS....
           SSL_connect:SSLv3/TLS read server hello
           Can't use SSL_get_servername
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 17 03 03 02 f5                                    .....
           read from 0x555fea3547c0 [0x555fea35dce8] (757 bytes => 757 (0x2F5))
           0000 - cf 92 75 e5 0d d9 95 af-a0 e5 d5 39 c6 ef 59 1d   ..u........9..Y.
           0010 - 89 f7 c8 9e 8d 96 60 f0-77 ad 13 24 60 7b fd 3f   ......`.w..$`{.?
           0020 - fc c1 aa 46 05 1e 85 e2-6c 6b c3 8c d6 a5 d2 0d   ...F....lk......
           0030 - d9 68 9d 08 45 e6 5c b3-b6 75 10 8d b7 fe 88 98   .h..E.\..u......
           0040 - f2 3a 8c 0a 8d a3 4a 5c-19 85 4b cf c5 5c cb e4   .:....J\..K..\..
           0050 - b4 83 cb df 9c 83 c0 5e-46 12 b1 53 47 23 4b f8   .......^F..SG#K.
           0060 - 91 78 a4 90 a0 07 7e e0-60 6f 50 a6 68 df 89 b3   .x....~.`oP.h...
           0070 - 65 bd 98 f4 a2 69 ca 75-03 ec b0 6d e7 3a 11 ec   e....i.u...m.:..
           0080 - 24 8c 4c 64 c2 c7 e8 5f-65 de 4c 95 a5 2f 8a b2   $.Ld..._e.L../..
           0090 - 3b 2b 8d 67 15 b4 e0 77-8b 58 cc f1 41 2f 3d 68   ;+.g...w.X..A/=h
           00a0 - fb fd 4e 3e f5 2c 3c a6-d6 95 3f b1 f1 53 3a a6   ..N>.,<...?..S:.
           00b0 - 6b 68 17 00 a0 87 1f 09-22 3f 4d 15 8b ec de d8   kh......"?M.....
           00c0 - 5a fd 4c 2b 55 fa 2e 27-c4 ea ef b4 4b d8 f2 3c   Z.L+U..'....K..<
           00d0 - 27 07 bd dc d0 ef 04 26-8f c6 af 31 1b ba ce a8   '......&...1....
           00e0 - 64 b2 c4 6e b3 67 84 70-89 cc e9 ea 34 b3 47 42   d..n.g.p....4.GB
           00f0 - 3f 18 b7 16 5e 92 5e 7c-bd 54 f1 f3 99 4f 7a 07   ?...^.^|.T...Oz.
           0100 - 48 71 9f 52 37 dc 07 58-db 88 4a 3b 14 f5 15 ab   Hq.R7..X..J;....
           0110 - e0 b8 81 d6 7e 4c 70 51-9f 83 20 6a 1d 15 2a db   ....~LpQ.. j..*.
           0120 - 94 1e 12 d9 13 31 10 d9-fb 0e 40 1d 9c 30 2c d2   .....1....@..0,.
           0130 - ba 57 02 6d 72 81 a6 2f-0e 9b 1a dd 71 bf cb bd   .W.mr../....q...
           0140 - 2d 8f 5f 19 67 4b 41 15-09 21 83 45 e0 3f b8 bc   -._.gKA..!.E.?..
           0150 - 4e a3 1a b5 b8 ed 66 ed-b3 7d dc 71 5f cd e3 6d   N.....f..}.q_..m
           0160 - 88 ef ea e9 d9 35 7f ef-19 2f d3 2d f8 d8 46 6a   .....5.../.-..Fj
           0170 - 4c 67 a8 03 a3 2c 0a a6-ef fb 20 8d a4 2a 81 5e   Lg...,.... ..*.^
           0180 - 9e ac 7d 04 f0 1e 9d 47-53 ea 09 40 66 97 91 53   ..}....GS..@f..S
           0190 - ff 68 34 98 6e 73 49 e4-9a 11 ae 13 a0 76 a4 97   .h4.nsI......v..
           01a0 - 3c 0f ed 03 e7 59 a4 4d-43 57 88 e1 bc 62 96 98   <....Y.MCW...b..
           01b0 - 86 fb d6 0d 20 69 1e ce-8d 6f 09 64 7f 22 a8 ec   .... i...o.d."..
           01c0 - 0e 3b 1f 94 96 68 3b 00-77 0d d5 00 38 47 0b 56   .;...h;.w...8G.V
           01d0 - 28 08 81 a8 fe bc 11 92-20 36 7c bf f9 35 34 72   (....... 6|..54r
           01e0 - 9f b9 a9 b4 c3 d6 84 b1-b7 4f fe a3 4b 9a d0 53   .........O..K..S
           01f0 - 2b 0a 26 0c 8b 80 a9 14-5a 62 b0 ab d3 08 56 2a   +.&.....Zb....V*
           0200 - d8 bb 6f db 6f 08 80 35-07 15 68 63 d0 86 fd cf   ..o.o..5..hc....
           0210 - 07 32 f9 d4 af 70 52 42-3e 5b 4c bf 17 ce 95 8c   .2...pRB>[L.....
           0220 - c5 cc 74 ad d2 f1 fd 02-b5 38 37 37 e4 1d c1 94   ..t......877....
           0230 - 01 99 dd d7 16 bb fd 2a-fe 42 22 53 6e 52 4a e9   .......*.B"SnRJ.
           0240 - 18 0b 4b 13 23 45 9a a7-6e 4c 5e 89 7c d1 75 16   ..K.#E..nL^.|.u.
           0250 - 6d 7c 1d 1b 39 ab e6 18-03 1f cb fb e0 a0 3c 9b   m|..9.........<.
           0260 - d2 05 ea 52 9c 3d fd 55-aa d0 32 d2 b6 98 62 0f   ...R.=.U..2...b.
           0270 - 4d bf aa c8 21 d3 f1 b8-90 6a ee 2a 69 ce fe 9e   M...!....j.*i...
           0280 - 30 03 65 da 73 c1 d1 6b-dc 36 59 b7 30 97 ce 56   0.e.s..k.6Y.0..V
           0290 - bd 04 da 7b e9 ef 53 f0-51 0a b1 6e ab 9a e8 c4   ...{..S.Q..n....
           02a0 - b4 83 9e 1b 1d 5f e6 72-b5 02 47 ee 80 43 8c 20   ....._.r..G..C.
           02b0 - 5b 0e 1c eb b3 4a 6b 28-1f 9f 8c 25 ac 82 22 1d   [....Jk(...%..".
           02c0 - 4c 1d a4 2d 52 fc 53 50-31 35 c9 54 e3 f7 9f 16   L..-R.SP15.T....
           02d0 - ff e0 72 37 4f bc 1f ac-10 f3 e7 ce 70 03 2f a5   ..r7O.......p./.
           02e0 - d7 29 aa ef 78 f6 89 1c-4b 54 60 5c b3 1a 56 21   .)..x...KT`\..V!
           02f0 - ba 79 ab 31 44                                    .y.1D
           SSL_connect:TLSv1.3 read encrypted extensions
           depth=0 CN = vagrant
           verify error:num=18:self signed certificate
           verify return:1
           depth=0 CN = vagrant
           verify return:1
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 17 03 03 01 19                                    .....
           read from 0x555fea3547c0 [0x555fea35dce8] (281 bytes => 281 (0x119))
           0000 - e0 64 fe 07 1d 66 0b b5-03 7d 51 27 5c 54 1f 58   .d...f...}Q'\T.X
           0010 - 93 b6 67 1b 6c 3d 67 9d-11 6a b2 a1 9e 9a 9e ca   ..g.l=g..j......
           0020 - 31 c1 30 ce 8d ec fb b6-1e 2d 0e 60 b4 dc 84 e3   1.0......-.`....
           0030 - 62 69 b3 08 92 52 c3 0b-64 54 b8 4e b1 d4 24 d2   bi...R..dT.N..$.
           0040 - 13 db 4c ba 48 76 60 cb-04 96 bd 99 cb 46 be 87   ..L.Hv`......F..
           0050 - b2 e1 ff a5 24 b6 c4 ac-90 ab f8 65 af 99 ce fb   ....$......e....
           0060 - 30 26 3b 5b 3c b5 bd 10-a6 bb da 6e d0 96 37 29   0&;[<......n..7)
           0070 - 71 37 1f b9 ad b1 7b d2-24 c6 96 3b b8 6b d0 23   q7....{.$..;.k.#
           0080 - 4c 24 aa d5 da 72 d8 75-3a dc a8 b3 7b 26 28 61   L$...r.u:...{&(a
           0090 - cd 85 45 26 73 ac db 92-ce 99 bb 07 50 4f 50 9b   ..E&s.......POP.
           00a0 - 49 5f bc 11 a4 7f aa 2a-47 14 43 28 eb bc fc f9   I_.....*G.C(....
           00b0 - 5c ab 98 3f 16 da cb 29-90 e0 c6 04 e6 39 a1 8f   \..?...).....9..
           00c0 - 84 09 ab 33 81 e4 fd 8b-96 15 9b 41 3c ab 79 83   ...3.......A<.y.
           00d0 - 1b 1a bf 8f 17 ac 81 65-19 81 0a e3 c9 d5 65 1f   .......e......e.
           00e0 - 76 98 8a 58 b0 fb 4a a8-16 d4 64 e5 fa eb 48 74   v..X..J...d...Ht
           00f0 - 3e 53 e8 8e 91 9e b3 b1-04 f2 a1 cc 51 5e f9 6c   >S..........Q^.l
            0100 - 06 e1 a2 3d 6d 0f 4b ab-b7 78 c5 85 55 1a 22 44   ...=m.K..x..U."D
           0110 - 2b 4b d5 40 29 55 f4 a6-60                        +K.@)U..`
           SSL_connect:SSLv3/TLS read server certificate
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 17 03 03 00 45                                    ....E
           read from 0x555fea3547c0 [0x555fea35dce8] (69 bytes => 69 (0x45))
           0000 - dd 7a dc 23 7d 29 22 8d-46 bd a9 b3 bd cb ed 5e   .z.#})".F......^
           0010 - f9 a3 0c c7 5c 31 af 77-af d4 02 8d 29 53 c1 1d   ....\1.w....)S..
           0020 - cd c3 d6 4a 0f 4f 89 9a-a7 b4 e0 9b 89 76 a5 58   ...J.O.......v.X
           0030 - ca 19 9d 2f b2 b5 24 77-d1 8d 46 99 8c 86 c9 f3   .../..$w..F.....
           0040 - 7d bd 56 82 65                                    }.V.e
           SSL_connect:TLSv1.3 read server certificate verify
           SSL_connect:SSLv3/TLS read finished
           SSL_connect:SSLv3/TLS write change cipher spec
           write to 0x555fea3547c0 [0x555fea366f00] (80 bytes => 80 (0x50))
           0000 - 14 03 03 00 01 01 17 03-03 00 45 cf f9 59 54 10   ..........E..YT.
           0010 - 01 b3 c7 57 e7 59 18 08-eb b1 e3 08 c3 37 94 47   ...W.Y.......7.G
           0020 - 1c 8d 2b 2b a1 1a ad a9-a2 a4 db 36 33 64 3e 56   ..++.......63d>V
           0030 - 2b 40 8e 93 b0 c6 26 46-81 11 aa f0 70 d2 c2 05   +@....&F....p...
           0040 - c0 d1 13 fd 82 98 3a 0f-1d 2e 25 e6 c5 5e ea be   ......:...%..^..
           SSL_connect:SSLv3/TLS write finished
           ---
           Certificate chain
           0 s:CN = vagrant
           i:CN = vagrant
            ---
           Server certificate
           -----BEGIN CERTIFICATE-----
           MIIC0zCCAbugAwIBAgIUQYqJUDmxfamycxU3z6MSwcvQ0r0wDQYJKoZIhvcNAQEL
           BQAwEjEQMA4GA1UEAwwHdmFncmFudDAeFw0yMjA3MjIxMzMzMjhaFw0zMjA3MTkx
           MzMzMjhaMBIxEDAOBgNVBAMMB3ZhZ3JhbnQwggEiMA0GCSqGSIb3DQEBAQUAA4IB
           DwAwggEKAoIBAQCbK9Q2j5UEDpqsjjfQDeW6a3+nXfYZOoc1MNBfZvPjj3w9EJD6
           Po2MNFd9nqi5L/vTa6MxbbGP7VDglrHx9mdOHmq3N0OSUSoumSOLmUtu1KXAebW2
           Yn35YVrvcsc1gilfrwE03wvj0Im97ZEdGAGKaJvW+aXlpwe2Msp2tV33y/I6Is6H
           tP2Z/HSL8fg/caEuyPxH8lEjwqMkBTj37nt2yqMZqkudVzGGuQTajcvsY4J7c4Kz
           bRKAERxRpC76H9atwqrtO/9tSHVeguVjWIsXyZ+rGg+GkwO5DX1wC8FGVrdVLjWr
           1ge28UQ46RBvjNPyWuOnUqdz+oPPWj+AFlv9AgMBAAGjITAfMAkGA1UdEwQCMAAw
           EgYDVR0RBAswCYIHdmFncmFudDANBgkqhkiG9w0BAQsFAAOCAQEAY7fEat/VMmbw
           NN5teYf1NR+ofxSqjpEm+glepvJY6GnqszibgizJGs1cI29GVKP0FBchCToB0MN5
           G1DucXGX3IQPzlbq1IkoZVnZNWquze3f/SyLdReDNQhZ+06Wek6RcCvcT24ZIHrG
           JeESkO18vjTMtq6+TGhN6UXyrJQE8i03CT3IKO8uJZXL5lELcJAVur2LnJ0Qjjno
           7vtwgOpBgH2sbFaatF9TqCW7C6BfV1qM40UVrLGtn9XbX0U/PX+CrmoqjGHVc3SL
           O4sCLKI/8rrdExZv5y2Qa8Rzgsb7zttgzZuDczvwuLbYWLPrhkdQMPaw0Xoyp5Um
           0xpctgxzeQ==
           -----END CERTIFICATE-----
           subject=CN = vagrant
     
           issuer=CN = vagrant
    
           ---
           No client certificate CA names sent
           Peer signing digest: SHA256
           Peer signature type: RSA-PSS
           Server Temp Key: X25519, 253 bits
           ---
           SSL handshake has read 1283 bytes and written 363 bytes
           Verification error: self signed certificate
           ---
           New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
           Server public key is 2048 bit
           Secure Renegotiation IS NOT supported
           Compression: NONE
           Expansion: NONE
           No ALPN negotiated
           Early data was not sent
           Verify return code: 18 (self signed certificate)
           ---
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 17 03 03 01 0a                                    .....
           read from 0x555fea3547c0 [0x555fea35dce8] (266 bytes => 266 (0x10A))
           0000 - 7d e5 a3 20 27 8e 51 93-a6 cf 8d 04 2c 60 3a b8   }.. '.Q.....,`:.
           0010 - 9c c3 80 ab d7 01 e2 14-0d d1 83 8a 16 ce 41 33   ..............A3
           0020 - e6 2e e1 c7 3f 87 51 b2-4e e0 cb b0 44 8b ff 06   ....?.Q.N...D...
           0030 - 40 09 51 83 cf b1 a4 67-97 b1 f2 a1 b6 8f 0c f3   @.Q....g........
           0040 - 33 10 c0 45 4f 75 68 d7-fb bb 35 59 f8 b6 73 da   3..EOuh...5Y..s.
           0050 - 8f a7 47 62 d4 e6 10 be-b2 6b be ca bc cd e8 12   ..Gb.....k......
           0060 - cc b6 3e ef a6 c7 c9 32-16 06 72 c6 8f 7a 26 5d   ..>....2..r..z&]
           0070 - e5 64 61 7a bf 72 24 5f-fd 1f cd da 73 aa e2 45   .daz.r$_....s..E
           0080 - 58 af ac 3f 57 c6 e7 7e-68 df 27 95 13 07 71 14   X..?W..~h.'...q.
           0090 - 2a 9c 51 ac db c0 5f cf-11 0d ec ec a1 fa fe 10   *.Q..._.........
           00a0 - 18 e5 27 75 ba 40 7c 7e-70 bb c5 a2 46 66 c9 74   ..'u.@|~p...Ff.t
           00b0 - 54 e8 7a b9 bd 64 cf 57-51 5e 41 3f 80 be f8 11   T.z..d.WQ^A?....
           00c0 - 60 c1 ea 72 e4 91 3a df-e2 c6 0c 22 52 17 93 a6   `..r..:...."R...
           00d0 - 08 b2 0c de 34 2a 4e 2c-79 d1 ef ac 8c b4 be 29   ....4*N,y......)
           00e0 - fb 13 b6 5b 5f 22 31 ed-c4 57 2f 77 96 66 82 87   ...[_"1..W/w.f..
           00f0 - 78 88 f5 51 59 4b bf 03-a5 ab 2f 81 e3 3e 52 c8   x..QYK..../..>R.
           0100 - a6 39 ea 4a 09 ef 41 9e-41 61                     .9.J..A.Aa
           SSL_connect:SSL negotiation finished successfully
           SSL_connect:SSL negotiation finished successfully
           ---
           Post-Handshake New Session Ticket arrived:
           SSL-Session:
           Protocol  : TLSv1.3
           Cipher    : TLS_AES_256_GCM_SHA384
           Session-ID: 34D456C6614755681FF0725BEBF44612BC2105B9291B52CFC9A1D6B85B6EA12F
           Session-ID-ctx:
           Resumption PSK: CF7F1EACEAC7968EB2DAE43E90757E997ACC15B87598193560346CB4A3B4783065D33A355FAAD9D063298AFF02970936
           PSK identity: None
           PSK identity hint: None
            SRP username: None
           TLS session ticket lifetime hint: 300 (seconds)
           TLS session ticket:
           0000 - 7c 36 d3 31 e0 52 71 bc-73 8c cc 1a de fc ea ef   |6.1.Rq.s.......
           0010 - 41 34 cc 29 a0 96 83 bf-e7 c2 2e d5 36 34 8f cc   A4.)........64..
           0020 - 56 cc 05 d8 49 54 8a 03-b9 bb e0 26 eb b1 12 c6   V...IT.....&....
           0030 - c0 c2 e8 a2 25 99 89 3f-cc dc f8 b1 5a 8e 9d ea   ....%..?....Z...
           0040 - bc 13 8c b0 3d 67 5a 57-6f 78 1b cc 32 8f 43 c0   ....=gZWox..2.C.
           0050 - 0c d6 a8 39 a6 6b 0c 0b-f1 a1 e8 d5 7f 9e a8 be   ...9.k..........
           0060 - 85 8d d5 dc ff 38 0f 3d-3a 15 7f 60 7f 28 0d d2   .....8.=:..`.(..
           0070 - 3d 89 b3 ea 43 02 43 6a-91 51 f1 a1 ed 9e 6a fe   =...C.Cj.Q....j.
           0080 - f0 19 a9 d0 74 2f 05 26-8c a8 6e 20 4b 37 3d 89   ....t/.&..n K7=.
           0090 - 10 c2 6e fa 2e 40 0c 43-b7 20 e5 40 19 bd ff 27   ..n..@.C. .@...'
           00a0 - 93 bb 89 7c 39 9e 71 6e-fa ef aa e0 7f fb b4 fe   ...|9.qn........
           00b0 - 2f 3c 70 62 51 00 61 07-65 7a d2 1b 74 ff bc ef   /<pbQ.a.ez..t...
           00c0 - 69 15 ef de e3 cd 7b e5-7d a7 aa 02 a8 2d e4 f9   i.....{.}....-..
           00d0 - f6 6e 23 7f 38 97 a1 2d-62 87 98 6a a0 ba 45 ab   .n#.8..-b..j..E.
    
              Start Time: 1658499969
              Timeout   : 7200 (sec)
              Verify return code: 18 (self signed certificate)
              Extended master secret: no
              Max Early Data: 0
           ---
           SSL_connect:SSLv3/TLS read server session ticket
           read R BLOCK
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 17 03 03 01 0a                                    .....
           read from 0x555fea3547c0 [0x555fea35dce8] (266 bytes => 266 (0x10A))
           0000 - 8f 02 fa 45 57 2f 52 a4-a3 e8 2b bb 19 2a 6f 90   ...EW/R...+..*o.
           0010 - 25 6c ce 3f 1a 40 34 e3-05 d8 aa b6 6d 09 84 59   %l.?.@4.....m..Y
           0020 - 27 f0 0e 46 c3 d9 ee 50-0d c7 09 9b 5c e1 6a 4e   '..F...P....\.jN
           0030 - f1 89 aa 65 56 72 cc 58-41 dc 1b 6e 3f 37 ba 20   ...eVr.XA..n?7.
           0040 - a1 20 c1 9e fa 80 7c 46-e0 a0 13 68 f1 c4 18 da   . ....|F...h....
           0050 - 1d 36 ef 43 76 d6 e2 22-d3 d3 6e 22 10 c1 1d c2   .6.Cv.."..n"....
           0060 - 28 9d 15 27 1c 1f fd 84-11 43 31 7c e5 06 b8 ab   (..'.....C1|....
           0070 - ce db c2 90 8e b6 6d 66-6f 69 a9 f7 1c ec ad 0b   ......mfoi......
           0080 - 33 87 9f 03 37 70 bc aa-80 9b 62 42 39 7b 9c ac   3...7p....bB9{..
           0090 - 5e c8 4b ae 3c 89 55 41-cd 6f dd 7c f8 61 24 54   ^.K.<.UA.o.|.a$T
           00a0 - 8c 2c e7 2b ac a2 9d e7-af d7 be 46 e4 96 16 0d   .,.+.......F....
           00b0 - d2 21 7a b4 73 ff 72 2e-fe 1f c8 8a d9 1e b1 b6   .!z.s.r.........
           00c0 - ff bf 1a ce 45 e3 bb 75-ab ee 82 0a 9f 3b d5 33   ....E..u.....;.3
           00d0 - 32 9d 98 1c 5a 2b 2c 3b-c7 83 9a 01 4e e1 cb ef   2...Z+,;....N...
           00e0 - 0f 5f 9e 2a 4d 56 41 f5-c5 1c a7 aa 5d 84 f8 9a   ._.*MVA.....]...
           00f0 - 2d ac a8 92 a9 8a 88 c1-0e 74 a5 d0 bd 82 72 68   -........t....rh
           0100 - 60 76 37 b5 30 82 22 03-10 ce                     `v7.0."...
           SSL_connect:SSL negotiation finished successfully
           SSL_connect:SSL negotiation finished successfully
           ---
           Post-Handshake New Session Ticket arrived:
           SSL-Session:
            Protocol  : TLSv1.3
           Cipher    : TLS_AES_256_GCM_SHA384
           Session-ID: 9489629F667E8B727927F74A11429DDCA3F1C19A73DE2615826A621B1BF7939C
           Session-ID-ctx:
            Resumption PSK: 43FA6CB49108E97F7564D32EF7EE0B592EC8324ED9F6F037B75566CC29FDC37938F19D158CC115A51ABD7D47D5F26EBC
           PSK identity: None
           PSK identity hint: None
           SRP username: None
           TLS session ticket lifetime hint: 300 (seconds)
           TLS session ticket:
           0000 - 7c 36 d3 31 e0 52 71 bc-73 8c cc 1a de fc ea ef   |6.1.Rq.s.......
           0010 - cc 07 1c d8 78 ee 80 bb-a4 f3 e7 0d 8f 84 39 05   ....x.........9.
           0020 - df cb c6 ef 2a 60 0a 0a-24 14 0e 4d 93 2e 93 ec   ....*`..$..M....
           0030 - 10 6e e6 d6 3f 92 f7 c8-c9 d2 e8 cf 8d 65 ce 85   .n..?........e..
           0040 - 4c fe 58 b4 7d bd 4d de-13 d9 55 42 4c 24 c4 27   L.X.}.M...UBL$.'
           0050 - 76 0d 16 cf dd 9c a4 96-d1 f0 34 b6 2b 56 12 50   v.........4.+V.P
           0060 - 77 b3 91 b6 3f 46 d3 3c-66 59 9d 83 7b 2c 29 eb   w...?F.<fY..{,).
           0070 - 7f 52 7e 3c 8e f1 4a 52-b7 8b b7 55 bf d7 92 2c   .R~<..JR...U...,
           0080 - ed 00 d7 c1 1d 13 45 fb-28 3d b3 02 75 c6 42 97   ......E.(=..u.B.
           0090 - 7a 13 bb e8 62 1c b5 ad-12 39 40 6e 15 8a 8d d6   z...b....9@n....
           00a0 - 35 6c d8 3e 3b f1 f0 34-16 8a 08 9a 4d 47 5f 69   5l.>;..4....MG_i
           00b0 - 51 7d 9c ea f6 aa ed c5-a0 52 47 15 6c dc 73 75   Q}.......RG.l.su
           00c0 - f3 a2 03 0d 6e 0d 91 a7-32 ae 0a 56 69 25 3c 8e   ....n...2..Vi%<.
           00d0 - 6d af 6b d3 4e 06 20 15-9d ad c2 64 bf 9e 25 aa   m.k.N. ....d..%.
    
              Start Time: 1658499969
              Timeout   : 7200 (sec)
              Verify return code: 18 (self signed certificate)
              Extended master secret: no
              Max Early Data: 0
           ---
            SSL_connect:SSLv3/TLS read server session ticket
            read R BLOCK
     
           write to 0x555fea3547c0 [0x555fea361e33] (23 bytes => 23 (0x17))
           0000 - 17 03 03 00 12 0a e3 22-04 5c e1 63 1d ce 4c a4   .......".\.c..L.
           0010 - db 39 38 6e 25 28 1f                              .98n%(.
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 17 03 03 01 f5                                    .....
           read from 0x555fea3547c0 [0x555fea35dce8] (501 bytes => 501 (0x1F5))
           0000 - 6f 6b 1a 63 c4 53 2a 7e-49 73 cf a5 a8 4b 94 48   ok.c.S*~Is...K.H
           0010 - 20 ea a1 89 eb 07 35 92-8d fa af 32 72 d6 0d 87    .....5....2r...
           0020 - d5 5d 76 af 9b 28 33 53-71 05 bf 9d 8b 7b 78 b7   .]v..(3Sq....{x.
           0030 - 49 a3 cb e0 a6 34 41 f1-17 8b f6 df 6a 9b 90 99   I....4A.....j...
           0040 - 62 68 da f1 6d 73 26 64-77 c8 a9 ec 65 47 e9 27   bh..ms&dw...eG.'
           0050 - 14 2e 46 53 6c ee 84 9f-a4 cf 93 77 57 0b c4 5f   ..FSl......wW.._
           0060 - 51 fc d9 49 5a a9 6a cb-d1 ab 3b f2 72 b9 ef 55   Q..IZ.j...;.r..U
           0070 - 90 b1 a7 ac 2e 6d d5 69-44 91 f6 d5 88 f9 6d a8   .....m.iD.....m.
           0080 - f6 60 d8 fc 59 81 d6 97-c3 eb 97 3c e8 b9 d3 a7   .`..Y......<....
           0090 - 14 64 bb 5d d8 e3 9f 71-56 4f 89 c7 9a a2 28 2e   .d.]...qVO....(.
           00a0 - 9d 2b 81 b1 e4 7f 8f 35-df 0e 4a 40 2f 3f a6 ba   .+.....5..J@/?..
           00b0 - c5 40 1c b1 93 08 ad 60-5a 47 97 b9 da 5f 8c d6   .@.....`ZG..._..
           00c0 - cf 68 44 f3 e1 62 eb ac-97 a3 08 19 79 64 82 ae   .hD..b......yd..
           00d0 - 21 82 50 e6 08 0f 31 b7-6a ed 1f 8c e5 9b c6 92   !.P...1.j.......
           00e0 - 03 74 01 28 18 6b 51 51-58 d6 97 da 20 ad 3f 24   .t.(.kQQX... .?$
           00f0 - 7d 7b 5e a8 50 35 84 37-03 a2 82 e5 7b 1b 84 b5   }{^.P5.7....{...
           0100 - 86 fb ff 7d ae 21 13 84-ec 41 dc aa c9 82 88 6f   ...}.!...A.....o
           0110 - 61 60 cf ce 8a f5 bf b5-5f eb f9 5b 63 c6 7b c3   a`......_..[c.{.
           0120 - ed 57 ad f3 d9 ea 5e c8-4c 24 a2 b5 05 f0 eb 9b   .W....^.L$......
           0130 - 3b 21 48 20 5f be d5 5d-0b b2 3a b8 5e 2f 92 bd   ;!H _..]..:.^/..
           0140 - 38 93 c3 15 93 92 b2 88-63 20 a5 a3 29 ba 11 87   8.......c ..)...
           0150 - 85 c7 36 ba a0 dc b1 7a-d6 fb 05 b8 05 09 5b 51   ..6....z......[Q
           0160 - 38 4f 5e 2f ad 6b 69 1d-87 2b d3 49 45 57 c6 e0   8O^/.ki..+.IEW..
           0170 - b4 05 f1 5b 94 bd a1 60-c6 23 69 63 89 d1 9d c0   ...[...`.#ic....
           0180 - b4 ce 02 7f 04 cf fc 19-f1 2f 1c d8 52 0a f8 63   ........./..R..c
           0190 - 25 8f 21 c1 4e 1d e3 7a-2d 48 65 e8 3e 66 0f 4b   %.!.N..z-He.>f.K
           01a0 - ba 26 98 f3 06 7a b1 04-2b 9c 5f d2 e1 cd 88 83   .&...z..+._.....
           01b0 - af da 57 d3 d8 23 46 8d-37 b5 77 28 a5 b1 e6 5f   ..W..#F.7.w(..._
           01c0 - a1 5a 32 c5 54 c0 d1 17-5d 15 a4 34 67 8e 8a 28   .Z2.T...]..4g..(
           01d0 - 40 34 25 45 0f b3 f0 1f-22 81 b6 17 1c c0 9c 01   @4%E....".......
           01e0 - 24 c9 9a f9 bd 14 4c d7-06 07 0e 6a 52 db 6e 18   $.....L....jR.n.
           01f0 - 6d 09 9f 9e 90                                    m....
           HTTP/1.1 400 Bad Request
           Date: Fri, 22 Jul 2022 14:26:12 GMT
           Server: Apache/2.4.41 (Ubuntu)
           Content-Length: 302
           Connection: close
           Content-Type: text/html; charset=iso-8859-1
    
           <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
           <html><head>
           <title>400 Bad Request</title>
           </head><body>
           <h1>Bad Request</h1>
           <p>Your browser sent a request that this server could not understand.<br />
           </p>
           <hr>
           <address>Apache/2.4.41 (Ubuntu) Server at 127.0.1.1 Port 443</address>
           </body></html>
           read from 0x555fea3547c0 [0x555fea35dce3] (5 bytes => 5 (0x5))
           0000 - 17 03 03 00 13                                    .....
           read from 0x555fea3547c0 [0x555fea35dce8] (19 bytes => 19 (0x13))
           0000 - f0 22 4a 2f eb 16 b8 c7-ba a2 69 67 32 f2 a3 29   ."J/......ig2..)
           0010 - df 9e 9b                                          ...
            SSL3 alert read:warning:close notify
           closed
           write to 0x555fea3547c0 [0x555fea361e33] (24 bytes => 24 (0x18))
           0000 - 17 03 03 00 13 e9 da 3a-0a e9 c4 8b e8 f2 79 6e   .......:......yn
            0010 - f9 4a 32 59 cc a6 c7 74-                          .J2Y...t
           SSL3 alert write:warning:close notify
           read from 0x555fea3547c0 [0x555fea34bf80] (8192 bytes => 0 (0x0))
           root@vagrant:~#

## 4. Проверьте на TLS уязвимости произвольный сайт в интернете (кроме сайтов МВД, ФСБ, МинОбр, НацБанк, РосКосмос, РосАтом, РосНАНО и любых госкомпаний, объектов КИИ, ВПК ... и тому подобное).

 Ответ:

   root@vagrant:~/testssl.sh-3.0.4#  ./testssl.sh --parallel https://pfk-obnovlenie.ru/
   
 //  ###########################################################
       testssl.sh       3.0.4 from https://testssl.sh/
   
         This program is free software. Distribution and
                modification under GPLv2 permitted.
         USAGE w/o ANY WARRANTY. USE IT AT YOUR OWN RISK!
   
          Please file bugs @ https://testssl.sh/bugs/
   
 //  ###########################################################
   
    Using "OpenSSL 1.0.2-chacha (1.0.2k-dev)" [~183 ciphers]
    on vagrant:./bin/openssl.Linux.x86_64
    (built: "Jan 18 17:12:17 2019", platform: "linux-x86_64")
   
   
    Start 2022-07-23 07:40:05        -->> 212.17.23.150:443 (pfk-obnovlenie.ru) <<--
   
    rDNS (212.17.23.150):   pfk-obnovlenie.ru.
    Service detected:       HTTP
   
   
    Testing protocols via sockets except NPN+ALPN
   
    SSLv2      not offered (OK)
    SSLv3      offered (NOT ok)
    TLS 1      offered (deprecated)
    TLS 1.1    offered (deprecated)
    TLS 1.2    offered (OK)
    TLS 1.3    not offered and downgraded to a weaker protocol
    NPN/SPDY   not offered
    ALPN/HTTP2 not offered
   
    Testing cipher categories
   
    NULL ciphers (no encryption)                  not offered (OK)
    Anonymous NULL Ciphers (no authentication)    not offered (OK)
    Export ciphers (w/o ADH+NULL)                 not offered (OK)
    LOW: 64 Bit + DES, RC[2,4] (w/o export)       offered (NOT ok)
    Triple DES Ciphers / IDEA                     not offered
    Obsolete CBC ciphers (AES, ARIA etc.)         offered
    Strong encryption (AEAD ciphers)              offered (OK)
   
   
    Testing robust (perfect) forward secrecy, (P)FS -- omitting Null Authentication/Encryption, 3DES, RC4
   
    PFS is offered (OK)          ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES256-SHA384 ECDHE-RSA-AES256-SHA DHE-RSA-AES256-GCM-SHA384
                                 DHE-RSA-AES256-SHA256 DHE-RSA-AES256-SHA ECDHE-RSA-AES128-GCM-SHA256 ECDHE-RSA-AES128-SHA256 ECDHE-RSA-AES128-SHA
                                 DHE-RSA-AES128-GCM-SHA256 DHE-RSA-AES128-SHA256 DHE-RSA-AES128-SHA
    Elliptic curves offered:     sect163k1 sect163r1 sect163r2 sect193r1 sect193r2 sect233k1 sect233r1 sect239k1 sect283k1 sect283r1 sect409k1
                                 sect409r1 sect571k1 sect571r1 secp160k1 secp160r1 secp160r2 secp192k1 prime192v1 secp224k1 secp224r1 secp256k1
                                 prime256v1 secp384r1 secp521r1 brainpoolP256r1 brainpoolP384r1 brainpoolP512r1
    DH group offered:            Unknown DH group (1536 bits)
   
    Testing server preferences
   
    Has server cipher order?     no (NOT ok)
    Negotiated protocol          TLSv1.2
    Negotiated cipher            DHE-RSA-AES256-SHA256, 1536 bit DH -- inconclusive test, matching cipher in list missing, better see below
    Negotiated cipher per proto  (matching cipher in list missing)
        RC4-SHA:                       SSLv3
        ECDHE-RSA-RC4-SHA:             TLSv1
        ECDHE-RSA-AES256-SHA:          TLSv1.1
        ECDHE-RSA-AES256-GCM-SHA384:   TLSv1.2
    No further cipher order check has been done as order is determined by the client
   
   
    Testing server defaults (Server Hello)
   
    TLS extensions (standard)    "renegotiation info/#65281" "EC point formats/#11" "max fragment length/#1"
    Session Ticket RFC 5077 hint no -- no lifetime advertised
    SSL Session ID support       yes
    Session Resumption           Tickets no, ID: yes
    TLS clock skew               -1 sec from localtime
    Signature Algorithm          SHA256 with RSA
    Server key size              RSA 4096 bits
    Server key usage             Digital Signature, Key Encipherment
    Server extended key usage    TLS Web Server Authentication, TLS Web Client Authentication
    Serial / Fingerprints        148C98426A8EBE2EDFA636D8 / SHA1 49327679E28CEDAE011BDCBC22F01751CB4855CF
                                 SHA256 5ABF8E1CA2AF7D11BABA6BD839F8C025DF2AB40EF148FA9CE06FBF99891F82EE
    Common Name (CN)             *.pfk-obnovlenie.ru
    subjectAltName (SAN)         *.pfk-obnovlenie.ru pfk-obnovlenie.ru
    Issuer                       AlphaSSL CA - SHA256 - G2 (GlobalSign nv-sa from BE)
    Trust (hostname)             Ok via SAN (same w/o SNI)
    Chain of trust               Ok
    EV cert (experimental)       no
    ETS/"eTLS", visibility info  not present
    Certificate Validity (UTC)   352 >= 60 days (2022-06-08 07:50 --> 2023-07-10 07:50)
    # of certificates provided   4 (certificate list ordering problem)
    Certificate Revocation List  http://crl.globalsign.com/gs/gsalphasha2g2.crl
    OCSP URI                     http://ocsp2.globalsign.com/gsalphasha2g2
    OCSP stapling                not offered
    OCSP must staple extension   --
    DNS CAA RR (experimental)    not offered
    Certificate Transparency     yes (certificate extension)
   
   
    Testing HTTP header response @ "/"
   
    HTTP Status Code             200 OK
    HTTP clock skew              -9 sec from localtime
    Strict Transport Security    not offered
    Public Key Pinning           --
    Server banner                CommuniGatePro/6.3.13
    Application banner           --
    Cookie(s)                    (none issued at "/")
    Security headers             X-Frame-Options: DENY
                                 X-Content-Type-Options: nosniff
                                 X-XSS-Protection: 1;mode=block
    Reverse Proxy banner         --
   
   
    Testing vulnerabilities
   
    Heartbleed (CVE-2014-0160)                not vulnerable (OK), no heartbeat extension
    CCS (CVE-2014-0224)                       not vulnerable (OK)
    Ticketbleed (CVE-2016-9244), experiment.  not vulnerable (OK), no session ticket extension
    ROBOT                                     not vulnerable (OK)
    Secure Renegotiation (RFC 5746)           supported (OK)
    Secure Client-Initiated Renegotiation     VULNERABLE (NOT ok), DoS threat
    CRIME, TLS (CVE-2012-4929)                not vulnerable (OK)
    BREACH (CVE-2013-3587)                    potentially NOT ok, "gzip" HTTP compression detected. - only supplied "/" tested
                                              Can be ignored for static pages or if no secrets in the page
    POODLE, SSL (CVE-2014-3566)               not vulnerable (OK)
    TLS_FALLBACK_SCSV (RFC 7507)              Downgrade attack prevention supported (OK)
    SWEET32 (CVE-2016-2183, CVE-2016-6329)    not vulnerable (OK)
    FREAK (CVE-2015-0204)                     not vulnerable (OK)
    DROWN (CVE-2016-0800, CVE-2016-0703)      not vulnerable on this host and port (OK)
                                              make sure you don't use this certificate elsewhere with SSLv2 enabled services
                                              https://censys.io/ipv4?q=5ABF8E1CA2AF7D11BABA6BD839F8C025DF2AB40EF148FA9CE06FBF99891F82EE could help you to find out
    LOGJAM (CVE-2015-4000), experimental      not vulnerable (OK): no DH EXPORT ciphers, no common prime detected
    BEAST (CVE-2011-3389)                     no CBC ciphers found for any protocol (OK)
    LUCKY13 (CVE-2013-0169), experimental     potentially VULNERABLE, uses cipher block chaining (CBC) ciphers with TLS. Check patches
    RC4 (CVE-2013-2566, CVE-2015-2808)        VULNERABLE (NOT ok): ECDHE-RSA-RC4-SHA RC4-SHA RC4-MD5
   
   
    Testing 370 ciphers via OpenSSL plus sockets against the server, ordered by encryption strength
   
   Hexcode  Cipher Suite Name (OpenSSL)       KeyExch.   Encryption  Bits     Cipher Suite Name (IANA/RFC)
   -----------------------------------------------------------------------------------------------------------------------------
    xc030   ECDHE-RSA-AES256-GCM-SHA384       ECDH 570   AESGCM      256      TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    xc028   ECDHE-RSA-AES256-SHA384           ECDH 570   AES         256      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
    xc014   ECDHE-RSA-AES256-SHA              ECDH 570   AES         256      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA
    x9f     DHE-RSA-AES256-GCM-SHA384         DH 1536    AESGCM      256      TLS_DHE_RSA_WITH_AES_256_GCM_SHA384
    x6b     DHE-RSA-AES256-SHA256             DH 1536    AES         256      TLS_DHE_RSA_WITH_AES_256_CBC_SHA256
    x39     DHE-RSA-AES256-SHA                DH 1536    AES         256      TLS_DHE_RSA_WITH_AES_256_CBC_SHA
    x3d     AES256-SHA256                     RSA        AES         256      TLS_RSA_WITH_AES_256_CBC_SHA256
    x35     AES256-SHA                        RSA        AES         256      TLS_RSA_WITH_AES_256_CBC_SHA
    xc02f   ECDHE-RSA-AES128-GCM-SHA256       ECDH 570   AESGCM      128      TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
    xc027   ECDHE-RSA-AES128-SHA256           ECDH 570   AES         128      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
    xc013   ECDHE-RSA-AES128-SHA              ECDH 570   AES         128      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
    x9e     DHE-RSA-AES128-GCM-SHA256         DH 1536    AESGCM      128      TLS_DHE_RSA_WITH_AES_128_GCM_SHA256
    x67     DHE-RSA-AES128-SHA256             DH 1536    AES         128      TLS_DHE_RSA_WITH_AES_128_CBC_SHA256
    x33     DHE-RSA-AES128-SHA                DH 1536    AES         128      TLS_DHE_RSA_WITH_AES_128_CBC_SHA
    x3c     AES128-SHA256                     RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA256
    x2f     AES128-SHA                        RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA
    xc011   ECDHE-RSA-RC4-SHA                 ECDH 570   RC4         128      TLS_ECDHE_RSA_WITH_RC4_128_SHA
    x05     RC4-SHA                           RSA        RC4         128      TLS_RSA_WITH_RC4_128_SHA
    x04     RC4-MD5                           RSA        RC4         128      TLS_RSA_WITH_RC4_128_MD5
   
   
    Running client simulations (HTTP) via sockets
   
    Android 4.4.2                TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 521 bit ECDH (P-521)
    Android 5.0.0                TLSv1.2 ECDHE-RSA-AES256-SHA, 521 bit ECDH (P-521)
    Android 6.0                  TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Android 7.0 (native)         TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Android 8.1 (native)         TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Android 9.0 (native)         TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Android 10.0 (native)        TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Chrome 74 (Win 10)           TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Chrome 79 (Win 10)           TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Firefox 66 (Win 8.1/10)      TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Firefox 71 (Win 10)          TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    IE 6 XP                      No connection
    IE 8 Win 7                   TLSv1.0 RC4-SHA, No FS
    IE 8 XP                      TLSv1.0 RC4-MD5, No FS
    IE 11 Win 7                  TLSv1.2 ECDHE-RSA-AES256-SHA384, 256 bit ECDH (P-256)
    IE 11 Win 8.1                TLSv1.2 ECDHE-RSA-AES256-SHA384, 256 bit ECDH (P-256)
    IE 11 Win Phone 8.1          TLSv1.2 AES128-SHA256, No FS
    IE 11 Win 10                 TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Edge 15 Win 10               TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Edge 17 (Win 10)             TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Opera 66 (Win 10)            TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
    Safari 9 iOS 9               TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Safari 9 OS X 10.11          TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Safari 10 OS X 10.12         TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Safari 12.1 (iOS 12.2)       TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Safari 13.0 (macOS 10.14.6)  TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Apple ATS 9 iOS 9            TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Java 6u45                    No connection
    Java 7u25                    TLSv1.0 ECDHE-RSA-RC4-SHA, 256 bit ECDH (P-256)
    Java 8u161                   TLSv1.2 ECDHE-RSA-AES256-SHA384, 256 bit ECDH (P-256)
    Java 11.0.2 (OpenJDK)        TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Java 12.0.1 (OpenJDK)        TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    OpenSSL 1.0.2e               TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    OpenSSL 1.1.0l (Debian)      TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    OpenSSL 1.1.1d (Debian)      TLSv1.2 ECDHE-RSA-AES256-GCM-SHA384, 256 bit ECDH (P-256)
    Thunderbird (68.3)           TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
   
    Done 2022-07-23 07:43:52 [ 230s] -->> 212.17.23.150:443 (pfk-obnovlenie.ru) <<--


 ## Проверяем еще один сервер в интернет.

         root@vagrant:~/testssl.sh-3.0.4# ./testssl.sh --parallel https://www.renewal.ru/
         
//         ###########################################################
             testssl.sh       3.0.4 from https://testssl.sh/
         
               This program is free software. Distribution and
                      modification under GPLv2 permitted.
               USAGE w/o ANY WARRANTY. USE IT AT YOUR OWN RISK!
         
                Please file bugs @ https://testssl.sh/bugs/
         
//         ###########################################################
         
          Using "OpenSSL 1.0.2-chacha (1.0.2k-dev)" [~183 ciphers]
          on vagrant:./bin/openssl.Linux.x86_64
          (built: "Jan 18 17:12:17 2019", platform: "linux-x86_64")
         
         
          Start 2022-07-23 08:34:46        -->> 151.248.114.50:443 (www.renewal.ru) <<--
         
          rDNS (151.248.114.50):  151-248-114-50.cloudvps.regruhosting.ru.
          Service detected:       HTTP
         
         
          Testing protocols via sockets except NPN+ALPN
         
          SSLv2      not offered (OK)
          SSLv3      not offered (OK)
          TLS 1      offered (deprecated)
          TLS 1.1    offered (deprecated)
          TLS 1.2    offered (OK)
          TLS 1.3    not offered and downgraded to a weaker protocol
          NPN/SPDY   not offered
          ALPN/HTTP2 http/1.1 (offered)
         
          Testing cipher categories
         
          NULL ciphers (no encryption)                  not offered (OK)
          Anonymous NULL Ciphers (no authentication)    not offered (OK)
          Export ciphers (w/o ADH+NULL)                 not offered (OK)
          LOW: 64 Bit + DES, RC[2,4] (w/o export)       not offered (OK)
          Triple DES Ciphers / IDEA                     not offered
          Obsolete CBC ciphers (AES, ARIA etc.)         offered
          Strong encryption (AEAD ciphers)              offered (OK)
         
         
          Testing robust (perfect) forward secrecy, (P)FS -- omitting Null Authentication/Encryption, 3DES, RC4
         
          PFS is offered (OK)          ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES256-SHA384 ECDHE-RSA-AES256-SHA ECDHE-RSA-AES128-GCM-SHA256
                                       ECDHE-RSA-AES128-SHA256 ECDHE-RSA-AES128-SHA
          Elliptic curves offered:     sect283k1 sect283r1 sect409k1 sect409r1 sect571k1 sect571r1 secp256k1 prime256v1 secp384r1 secp521r1
                                       brainpoolP256r1 brainpoolP384r1 brainpoolP512r1
         
         
          Testing server preferences
         
          Has server cipher order?     yes (OK)
          Negotiated protocol          TLSv1.2
          Negotiated cipher            ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Cipher order
             TLSv1:     ECDHE-RSA-AES128-SHA ECDHE-RSA-AES256-SHA AES256-SHA AES128-SHA
             TLSv1.1:   ECDHE-RSA-AES128-SHA ECDHE-RSA-AES256-SHA AES256-SHA AES128-SHA
             TLSv1.2:   ECDHE-RSA-AES128-GCM-SHA256 ECDHE-RSA-AES128-SHA256 ECDHE-RSA-AES128-SHA ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES256-SHA384
                        ECDHE-RSA-AES256-SHA AES256-GCM-SHA384 AES256-SHA256 AES256-SHA AES128-GCM-SHA256 AES128-SHA256 AES128-SHA
         
         
          Testing server defaults (Server Hello)
         
          TLS extensions (standard)    "server name/#0" "renegotiation info/#65281" "EC point formats/#11" "session ticket/#35" "heartbeat/#15"
                                       "application layer protocol negotiation/#16"
          Session Ticket RFC 5077 hint 300 seconds, session tickets keys seems to be rotated < daily
          SSL Session ID support       yes
          Session Resumption           Tickets: yes, ID: yes
          TLS clock skew               Random values, no fingerprinting possible
          Signature Algorithm          SHA256 with RSA
          Server key size              RSA 2048 bits
          Server key usage             Digital Signature, Key Encipherment
          Server extended key usage    TLS Web Server Authentication, TLS Web Client Authentication
          Serial / Fingerprints        03E1EEAAF663CD35D433BF3CDF445FB8AC2A / SHA1 0E07522C55AED118493BB94165AA5B667C6C7F6F
                                       SHA256 BBD64F970379291B0861B6998FF639394896A8D4237884C69B1D17BAA094FE74
          Common Name (CN)             renewal.ru  (CN in response to request w/o SNI: dev.renewal.ru )
          subjectAltName (SAN)         renewal.ru www.renewal.ru
          Issuer                       R3 (Let's Encrypt from US)
          Trust (hostname)             Ok via SAN (SNI mandatory)
          Chain of trust               NOT ok (expired)
          EV cert (experimental)       no
          ETS/"eTLS", visibility info  not present
          Certificate Validity (UTC)   expires < 60 days (40) (2022-06-03 23:43 --> 2022-09-01 23:43)
          # of certificates provided   3
          Certificate Revocation List  --
          OCSP URI                     http://r3.o.lencr.org
          OCSP stapling                not offered
          OCSP must staple extension   --
          DNS CAA RR (experimental)    not offered
          Certificate Transparency     yes (certificate extension)
         
         
          Testing HTTP header response @ "/"
         
          HTTP Status Code             200 OK
          HTTP clock skew              -5 sec from localtime
          Strict Transport Security    not offered
          Public Key Pinning           --
          Server banner                Apache/2.4.18 (Ubuntu)
          Application banner           --
          Cookie(s)                    1 issued: NOT secure, 1/1 HttpOnly
          Security headers             Cache-Control: no-store, no-cache, must-revalidate
                                       Pragma: no-cache
          Reverse Proxy banner         --
         
         
          Testing vulnerabilities
         
          Heartbleed (CVE-2014-0160)                not vulnerable (OK), timed out
          CCS (CVE-2014-0224)                       not vulnerable (OK)
          Ticketbleed (CVE-2016-9244), experiment.  not vulnerable (OK)
          ROBOT                                     not vulnerable (OK)
          Secure Renegotiation (RFC 5746)           supported (OK)
          Secure Client-Initiated Renegotiation     not vulnerable (OK)
          CRIME, TLS (CVE-2012-4929)                not vulnerable (OK)
          BREACH (CVE-2013-3587)                    potentially NOT ok, "none" HTTP compression detected. - only supplied "/" tested
                                                    Can be ignored for static pages or if no secrets in the page
          POODLE, SSL (CVE-2014-3566)               not vulnerable (OK), no SSLv3 support
          TLS_FALLBACK_SCSV (RFC 7507)              Downgrade attack prevention supported (OK)
          SWEET32 (CVE-2016-2183, CVE-2016-6329)    not vulnerable (OK)
          FREAK (CVE-2015-0204)                     not vulnerable (OK)
          DROWN (CVE-2016-0800, CVE-2016-0703)      not vulnerable on this host and port (OK)
                                                    make sure you don't use this certificate elsewhere with SSLv2 enabled services
                                                    https://censys.io/ipv4?q=BBD64F970379291B0861B6998FF639394896A8D4237884C69B1D17BAA094FE74 could help you to find out
          LOGJAM (CVE-2015-4000), experimental      not vulnerable (OK): no DH EXPORT ciphers, no DH key detected with <= TLS 1.2
          BEAST (CVE-2011-3389)                     TLS1: ECDHE-RSA-AES128-SHA ECDHE-RSA-AES256-SHA AES256-SHA AES128-SHA
                                                    VULNERABLE -- but also supports higher protocols  TLSv1.1 TLSv1.2 (likely mitigated)
          LUCKY13 (CVE-2013-0169), experimental     potentially VULNERABLE, uses cipher block chaining (CBC) ciphers with TLS. Check patches
          RC4 (CVE-2013-2566, CVE-2015-2808)        no RC4 ciphers detected (OK)
         
         
          Testing 370 ciphers via OpenSSL plus sockets against the server, ordered by encryption strength
         
         Hexcode  Cipher Suite Name (OpenSSL)       KeyExch.   Encryption  Bits     Cipher Suite Name (IANA/RFC)
         -----------------------------------------------------------------------------------------------------------------------------
          xc030   ECDHE-RSA-AES256-GCM-SHA384       ECDH 256   AESGCM      256      TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
          xc028   ECDHE-RSA-AES256-SHA384           ECDH 256   AES         256      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
          xc014   ECDHE-RSA-AES256-SHA              ECDH 256   AES         256      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA
          x9d     AES256-GCM-SHA384                 RSA        AESGCM      256      TLS_RSA_WITH_AES_256_GCM_SHA384
          x3d     AES256-SHA256                     RSA        AES         256      TLS_RSA_WITH_AES_256_CBC_SHA256
          x35     AES256-SHA                        RSA        AES         256      TLS_RSA_WITH_AES_256_CBC_SHA
          xc02f   ECDHE-RSA-AES128-GCM-SHA256       ECDH 256   AESGCM      128      TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
          xc027   ECDHE-RSA-AES128-SHA256           ECDH 256   AES         128      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
          xc013   ECDHE-RSA-AES128-SHA              ECDH 256   AES         128      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
          x9c     AES128-GCM-SHA256                 RSA        AESGCM      128      TLS_RSA_WITH_AES_128_GCM_SHA256
          x3c     AES128-SHA256                     RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA256
          x2f     AES128-SHA                        RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA
         
         
          Running client simulations (HTTP) via sockets
         
          Android 4.4.2                TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Android 5.0.0                TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Android 6.0                  TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Android 7.0 (native)         TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Android 8.1 (native)         TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Android 9.0 (native)         TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Android 10.0 (native)        TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Chrome 74 (Win 10)           TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Chrome 79 (Win 10)           TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Firefox 66 (Win 8.1/10)      TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Firefox 71 (Win 10)          TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          IE 6 XP                      No connection
          IE 8 Win 7                   TLSv1.0 ECDHE-RSA-AES128-SHA, 256 bit ECDH (P-256)
          IE 8 XP                      No connection
          IE 11 Win 7                  TLSv1.2 ECDHE-RSA-AES128-SHA256, 256 bit ECDH (P-256)
          IE 11 Win 8.1                TLSv1.2 ECDHE-RSA-AES128-SHA256, 256 bit ECDH (P-256)
          IE 11 Win Phone 8.1          TLSv1.2 ECDHE-RSA-AES128-SHA256, 256 bit ECDH (P-256)
          IE 11 Win 10                 TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Edge 15 Win 10               TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Edge 17 (Win 10)             TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Opera 66 (Win 10)            TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Safari 9 iOS 9               TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Safari 9 OS X 10.11          TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Safari 10 OS X 10.12         TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Safari 12.1 (iOS 12.2)       TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Safari 13.0 (macOS 10.14.6)  TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Apple ATS 9 iOS 9            TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Java 6u45                    TLSv1.0 AES128-SHA, No FS
          Java 7u25                    TLSv1.0 ECDHE-RSA-AES128-SHA, 256 bit ECDH (P-256)
          Java 8u161                   TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Java 11.0.2 (OpenJDK)        TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Java 12.0.1 (OpenJDK)        TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          OpenSSL 1.0.2e               TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          OpenSSL 1.1.0l (Debian)      TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          OpenSSL 1.1.1d (Debian)      TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
          Thunderbird (68.3)           TLSv1.2 ECDHE-RSA-AES128-GCM-SHA256, 256 bit ECDH (P-256)
         
          Done 2022-07-23 08:36:48 [ 125s] -->> 151.248.114.50:443 (www.renewal.ru) <<--


## 5. Установите на Ubuntu ssh сервер, сгенерируйте новый приватный ключ. Скопируйте свой публичный ключ на другой сервер. 
   Подключитесь к серверу по SSH-ключу.

Ответ:

Проверяем установку openssh-server на Ubuntu

         root@vagrant:~# apt show openssh-server | grep Version
         WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
         Version: 1:8.2p1-4ubuntu0.5

Проверяем статус службы: 

        root@vagrant:~# systemctl status ssh | grep Active
        Active: active (running) since Thu 2022-07-07 15:02:36 UTC; 2 weeks 1 days ago

Открываем порт для входящих соединений для сервиса:

        root@vagrant:~#  sudo ufw allow ssh

Проверяем работу сервиса:

         root@vagrant:~# ssh vagrant@127.0.0.1
         The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
         ECDSA key fingerprint is SHA256:8Lb/tKqeyNQllMhaDRbn8d8aX/ef6T2IkQ5EWnKa01s.
         Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
         Warning: Permanently added '127.0.0.1' (ECDSA) to the list of known hosts.
         vagrant@127.0.0.1's password:

Сгенерим ключи

         root@vagrant:~# ssh-keygen
         Generating public/private rsa key pair.
         Enter file in which to save the key (/root/.ssh/id_rsa):
         Enter passphrase (empty for no passphrase):
         Enter same passphrase again:
         Your identification has been saved in /root/.ssh/id_rsa
         Your public key has been saved in /root/.ssh/id_rsa.pub
         The key fingerprint is:
         SHA256:Pj0/9Iy0jvRzwST4WnXNu90SGPS+H+DizaBzj9TfSxE root@vagrant
         The key's randomart image is:
         +---[RSA 3072]----+
         |                 |
         |            .    |
         |           o . E.|
         |          . o + =|
         |        S  . X o.|
         |       . .  O *..|
         |        o +O B *+|
         |         +=*@ O.=|
         |         .++=B =+|
         +----[SHA256]-----+

Проверяем наличие пары ключей:

         root@vagrant:~# ls -la  /root/.ssh
         total 20
         drwx------ 2 root root 4096 Jul 23 08:07 .
         drwx------ 8 root root 4096 Jul 23 07:39 ..
         -rw------- 1 root root    0 Jun  7 11:50 authorized_keys
         -rw------- 1 root root 2602 Jul 23 08:07 id_rsa
         -rw-r--r-- 1 root root  566 Jul 23 08:07 id_rsa.pub
         -rw-r--r-- 1 root root  222 Jul 23 08:02 known_hosts

Копируем публичный ключ на удаленный сервер в файл /root/.ssh/authorized_keys .   

         root@vagrant:~# ssh-copy-id root@192.168.1.200
         /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_rsa.pub"
         The authenticity of host '192.168.1.200 (192.168.1.200)' can't be established.
         ECDSA key fingerprint is SHA256:zKp2l2+i+2ySq3rIZ3A8FAjazIEWwsyJ8t46SwfS0B4.
         Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
         /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
         /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
         root@192.168.1.200's password:
         
         Number of key(s) added: 1
         
         Now try logging into the machine, with:   "ssh 'root@192.168.1.200'"
         and check to make sure that only the key(s) you wanted were added.
         
         root@vagrant:~#

Подключаемся по стандартному ключу без пароля к удаленному серверу:

         root@vagrant:~# ssh root@192.168.1.200
         Last login: Fri Jul  8 00:15:00 2022 from 192.168.1.114
         
           O @ @    Issabel is a product meant to be configured through a web browser.
           @ @ O    Any changes made from within the command line may corrupt the system
           @ O O    configuration and produce unexpected behavior; in addition, changes
             O      made to system files through here may be lost when doing an update.
         
         To access your Issabel System, using a separate workstation (PC/MAC/Linux)
         Open the Internet Browser using the following URL:
         
         https://192.168.1.200
         
         Your opportunity to give back: http://www.patreon.com/issabel
         
         System load:  0.01 (1min) 0.03 (5min) 0.05 (15min)        Uptime:  290 days
         Asterisk:     Asterisk 16.7.0                       Active Calls:  0
         Memory:       [=========>---------------------------------------]  21% 421/1999M
         Usage on /:   [===============>---------------------------------]  31% 4.1/14G
         Swap usage:   0.0%
         SSH logins:   2 open sessions
         Processes:    132 total, 93 yours
         
         [root@issabel1 ~]#

Проверяем работу локальных SSH-ключей и получаем рекомендации по тонкой настройке файла /etc/ssh/sshd_config

         root@vagrant:~# apt install -y ssh-audit
         root@vagrant:~# ssh-audit localhost
         # general
         (gen) banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
         (gen) software: OpenSSH 8.2p1
         (gen) compatibility: OpenSSH 7.3+, Dropbear SSH 2016.73+
         (gen) compression: enabled (zlib@openssh.com)
         
         # key exchange algorithms
         (kex) curve25519-sha256                     -- [warn] unknown algorithm
         (kex) curve25519-sha256@libssh.org          -- [info] available since OpenSSH 6.5, Dropbear SSH 2013.62
         (kex) ecdh-sha2-nistp256                    -- [fail] using weak elliptic curves
                                                     `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
         (kex) ecdh-sha2-nistp384                    -- [fail] using weak elliptic curves
                                                     `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
         (kex) ecdh-sha2-nistp521                    -- [fail] using weak elliptic curves
                                                     `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
         (kex) diffie-hellman-group-exchange-sha256  -- [warn] using custom size modulus (possibly weak)
                                                     `- [info] available since OpenSSH 4.4
         (kex) diffie-hellman-group16-sha512         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
         (kex) diffie-hellman-group18-sha512         -- [info] available since OpenSSH 7.3
         (kex) diffie-hellman-group14-sha256         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
         
         # host-key algorithms
         (key) rsa-sha2-512                          -- [info] available since OpenSSH 7.2
         (key) rsa-sha2-256                          -- [info] available since OpenSSH 7.2
         (key) ssh-rsa                               -- [info] available since OpenSSH 2.5.0, Dropbear SSH 0.28
         (key) ecdsa-sha2-nistp256                   -- [fail] using weak elliptic curves
                                                     `- [warn] using weak random number generator could reveal the key
                                                     `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
         (key) ssh-ed25519                           -- [info] available since OpenSSH 6.5
         
         # encryption algorithms (ciphers)
         (enc) chacha20-poly1305@openssh.com         -- [info] available since OpenSSH 6.5
                                                     `- [info] default cipher since OpenSSH 6.9.
         (enc) aes128-ctr                            -- [info] available since OpenSSH 3.7, Dropbear SSH 0.52
         (enc) aes192-ctr                            -- [info] available since OpenSSH 3.7
         (enc) aes256-ctr                            -- [info] available since OpenSSH 3.7, Dropbear SSH 0.52
         (enc) aes128-gcm@openssh.com                -- [info] available since OpenSSH 6.2
         (enc) aes256-gcm@openssh.com                -- [info] available since OpenSSH 6.2
         
         # message authentication code algorithms
         (mac) umac-64-etm@openssh.com               -- [warn] using small 64-bit tag size
                                                     `- [info] available since OpenSSH 6.2
         (mac) umac-128-etm@openssh.com              -- [info] available since OpenSSH 6.2
         (mac) hmac-sha2-256-etm@openssh.com         -- [info] available since OpenSSH 6.2
         (mac) hmac-sha2-512-etm@openssh.com         -- [info] available since OpenSSH 6.2
         (mac) hmac-sha1-etm@openssh.com             -- [warn] using weak hashing algorithm
                                                     `- [info] available since OpenSSH 6.2
         (mac) umac-64@openssh.com                   -- [warn] using encrypt-and-MAC mode
                                                     `- [warn] using small 64-bit tag size
                                                     `- [info] available since OpenSSH 4.7
         (mac) umac-128@openssh.com                  -- [warn] using encrypt-and-MAC mode
                                                     `- [info] available since OpenSSH 6.2
         (mac) hmac-sha2-256                         -- [warn] using encrypt-and-MAC mode
                                                     `- [info] available since OpenSSH 5.9, Dropbear SSH 2013.56
         (mac) hmac-sha2-512                         -- [warn] using encrypt-and-MAC mode
                                                     `- [info] available since OpenSSH 5.9, Dropbear SSH 2013.56
         (mac) hmac-sha1                             -- [warn] using encrypt-and-MAC mode
                                                     `- [warn] using weak hashing algorithm
                                                     `- [info] available since OpenSSH 2.1.0, Dropbear SSH 0.28
         
         # algorithm recommendations (for OpenSSH 8.2)
         (rec) -diffie-hellman-group-exchange-sha256 -- kex algorithm to remove
         (rec) -ecdh-sha2-nistp256                   -- kex algorithm to remove
         (rec) -ecdh-sha2-nistp384                   -- kex algorithm to remove
         (rec) -ecdh-sha2-nistp521                   -- kex algorithm to remove
         (rec) -ecdsa-sha2-nistp256                  -- key algorithm to remove
         (rec) -hmac-sha1                            -- mac algorithm to remove
         (rec) -hmac-sha2-256                        -- mac algorithm to remove
         (rec) -hmac-sha2-512                        -- mac algorithm to remove
         (rec) -umac-64@openssh.com                  -- mac algorithm to remove
         (rec) -umac-128@openssh.com                 -- mac algorithm to remove
         (rec) -hmac-sha1-etm@openssh.com            -- mac algorithm to remove
         (rec) -umac-64-etm@openssh.com              -- mac algorithm to remove



## 6. Переименуйте файлы ключей из задания 5. Настройте файл конфигурации SSH клиента, так чтобы вход на удаленный сервер осуществлялся по имени сервера.

Ответ:
Переименовываем файлы

         root@vagrant:~/.ssh# cd ~/.ssh
         root@vagrant:~/.ssh# mv id_rsa 1.200_rsa
         root@vagrant:~/.ssh# mv id_rsa.pub 1.200_rsa.pub

Настраиваем файл конфигурации клиента

         root@vagrant:~/.ssh# cat config
             Host asterisk
             HostName 192.168.1.200
             IdentityFile ~/.ssh/1.200_rsa
             User root
        
Подключаемся к удаленному серверу по имени

         root@vagrant:~/.ssh# ssh asterisk
         Last login: Sat Jul 23 20:43:09 2022 from 192.168.214.203
         
           O @ @    Issabel is a product meant to be configured through a web browser.
           @ @ O    Any changes made from within the command line may corrupt the system
           @ O O    configuration and produce unexpected behavior; in addition, changes
             O      made to system files through here may be lost when doing an update.
         
         To access your Issabel System, using a separate workstation (PC/MAC/Linux)
         Open the Internet Browser using the following URL:
         
         https://192.168.1.200
         
         Your opportunity to give back: http://www.patreon.com/issabel
         
         System load:  0.00 (1min) 0.02 (5min) 0.05 (15min)        Uptime:  291 days
         Asterisk:     Asterisk 16.7.0                       Active Calls:  0
         Memory:       [=========>---------------------------------------]  21% 421/1999M
         Usage on /:   [===============>---------------------------------]  31% 4.1/14G
         Swap usage:   0.0%
         SSH logins:   2 open sessions
         Processes:    132 total, 93 yours

         [root@issabel1 ~]#

## 7. Соберите дамп трафика утилитой tcpdump в формате pcap, 100 пакетов. Откройте файл pcap в Wireshark.

        root@vagrant:~# tcpdump -c 100 -w tcpdump.log
        tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
        100 packets captured
        105 packets received by filter
        0 packets dropped by kernel

Скачиваем файл дампа на Windows c помощью psftp в составе putty

       cd c:\tmp

       c:\tmp>psftp
       psftp: no hostname specified; use "open host.name" to connect
       psftp> open 127.0.0.1 2222
       login as: vagrant
       vagrant@127.0.0.1's password:
       Remote working directory is /home/vagrant
       psftp> !lpwd
       Current local directory is c:\tmp
       psftp> get tcpdump.log
       remote:/home/vagrant/tcpdump.log => local:tcpdump.log
       psftp> quit
       
Проверяем содержимое папки c:\tmp

       c:\tmp>dir  c:\tmp
       Том в устройстве C имеет метку SYSTEM
       Серийный номер тома: 6105-DDBC

       23.07.2022  21:16    <DIR>          .
       23.07.2022  21:16    <DIR>          ..
       23.07.2022  21:16    15217 tcpdump.log
               1 файлов        15  217 байт
               2 папок  37 493 080 064 байт свободно

Открываем файл tcpdump.log  в пакете WiresharkPortable64  - Скриншот ниже

![Tcpdump Log](https://github.com/edward-burlakov/vagrant/blob/main/tcpdump_log.png "Tcpdump Log")

