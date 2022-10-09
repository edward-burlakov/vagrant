FROM httpd

RUN apt update
RUN apt install apache2 -y
RUN apt install apache2-utils -y
RUN apt clean
RUN cp $HOME/www/index.html /var/www/html/index.html

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND
