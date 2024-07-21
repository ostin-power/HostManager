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

# Function to print colored text
def print_colored(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
    }

    print(f"{colors[color]}{text}{colors['reset']}")
    
#loading environment variables
load_dotenv()

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
    print()
    print("usage : <command> <option> <host_alias>")
    print()
    print("\t-h --help\t# print command instructions")
    print("\t-c\t\t# create ssh connection")
    print("\t-d\t\t# delete saved host : <command> -d <host_alias>")
    print("\t-l\t\t# list all saved hosts")
    print("\t--save\t\t# save new host : <command> --save <host_alias>")
    print("\t--search\t# search for specific host : <command> --search <host_alias>")
    print("\t--reset\t\t# clear all stored aliases")
    print("\t--import\t# import from ssh config all stored hosts")
    print()

elif opt == "-c":
    #connect command
    if alias is not None:
        if alias in data:
            print("Trying to connect...")
            command = "ssh "+data[alias]["user"]+"@"+data[alias]["host"]
            if data[alias]["port"] != 22:
                command = command+" -p "+data[alias]["port"]
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
    # list command
    if data:
        print_colored("\nSaved Hosts:", 'cyan')
        print_colored("\n{:<20} {:<20} {:<20} {:<20}".format("Alias", "User", "Host", "Port"), 'yellow')
        for alias, d in data.items():
            print("{:<20} {:<20} {:<20} {:<20}".format(alias, d['user'], d['host'], d['port']))
    else:
        print_colored("No hosts saved.", 'red')

elif opt == "--save":
    if alias is not None:
        host = input("insert host : ")
        user = input("insert user : ")
        port = input("insert port (leave empty if is 22 <default ssh port>) : ")

        temp = {}
        temp['host'] = host
        temp['user'] = user
        temp['port'] = 22 if port == "" else port #set default ssh porqt

        data[alias] = temp
        save_data(SAVED_DATA_JSON, data)
        print_colored("Saved!", 'green')
    else :
        print_colored("Please specify an alias", 'yellow')
        print("<use -h or --help option>")

elif opt == "--search":
    #search command
    if alias in data:
        print(json.dumps(data[alias], indent=4))
    else:
        print_colored("Alias not found", 'yellow')

elif opt == "--reset":
    confirm = input("Are you sure you want to reset all aliases ? [Y/n] : ")
    if confirm in ["Y", "yes"]:
        save_data(SAVED_DATA_JSON, {})
    else:
        print_colored("Reset aborted!", 'yellow')

elif opt == "--import":
    #Import from .ssh/config
    data = {}
    with open(os.getenv('SSH_HOSTS_PATH_FILE'), 'r') as f:
        line = f.readline()
        while line:
            line = f.readline()
            if line.startswith('Host '):
                alias = line.split(' ')
                alias = alias[1].replace("\n","")
                data[alias] = {}
            
            if line.startswith('HostName'):
                host = line.split(' ')
                host = host[1].replace("\n","")
                data[alias]['host'] = host

            if line.startswith('User '):
                user = line.split(' ')
                user = user[1].replace("\n","")
                data[alias]['user'] = user

            if line.startswith('Port '):
                port = line.split(' ')
                port = port[1].replace("\n","")
                data[alias]['port'] = port
            
    save_data(SAVED_DATA_JSON, data)
    print_colored("Import completed!", 'green')

else:
    print_colored("Command does not exists", 'red')
    print("<use -h or --help option>")