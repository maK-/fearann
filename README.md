# fearann - (previously called domaination)
This is a simple script to generate subdomain permutations/alterations. Goes hard with massdns or shuffledns. It was originally part of a an automated discovery framework. For a single domain please use the following:

` ./fearann.py -s [list-of-known-subs.txt] -t [some.dev-test.example.com] -o output-file.txt`

It can also be passed a list using the following:  **Note:** *be conscious a single subdomain can have 250k+ permutations*

` ./fearann.py -s [list-of-known-subs.txt] -t [list-of-subdomains-to-permutate.txt] -o output-file.txt`

A large list may take a long time,

Estimates: list of **1000** subdomains = **250,000,000** permutations

