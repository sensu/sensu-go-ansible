#!/bin/sh

# Generate root CA certificate
openssl genrsa -out sensu-api-ca.key 2048
openssl req -x509 -sha256 -new -nodes -key sensu-api-ca.key -subj '/CN=Sensu-test CA' -days 1095 -out sensu-api-ca.crt

# Generate certificate
openssl genrsa -out sensu-api.key 2048
openssl req -new -key "sensu-api.key" -out "sensu-api.csr" -sha256 -subj '/CN=sensu-api'
openssl x509 -req -days 1095 -in "sensu-api.csr" -sha256 -CA "sensu-api-ca.crt" -CAkey "sensu-api-ca.key" -CAcreateserial -out "sensu-api.crt" -extfile "sensu-api.cnf" -extensions server

# print content of certificate
openssl x509 -in sensu-api-ca.crt -text
openssl x509 -in sensu-api.crt -text