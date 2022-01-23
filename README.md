# HostManager

A small system that allow you to manage hosts stored in your .ssh/config file

HostManager requires Python3 to run.

## Installation

After cloning the repository, create .env file in the working directory and set the environment variables.

```bash
SSH_HOSTS_PATH_FILE="path/to/your/ssh/config"
JSON_FILE="path/to/storage/file/data.json"
```

### Add new alias for your command

#### MacOS

on your terminal type
```bash
nano ~/.bash_profile
```
then add
```bash
alias <your_command>="python3 /path/to/repo/manager.py" 
```
save and restart terminal

#### Linux

on your terminal type
```bash
nano ~/.bashrc
```
then add
```bash
alias <your_command>="python3 /path/to/repo/manager.py" 
```
save and restart terminal


## Usage

```bash
usage : <command> <option> <host_alias>

	-h --help	# print command instructions
	-c		# create ssh connection
	-d		# delete saved host : <command> -d <host_alias>
	-l		# list all saved hosts
	--save		# save new host : <command> --save <host_alias>
	--search	# search for specific host : <command> --search <host_alias>
	--reset		# clear all stored aliases
	--import	# import from ssh config all stored hosts
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
