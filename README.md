# pyshella-toolkit

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

This is simple toolkit for Bitcoin or Bitcoin forks , which contains
cli scripts such as `peers-scanner` and `coins-withdrawal`.


## Peers Scanner
The `peers scanner` scans the network for available peers and 
writes them to a file. For new peers, old ones are blacklisted.

### Installation
```bash
git clone https://github.com/mkbeh/pyshella-toolkit
cd pyshella-toolkit/
python3.6 setup.py install --user
```

### How to use
```
usage: pyshella_scanner [-h] -u  [-b] [-i]

Scanner which parse Bitcoin or forks peers and writes them into file.

optional arguments:
  -h, --help        show this help message and exit
  -u , --uri        Node URI.
  -b , --ban-time   The time(days) which will be banned each peer (by default
                    14 days).
  -i , --interval   Interval(secs) between call cycles for new peers (by
                    default 60 secs).
```