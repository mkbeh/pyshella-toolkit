# pyshella-toolkit
This is simple toolkit for Bitcoin or Bitcoin forks , which contains
cli scripts such as `peers-scanner` and `coins-withdrawal`.

## Peers Scanner
The `peers scanner` scans the network for available peers and 
writes them to a file. For new peers, old ones are blacklisted.

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