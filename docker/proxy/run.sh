#!/bin/sh

set -e

echo "Checking for dhparams.pem..."
if [ ! -f "/vol/proxy/ssl-dhparams.pem"]; then
    echo "dhparams.pem does not exist. Creating it..."
    openssl dhparam -out /vol/proxy/ssl-dhparams.pem 2048
fi

#Avoid replacing these with envsubst
export host=\$host
export request_uri=\$request_uri

echo "Checking for fullchain.pem..."
if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
    echo "No SSL cert, enabling HTTP only..."
    envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
else
    echo "SSL certs exist, Enabling HTTPS..."
    envsubsts < /etc/nginx/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf
fi

nginx -g 'daemon off;'