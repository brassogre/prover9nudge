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
        self.original = s
        #print s
        try:
            self.parse_dictionary = ladrParser.ladr_parser(s)
        except RuntimeError:
            self.parse_dictionary = None
        pickleString = pickle.dumps(self)
        self.hashKey = hashlib.sha224(pickleString).hexdigest()
        try:
            self.parse_dictionary['canonical_hash'] = hashlib.sha224(pickle.dumps(self.parse_dictionary['tree_canonicalized'])).hexdigest()
        except:
            self.parse_dictionary['canonical_hash'] = ''

    def prettyPrint(self):
        pass

    def clause_matches(self, new_clause):
        return self.parse_dictionary['tree_canonicalized'] == (
            new_clause.parse_dictionary['tree_canonicalized'])

    def clause_transformation(self, new_clause):
        """Dictionary to map self.clause into new_clause"""
        d = {v: new_clause.parse_dictionary['inverse_replacement_dict']\
                [self.parse_dictionary['replacement_dict'][v]] for v in\
                self.parse_dictionary['flattened']}
        return d


