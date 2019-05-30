# pyshella-toolkit

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
![Platform](https://img.shields.io/badge/platform-linux-green.svg)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

This is simple toolkit for Bitcoin or Bitcoin forks , which contains
cli scripts such as `peers-scanner`, `jsonrpc-searcher`, 
`jsonrpc-bruter`, `coins-withdrawal`.


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
usage: pyshella_scanner [-h] -nU  [-b] [-i] -mU   -n

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
Usage example: pyshella_scanner -nU <node_uri> -mU <mongo_uri> -n <coin_name>
```

## JSON-RPC Searcher
Scanner which discovers Bitcoin/forks JSON-RPC on peers.

### How to use
```
usage: pyshella_jsonrpc_searcher [-h] -n NAME [-mU URI] [-cT SECS] [-rT SECS]
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
