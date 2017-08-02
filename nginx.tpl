# ----------------------------------------------------------------------------
# !!CAUTION!!
# This file is modified by dynamicdns, changes in this file may be lost in
# future updates
# ----------------------------------------------------------------------------
server {
    listen 127.0.0.1:80;
    server_name {{domain}};

    access_log /var/log/nginx/{{domain}}.access_log;
    error_log /var/log/nginx/{{domain}}.error_log;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://{{target_ip}}:{{target_port}};
    }
}