#!/usr/bin/python2.7

"""
Creates the most gibberish possible by compounding word
pieces and sorting the results based on highest entropy.
Inspired by moonbase alpha youtube videos.
"""   

import re
import entropy
import subprocess
import random
from collections import defaultdict

wordlist = open('words.txt','r')
somedict = defaultdict(list)
words = wordlist.readlines()
wordlist = [ word.strip() for word in words if re.search('rur[a-z]',word) ]


for i in range(0,10000):
    e_words = random.sample(wordlist,10)
    e_words = ''.join(e_words)

    cmd = ['/usr/bin/espeak','--stdout',e_words]

    if not cmd:
        continue

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    somedict[e_words] = entropy.shannon_entropy(proc.stdout.read())
    print (somedict[e_words]*100),e_words
