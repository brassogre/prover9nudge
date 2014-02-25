import os
import sys
import string
import pickle
import cPickle as pickle
import hashlib
import ladrParser
import globalConfig as gc 

def allWhiteSpace(s):
    sentinal = True
    for c in s:
        if not c in string.whitespace: sentinal = False
    return sentinal

class Clause:
    """Class for defining clauses."""
    
    parse_dictionary = {}
    hashKey = ''

    def __init__(self, s):
        self.parse_dictionary = ladrParser.ladr_parser(s)
        pickleString = pickle.dumps(self)
        self.hashKey = hashlib.sha224(pickleString).hexdigest()

    def prettyPrint(self):
        pass

