import sys
import argparse
import subprocess as s
from json_2_excel import convertXlsx 
import os
import sys

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_sh = os.path.abspath(os.path.join(bundle_dir, 'src'))

argParser = argparse.ArgumentParser()
requiredNamed = argParser.add_argument_group("required arguments")
requiredNamed.add_argument("-u", "--url", type=str, help="The url of a Conjur Follower (or Follower LB).", required=True)
requiredNamed.add_argument("-a", "--account", type=str, help="The conjur account for the environment (dev, prod, etc.).", required=True)
requiredNamed.add_argument("-s", "--serviceacct", type=str, help="The service account running the executable.", required=True)
requiredNamed.add_argument("-p", "--password", type=str, help="The password of the builtin admin role.", required=True)

args = argParser.parse_args()
_url = str(args.url)
_acct = str(args.account)
_sa = str(args.serviceacct)
_password = str(args.password)

posargs = " -u " + _url + " -a " + _acct + " -s " + _sa + " -p " + _password
# try to run with the vars defined through argv
try:
    exit_code = s.run(["bash " + str(path_to_sh) + "/resourceByHost.sh" + posargs], executable='/bin/bash', shell=True, check=True)
# except OSError or ValueError
except OSError as err:
    print("OS Error Occurred:\n", err)
except ValueError:
    print("Invalid value entered. Please refer to help [-h].")

if "returncode=0" in str(exit_code):
    try:
        convertXlsx()
        s.run(["rm -Rf host_resources.json"], executable='/bin/bash', shell=True, check=True)
    except OSError as err:
        print("OS Error Occurred:\n", err)
    except ValueError:
        print("Invalid value entered. Please refer to help [-h].")

else:
    err = exit_code
    print("Something went wrong. Please double-check passed parameters.\n\n" + err)
    exit(1)
