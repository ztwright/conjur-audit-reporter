# Audit-Reporter 

Generates an role-based report on resource access control for application accounts (hosts).

> ***NOTE***: For testing purposes only. Not recommended for production environments.

## Certification level

![](https://img.shields.io/badge/Certification%20Level-Community-28A745?link=https://github.com/cyberark/community/blob/master/Conjur/conventions/certification-levels.md)

This repo is a **Community** level project. It's a community contributed project that **is not reviewed or supported
by CyberArk**. For more detailed information on our certification levels, see [our community guidelines](https://github.com/cyberark/community/blob/master/Conjur/conventions/certification-levels.md#community).

## Requirements

To generate the report, the following must be fulfilled:
1. A Linux host machine (any distribution), with:
  1. Connectivity to the Conjur Follower LB over 443
2. A healthy Conjur Cluster w/ Leaders + Followers

## Usage instructions

To generate the report, simply migrate it to an applicable Linux-based host machine, and run the following command:
`./build-report.exe -u URL -a ACCOUNT -s SERVICEACCT -p PASSWORD`

where...

 | Postitional Argument | Definition                          |
 | -------------------- | ----------------------------------- |
 | URL                  | The URL of the Conjur Follower LB   |
 | ACCOUNT              | The Conjur Cluster account name[^1] |
 | SERVICEACCT          | The service account running the executable |
 | PASSWORD             | The password of the builtin conjur admin user |

[^1]: From `"account"` value in return JSON from `https://{{ conjur-url }}/info` endpoint

## Contributing

We welcome contributions of all kinds to this repository. For instructions on how to get started and descriptions
of our development workflows, please see our [contributing guide](CONTRIBUTING.md).

## License

Copyright (c) 2020 CyberArk Software Ltd. All rights reserved.

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
