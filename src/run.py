import sys
import argparse
import subprocess as s
from json_2_excel import convertXlsx
import os
import sys

path_to_sh = os.path.abspath(os.path.dirname(__file__))

argParser = argparse.ArgumentParser()
requiredNamed = argParser.add_argument_group("required arguments")
requiredNamed.add_argument("-u", "--url", type=str, help="The url of a Conjur Follower (or Follower LB) - no https:// prefix.", required=True)
requiredNamed.add_argument("-a", "--account", type=str, help="The conjur account for the environment (dev, prod, etc.).", required=True)
requiredNamed.add_argument("-p", "--password", type=str, help="The password of the builtin admin role.", required=True)

args = argParser.parse_args()
_url = str(args.url)
_acct = str(args.account)
_password = str(args.password)

posargs = " -u " + _url + " -a " + _acct + " -p " + _password
# try to run with the vars defined through argv
try:
    exit_code = s.run(["bash " + str(path_to_sh) + "/resourceByHost.sh" + posargs], executable='/bin/bash', shell=True, check=True)
# except OSError or ValueError
except OSError as err:
    print("OS Error: An unexpected error occurred.", err)
except ValueError:
    print("Invalid value entered: Please refer to help [-h].")

if "returncode=0" in str(exit_code):
    try:
        convertXlsx()
        s.run(["rm -Rf host_resources.json"], executable='/bin/bash', shell=True, check=True)
        s.run(["mv *.xlsx export_location/"], executable='/bin/bash', shell=True, check=True)
    except OSError as err:
        print("OS Error: An unexpected error occurred.", err)
    except ValueError:
        print("Invalid Value: Invalid entries in request.")
        print(path_to_sh)
    except ConnectionError as err:
        print("Connection Error: Verify connectivity to Conjur.")
else:
    err = exit_code
    print("Something went wrong: Validate entries and try again." + err)
    exit(1)
