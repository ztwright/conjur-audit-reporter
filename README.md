# Conjur-Audit-Report

Generates a role-based report on resource access control for application accounts (hosts) stored as resource data in Conjur.

> **Note**: For testing purposes only. Not recommended for production environments.

## Certification level

![](https://img.shields.io/badge/Certification%20Level-Community-28A745?link=https://github.com/cyberark/community/blob/master/Conjur/conventions/certification-levels.md)

This repo is a **Community** level project. It's a community contributed project that **is not reviewed or supported
by CyberArk**. For more detailed information on our certification levels, see [our community guidelines](https://github.com/cyberark/community/blob/master/Conjur/conventions/certification-levels.md#community).

## Requirements

To generate the report, the following must be fulfilled:

  1.  A Linux host machine (any distribution), with:
      -  Connectivity to the Conjur Follower LB over 443
      -  Docker or Podman installed

  2.  A healthy Conjur Cluster w/ Leaders + Followers

  3.  Install ``jq`` ``[i]`` to the machine running the report

> `[i]`: jq is a well-known JSON parser and interpretter for shell; Read more about jq in the [jq docs](https://jqlang.github.io/jq/manual/).

  4.  Ensure that a certificate is available in the relative project directory under `src/`:
  ```bash
  $ ls -l
  total 592K
  -rw-r--r--. 1 ec2-user ec2-user 563K Feb  3 20:37 2024-07-02_resources-by-apphost.xlsx
  -rw-r--r--. 1 ec2-user ec2-user  607 Feb  3 22:03 Dockerfile
  drwxr-xr-x. 2 ec2-user ec2-user   41 Feb  3 20:37 __pycache__
  -rwxr-xr-x. 1 ec2-user ec2-user 1.1K Feb  3 20:37 build.sh
  -rw-r--r--. 1 ec2-user ec2-user 6.3K Feb  3 21:56 conjur.crt
  -rw-r--r--. 1 ec2-user ec2-user 2.8K Feb  3 21:36 json_2_excel.py
  -rwxr-xr-x. 1 ec2-user ec2-user 2.7K Feb  3 20:37 resourceByHost.sh
  -rw-r--r--. 1 ec2-user ec2-user    0 Feb  3 22:03 root.pem
  -rw-r--r--. 1 ec2-user ec2-user 1.8K Feb  3 20:37 run.py
  ```

  If it is not, use the following command to store the certificate locally:
  ```bash
  CONJUR_URL="follower.conjur.acme.com"
  openssl s_client -showcerts -connect $CONJUR_URL:443 < /dev/null 2> /dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > conjur.crt
  ```

## Usage instructions

  1.  Run `./build.sh` to build the runtime environment for the script, as well as for the script itself.

  2.  To generate the report, simply migrate it to an applicable Linux-based host machine, and run the following command:

  ```bash
  URL="follower.conjur.acme.com"              # Follower LB Vanity URL
  ACCOUNT="conjur"                            # Account name (i.e., conjur)
  PASSWORD="somePass1!"                       # Password of the admin account
  docker exec conjur-audit python3 run.py -u $URL -a $ACCOUNT -p $PASSWORD
  ```

where...

 | Postitional Argument | Example Value | Definition                     |
 | -------------------- | ------------- | ------------------------------ |
 | URL                  | ``follower.conjur.some.site.com`` | The URL of the Conjur Follower LB - no ``https://`` prefix   |
 | ACCOUNT              | ``dev``     | The Conjur Cluster account name `[i]` |
 | PASSWORD             | ``s0me4p#s5!``  | The password of the builtin conjur admin user |
---
>  `[i]`: From `"account"` value in return JSON from `https://{{ conjur-url }}/info` endpoint

>  Run the following command to get the account name: `curl -k https://$CONJUR_URL/info | jq .configuration.conjur.account`

  3.  Once the report has finished generating, run the following commands to clean up:
  ```bash
  docker rm -f conjur-audit
  docker image rm -f conjur-audit
  ```

## Contributing

We welcome contributions of all kinds to this repository. For instructions on how to get started and descriptions
of our development workflows, please see our [contributing guide](CONTRIBUTING.md).

## License

Copyright (c) 2023 CyberArk Software Ltd. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

For the full license text see [`LICENSE`](LICENSE).
