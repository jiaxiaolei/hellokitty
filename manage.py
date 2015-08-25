server {

    listen  80;
    server_name hellokitty.wangyiyang.cn;
    access_log /home/kk/www/hellokitty/logs/access.log;
    error_log /home/kk/www/hellokitty/logs/error.log;

    #charset koi8-r;

    #access_log  logs/host.access.log  main;

    location / {
     include        uwsgi_params;
     uwsgi_pass     127.0.0.1:8074;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }

    location /static/ {
        alias  /home/kk/www/hellokitty/hellokitty/static/;
        index  index.html index.htm;
    }

    location /media/ {
        alias  /home/kk/www/hellokitty/hellokitty/media/;
    }
}
