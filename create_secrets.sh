#!/bin/bash

SECRETS_BASEDIR=secrets/certs

rm -rf "$SECRETS_BASEDIR"
mkdir -p "$SECRETS_BASEDIR" \
&& openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
    -subj "/O=DSI testbed" \
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1,DNS:nginx,DNS:trino,DNS:spark-iceberg,DNS:spark-worker,DNS:hive-metastore" \
    -keyout "$SECRETS_BASEDIR"/cert.key -out "$SECRETS_BASEDIR"/cert.crt \
&& openssl pkcs12 -export -out "$SECRETS_BASEDIR"/cert.pfx -inkey "$SECRETS_BASEDIR"/cert.key -in "$SECRETS_BASEDIR"/cert.crt -password pass:mypassword \
&& keytool -importkeystore -srckeystore "$SECRETS_BASEDIR"/cert.pfx -srcstoretype pkcs12 \
-srcalias 1 -srcstorepass mypassword -destkeystore "$SECRETS_BASEDIR"/cert.jks -deststoretype jks -deststorepass mypassword -destalias myalias
