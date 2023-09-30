FROM nginx:1.24.0-alpine

COPY conf /etc/nginx/conf.d/default.conf
COPY ../certificate.crt /etc/nginx/
COPY ../private.key /etc/nginx/