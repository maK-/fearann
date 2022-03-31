#!/usr/bin/python3

"""
  __
 / _| ___  __ _ _ __ __ _ _ __  _ __
| |_ / _ \/ _` | '__/ _` | '_ \| '_ \
|  _|  __| (_| | | | (_| | | | | | | |
|_|  \___|\__,_|_|  \__,_|_| |_|_| |_|
=======================================
*   This script can be used to generate subdomain alterations
*   It replicates altdns but adds the following features:
*       - Use list of known good & dictionary permutations
*       - Use a list of already found subdomains to make educated guesses
*       - Create special cases with numbers
*       - Minimize the test cases to unique test cases only
*       - Output the generated list to a file
*       - Part of greater "scanomaly" framework
"""

import argparse
import sys

NUMLIST = [  '0','1','2','3','4','5','6','7','8','9','10','11','12','13',
             '00','01','02','03','04','05','06','07','08','09','14','15',
             '16','17','18','20','21','22','23','24','25','99','80',
             '443','2015','2016','2017','2018','2019','2020','2021',
             '2022','2023','2024','2025']

"""
*   This class does required file in/out operations
"""
class Fileop:
    def __init__(self, name):
        self.fname = name

    #Read file to a list
    def reader(self):
        try:
            with open(self.fname) as f:
                data = f.read().splitlines()
        except IOError as e:
            print('reader: File IO Error!')
            print(e)
            sys.exit(0)
        return data

    #If data is a list write to file
    def writer(self, wobj):
        try:
            f = open(self.fname, 'w')
            for i in wobj:
                f.write(i+'\n')
            f.close()
        except IOError as e:
            print('writer: File IO Error!')
            print(e)

"""
*   Grab new wordlist to alt from a list of subdomains
*   For example - input the output of sublister
*   Example: dev-test.hax.example.com
*   Becomes: [dev-test, dev, test, hax, example, com]
"""
def getSubList(knownsubs, words):
    results = []
    templist = []
    known = Fileop(knownsubs).reader()
    words = Fileop(words).reader()
    for know in known:
        sub = know.split('.')
        for split in sub:
            if split != '*':
                templist.append(split)
            if '-' in split:
                subsplit = split.split('-')
                for basic in subsplit:
                    templist.append(basic)
    results = set(templist)
    templist = set(words)
    results = sorted(results.union(templist))
    return results

"""
*   Permutate like a motherfucker from hell, son

*   Put a word at each position in the domain test-dev.new01.example.com
*   Examples:
*   1. WORDtest-dev.new01.example.com
*   2. test-devWORD.new01.example.com
*   3. testWORD-dev.new01.example.com
*   4. test-WORDdev.new01.example.com
*   5. test-dev.WORDnew01.example.com
*   6. test-dev.new01WORD.example.com
*   7. WORD-test-dev.new01.example.com
*   8. test-dev-WORD.new01.example.com
*   9. test-WORD-dev.new01.example.com
*   10. test-dev.WORD-new01.example.com
*   11. test-dev.new01-WORD.example.com
*   12. WORD.new01.example.com
*   13. WORD-dev.new01.example.com
*   14. test-WORD.new01.example.com
*   15. test-dev.WORD.example.com
*   
*   Replace any numbers already in the domain subdomain for each sub-subdomain
*   Example: test1.example.com
*   Becomes: test[1-9].example.com, test[01-09], test[years], test[15-25]
"""
def permutate(domain, wordlist):
    perms = []
    basedom = getDomain(domain)
    nondom = domain.replace(basedom, '')[:-1]
    thesubs = nondom.split('.')
    nums = replaceNum(domain)
    perms += nums
    
    for word in wordlist:
        perms.append(word + nondom + '.' + basedom) #1.
        perms.append(nondom + word + '.' + basedom) #6.
        perms.append(word + '-' + nondom + '.' + basedom) #7.
        perms.append(nondom + '-' + word + '.' + basedom) #11.
        newsubs = nondom.split('.')
        for sub in thesubs:
            #Same shit but for subdomains with -
            if '-' in sub:
                newdashsubs = []
                dashsub = sub.split('-')
                bkpsub = nondom.split('.')
                for dash in dashsub:
                    newdash1 = word + dash
                    newdash2 = dash + word
                    newdash3 = word + '-' + dash
                    newdash4 = dash + '-' + word
                    newdash5 = word
                    bkpdash = sub.split('-')
                    for i,n in enumerate(bkpdash):
                        if dash == n:
                            bkpdash[i] = newdash1
                            ddoms = '-'.join(bkpdash)
                            newdashsubs.append(ddoms)

                            bkpdash[i] = newdash2
                            ddoms = '-'.join(bkpdash)
                            newdashsubs.append(ddoms)
                    
                            bkpdash[i] = newdash3
                            ddoms = '-'.join(bkpdash)
                            newdashsubs.append(ddoms)
        
                            bkpdash[i] = newdash4
                            ddoms = '-'.join(bkpdash)
                            newdashsubs.append(ddoms)

                            bkpdash[i] = newdash5
                            ddoms = '-'.join(bkpdash)
                            newdashsubs.append(ddoms)
                    bkpdash = dashsub
                bkpsub = nondom.split('.')
                for i,n in enumerate(bkpsub):
                    if sub == n:
                        for ds in newdashsubs:
                            bkpsub[i] = ds
                            sdoms = '.'.join(bkpsub)
                            ndomain = sdoms +'.'+ basedom
                            perms.append(ndomain)
                
            newsub1 = word + sub 
            newsub2 = sub + word    
            newsub3 = word + '-' + sub
            newsub4 = sub + '-' + word
            bkpsub = nondom.split('.') 
            for i,n in enumerate(bkpsub):
                if sub == n:
                    bkpsub[i] = newsub1
                    sdoms = '.'.join(bkpsub)
                    ndomain = sdoms +'.'+ basedom
                    perms.append(ndomain)

                    bkpsub[i] = newsub2
                    sdoms = '.'.join(bkpsub)
                    ndomain = sdoms +'.'+ basedom
                    perms.append(ndomain)

                    bkpsub[i] = newsub3
                    sdoms = '.'.join(bkpsub)
                    ndomain = sdoms +'.'+ basedom
                    perms.append(ndomain)

                    bkpsub[i] = newsub4
                    sdoms = '.'.join(bkpsub)
                    ndomain = sdoms +'.'+ basedom
                    perms.append(ndomain)
            bkpsub = thesubs

    perms = list(set(perms))
    return perms

