#!/usr/bin/bash

APPLIANCE_URL="{{ conjur-leader-url }}"

# Download the base64-encoded PEM bundle
openssl s_client -connect $APPLIANCE_URL:443 -showcerts </dev/null 2> \
/dev/null | awk '/BEGIN CERTIFICATE/,/END CERTIFICATE/ {print $0}' > conjur.pem

# Parse root-ca PEM from public cert chain
tail -26 conjur.pem > root.pem

# If any conflicting named containers exist, rm them
docker rm -f conjur-audit

# Build the image from the Dockerfile spec
docker build -t conjur-audit:latest .

# Run the image as a container
docker run -d --restart=unless-stopped --name conjur-audit -it conjur-audit:latest

# Add Conjur server certificates to trusted CA certificate store
docker exec -t conjur-audit mkdir -p /usr/local/share/ca-certificates/extra
docker cp conjur.crt conjur-audit:/usr/local/share/ca-certificates/extra/
docker exec -t conjur-audit update-ca-certificates

# Migrate scripts to configured container
docker cp json_2_excel.py conjur-audit:json_2_excel.py
docker cp resourceByHost.sh conjur-audit:resourceByHost.sh
docker cp run.py conjur-audit:run.py
