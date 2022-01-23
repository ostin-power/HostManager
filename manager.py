import sys
import os
import json
import subprocess
from dotenv import load_dotenv

#function used for loading json file data into dict variable
def load_data(filepath) :
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except:
        return {}

#function used to store data into json file
def save_data(filepath, data):
    with open (filepath, "w") as f:
        json.dump(data, f)

#loading environment variables
load_dotenv()

#Hosts file
HOSTS_FILE = os.getenv('SSH_HOSTS_PATH_FILE')

#Loading data from json
SAVED_DATA_JSON = os.getenv('JSON_FILE')
data = load_data(SAVED_DATA_JSON)

#command to exec
opt = None
if len(sys.argv) >= 2:
    opt = sys.argv[1]

#host alias
alias = None
if len(sys.argv) >= 3:
    alias = sys.argv[2]

if opt == "-h" or opt == "--help":
    #help command
    print("[ usage : <command> <option> <host_alias> ]")
    print("[\t-h\t\t# print command instructions]")
    print("[\t-c\t\t# create ssh connection]")
    print("[\t-d\t\t# delete saved host : <command> -d <host_alias>]")
    print("[\t-l\t\t# list all saved hosts]")
    print("[\t--save\t\t# save new host : <command> --save <host_alias>]")
    print("[\t--search\t# search for specific host : <command> --search <host_alias>]")

elif opt == "-c":
    #connect command
    if alias is not None:
        if alias in data:
            print("Trying to connect...")
            command = "ssh "+data[alias]["user"]+"@"+data[alias]["host"]
            subprocess.call(command, shell=True)
        else:
            print("Alias not found!")
    else:
        print("Please specify an alias!")

elif opt == "-d":
    #delete command
    if alias is not None:
        if alias in data:
            data.pop(alias)
            save_data(SAVED_DATA_JSON, data)
        else:
            print("Alias not found")
    else:
        print("Please specify an alias")
        print("<use -h or --help option>")

elif opt == "-l":
    #list command
    print(json.dumps(data, indent=4))

elif opt == "--save":
    if alias is not None:
        host  = input("insert host : ")
        user  = input("insert user : ")

        temp = {}
        temp['host'] = host
        temp['user'] = user

        data[alias] = temp
        save_data(SAVED_DATA_JSON, data)
        print("Saved!")
    else :
        print("Please specify an alias")
        print("<use -h or --help option>")

elif opt == "--search":
    #search command
    if alias in data:
        print(json.dumps(data[alias], indent=4))
    else:
        print("Alias not found")

elif opt == "--reset":
    confirm = input("Are you sure you want to reset aliases ? [Y/n]")
    if confirm.upper() == "Y":
        save_data(SAVED_DATA_JSON, {})
    else:
        print("Reset aborted!")
elif opt == "-import":
    print()
else:
    print("Command does not exists")
    print("<use -h or --help option>")