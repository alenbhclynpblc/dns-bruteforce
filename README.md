# DNS Bruter

We did looked for good and configurable bruteforce script for DNS records. All of our founds based on wordlists, some of the tools had true-bruteforce capabilities but they were not configurable in detail.

Tool focues for finding A type records (CNAME's are also be founded).

```
DNS Subdomain Bruteforcer.

Usage:
  dns-bruter.py <domain> [options]

Options:
  -h --help                  Show this screen.
  --thread <thread>          Thread count. [default: 100]
  --characters <characters>  Characters to use permutation [default: qwertyuopasdfghjklizxcvbnm0123456789-_]
  --length <length>          Maximum subdomain length [default: 7]
  --min-length <min-length>  Minimum subdomain length [default: 1]
  --dns-servers <servers>    DNS servers for requesting iterativly, comma for multiple [default: 8.8.8.8]
  --output-path <file>       Save outputs to file
  --statistics               Show request statistics
```