"""
*   For domains that are double barrel or more, adjust the suffix count
*   Example: .co.uk domains
"""
def returnSuffixCount(domain):
    suffixes = Fileop('public_suffixes.txt').reader()
    count = 1
    for suffix in suffixes:
        if domain.endswith(suffix):
            count = len(suffix.split('.'))
            break
    return count + 1

"""
*   Get the base domain
"""
def getDomain(domain):
    domlist = domain.split('.')
    suff = returnSuffixCount(domain)
    domain = domlist[-suff:]
    return '.'.join(domain)

"""
*   Do our number enumeration
"""
def getLongNum(val):
    latest = []
    the_no = ''
    for i in range(0,len(val)):
        if(val[i].isnumeric()):
            the_no += val[i]
            if i < len(val)-1:
                if(val[i+1].isnumeric()):
                    continue 
                else:
                    latest.append(the_no)
                    the_no = ''
            else:
                latest.append(the_no)
                the_no = ''
    return latest
        
"""
*   Does the domain contain a number anywhere?
"""
def isNums(domain):
    basedom = getDomain(domain)
    nondom = domain.replace(basedom, '')[:-1]
    for i in NUMLIST:
        if i in nondom:
            return True
    return False

"""
*   Replace nums with the list
*   Example: test01.dev2.example.com
*   Becomes:    test[0-9, 00-09, years].dev2.example.com
*               test01.dev[0-9, 00-09, years].example.com
"""
def replaceNum(domain):
    if isNums(domain):
        pass
    else:
        return []
    perms = []
    newlist = []
    basedom = getDomain(domain)
    nondom = domain.replace(basedom, '')[:-1]
    thesubs = nondom.split('.')

    #For each subdomain, replace the nums with NUMLIST
    for sub in thesubs: 
        nums = getLongNum(sub)
        for num in nums:
            for entry in NUMLIST:
                bkpsubs = nondom.split('.')
                newdom = sub.replace(num, entry)
                for i, n in enumerate(bkpsubs):
                    if sub==n:
                        bkpsubs[i] = newdom
                subdoms = '.'.join(bkpsubs)
                newdomain = subdoms +'.'+ basedom
                perms.append(newdomain)
                bkpsubs = thesubs
    newlist = set(perms)
    return newlist
                
                
if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-s', '--subdomains', type=str, default=None,
                        help='Provide a list of known subdomains')
    parse.add_argument('-w', '--words', type=str, default='words.txt',
                        help='Provide a list of words to permutate')
    parse.add_argument('-t', '--target', type=str, default=None,
                        help='Provide a single subdomain to use as a seed')
    parse.add_argument('-l', '--listsub', type=str, default=None,
                        help='Provide a list of subdomains to use as seed')
    parse.add_argument('-o', '--output', type=str, default='output.txt',
                        help='Output a list of unique subdomains to brute')
    args = parse.parse_args()

    if len(sys.argv) <= 1:
        parse.print_help()
        sys.exit(0)

    if args.subdomains != None and args.target != None:
        alts = getSubList(args.subdomains, args.words)
        perms = permutate(args.target, alts)
        print('Number of domains generated: '+str(len(perms)))
        Fileop(args.output).writer(perms)

    if args.subdomains != None and args.listsub != None:
        alts = getSubList(args.subdomains, args.words)
        seeds = Fileop(args.listsub).reader()
        results = []
        for seed in seeds:
            perms = permutate(seed, alts)
            results = results + perms
        final = list(set(results))
        print('Number of domains generated: '+str(len(final)))
        Fileop(args.output).writer(final)
