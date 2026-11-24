#!/usr/bin/env bash
# A certificate for the made-up Machine on 127.0.0.1, in the folder given: cert.pem, key.pem and the root.pem it is checked
# against. The root is good for a day, for 127.0.0.1 only, and its key is gone when this ends. Whoever runs this decides
# where the root is trusted (desktop.yml: on its throwaway runner, while the smoke run lasts).
set -euo pipefail
mkdir -p "$1"
cd "$1"
cat > made-up.cnf <<'T'
[req]
distinguished_name = name
prompt = no
[name]
CN = $ENV::NAME
[root]
basicConstraints = critical,CA:TRUE,pathlen:0
keyUsage = critical,keyCertSign
subjectKeyIdentifier = hash
nameConstraints = critical,permitted;IP:127.0.0.1/255.255.255.255
[cert]
basicConstraints = critical,CA:FALSE
keyUsage = critical,digitalSignature
extendedKeyUsage = serverAuth
subjectAltName = IP:127.0.0.1
authorityKeyIdentifier = keyid
T
new() { NAME=$1 openssl req -config made-up.cnf -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes "${@:2}"; }
trap 'rm -f root.key cert.csr made-up.cnf' EXIT
new 'Made-up Machine root' -x509 -days 1 -extensions root -keyout root.key -out root.pem
new 127.0.0.1 -keyout key.pem -out cert.csr
NAME=127.0.0.1 openssl x509 -req -in cert.csr -CA root.pem -CAkey root.key -set_serial "0x$(openssl rand -hex 8)" -days 1 -extfile made-up.cnf -extensions cert -out cert.pem
