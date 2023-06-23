#!/usr/bin/env bash

# Preprocessing args from python subprocess call

# Function initArg()
# Args:
#   -u --> Conjur URL
#   -a --> Conjur account name
#   -p --> Conjur audit-role password
set -x
initArg(){
    while getopts ":u:a:p:" flag
    do
        case "${flag}" in
            u) url=${OPTARG};;
            a) acct=${OPTARG};;
            p) pass=${OPTARG};;
        esac
    done
}

# Call the function to parse the arguments from the command
initArg $@

# Preprocessing environment vars
creds=$(echo "admin:$pass" | tr -d '\n' | base64)

# openssl command to get public certificate back from Conjur
openssl s_client -connect $url:443 \
  -showcerts </dev/null 2> /dev/null | \
  awk '/BEGIN CERTIFICATE/,/END CERTIFICATE/ {print $0}' \
  > $HOME/conjur.pem

# INSTALL: jq for formatting output
# sudo yum install jq -y
# GET: API key for admin user
apikey=$(curl --cacert $HOME/conjur.pem --silent --location --request GET "https://$url/authn/$acct/login" -H "Authorization: Basic $creds" --data-raw "")

getToken(){
    # POST: Auth-Z token for admin user
    token=$(curl --cacert $HOME/conjur.pem --silent --location --request POST "https://$url/authn/$acct/admin/authenticate" -H 'Content-Type: application/json' -H 'Accept-Encoding: base64' --data-raw "$apikey")
}

getToken

# GET: Conjur hosts and send to file
curl --cacert $HOME/conjur.pem --silent --location --request GET "https://$url/resources/$acct?kind=host" -H "Authorization: Token token=\"$token\"" > tmp.json

cat tmp.json | grep -o '"id":"[^"]*' > tmp2.json
cat tmp2.json | grep -o "$acct[^\"]*" > decode.json
rm tmp.json tmp2.json

# GET: Resources for each given host -> output results to output.file
LINES=$(cat decode.json)
echo "[" > hosts.json
for LINE in $LINES
    do
	    # Refreshes token every iteration
        getToken
        echo $LINE > string.txt
	    sed -e 's/\//%2F/g' string.txt > string2.txt
	    sed -e 's/\:/%3A/g' string2.txt > string3.txt
	    cat string3.txt >> encoded.json
	    hostId=$(cat string3.txt)
	    host=$(cat string.txt)
	    
	    echo "{\"hostid\": "\"$host\""," >> hosts.json
        echo "\"resources\": [" >> hosts.json
        resources="$(curl --cacert $HOME/conjur.pem --silent --request GET "https://$url/resources/$acct?role=$hostId" -H "Authorization: Token token=\"$token\"")"
        resources=$(echo $resources | sed 's/^\[//g')
        echo $resources | sed 's/]$//g' >> hosts.json
	    echo "]}," >> hosts.json
    done

echo "]" >> hosts.json
cat hosts.json | sed -z 's/},\n]/}\n]/g' > hosts2.json
mv hosts2.json hosts.json
cat hosts.json | jq '.' > "host_resources.tmp"
rm -f string.txt string2.txt string3.txt  hosts.json decode.json encoded.json
mv "host_resources.tmp" "host_resources.json"
