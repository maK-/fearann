# fearann - (previously called domaination)
This is a simple script to generate subdomain permutations/alterations. Goes hard with massdns or shuffledns. It was originally part of a an automated discovery framework. For a single domain please use the following:

` ./fearann.py -s [list-of-known-subs.txt] -t [some.dev-test.example.com] -o output-file.txt`

It can also be passed a list using the following:  **Note:** *be conscious a single subdomain can have 250k+ permutations*

` ./fearann.py -s [list-of-known-subs.txt] -t [list-of-subdomains-to-permutate.txt] -o output-file.txt`

A large list may take a long time,

Estimates: list of **1000** subdomains = **250,000,000** permutations

## Different permutations used

Put a word at each position in the domain test-dev.new01.example.com
Examples:
 1. WORDtest-dev.new01.example.com
 2. test-devWORD.new01.example.com
 3. testWORD-dev.new01.example.com
 4. test-WORDdev.new01.example.com
 5. test-dev.WORDnew01.example.com
 6. test-dev.new01WORD.example.com
 7. WORD-test-dev.new01.example.com
 8. test-dev-WORD.new01.example.com
 9. test-WORD-dev.new01.example.com
 10. test-dev.WORD-new01.example.com
 11. test-dev.new01-WORD.example.com
 12. WORD.new01.example.com
 13. WORD-dev.new01.example.com
 14. test-WORD.new01.example.com
 15. test-dev.WORD.example.com
   
Replace any numbers already in the domain subdomain for each sub-subdomain
Example: test1.example.com
Becomes: test[1-9].example.com, test[01-09], test[years], test[15-25]


