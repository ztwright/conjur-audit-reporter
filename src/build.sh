#!/usr/bin/bash

# If any conflicting named containers exist, rm them
docker rename conjur-audit conjur-audit-backup

# Build the image from the Dockerfile spec
docker build -t conjur-audit:latest .

# Run the image as a container
docker run -d --restart=unless-stopped --name conjur-audit -v $(pwd):/export_location/ -it conjur-audit:latest

# Add Conjur server certificates to trusted CA certificate store
docker exec -t conjur-audit mkdir -p /usr/local/share/ca-certificates/extra
docker cp conjur.crt conjur-audit:/usr/local/share/ca-certificates/extra/
docker exec -t conjur-audit update-ca-certificates

# Migrate scripts to configured container
docker cp json_2_excel.py conjur-audit:json_2_excel.py
docker cp resourceByHost.sh conjur-audit:resourceByHost.sh
docker cp run.py conjur-audit:run.py
docker cp conjur.crt conjur-audit:/root/conjur.pem
