
import pickle
#  import cPickle as pickle
import hashlib
import ladrParser

class Clause:
    """Class for defining clauses."""

    parse_dictionary = {}
    hashKey = ''
    human_readable_string = ''

    def __init__(self, s):
        """
        The clause is initialized using str s.
        """
        self.human_readable_string = s
        self.parse_dictionary = ladrParser.ladr_parser(s)
        pickleString = pickle.dumps(self)
        self.hashKey = hashlib.sha224(pickleString).hexdigest()

    def __str__(self):
        return self.human_readable_string

