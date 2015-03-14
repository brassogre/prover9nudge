"""
    Miscellaneous utility functions for processing strings.
"""
import string
import globalConfig as gc

def stripWhitespace(structure):
    """Returns a copy of the structure with all its strings stripped of all whitespace characters.
    If structure is a str, a whitespace-stripped str is returned."""
    ltype = type(structure)
    if ltype == str:
        out = ''
        for c in structure:
            if not c in string.whitespace:
                out += c
        return out
    #  Recurse into any list or tuples
    if ltype == list or ltype == tuple:
        return ltype([stripWhitespace(s) for s in structure if not allWhitespace(s)])
    #  If structure is neither a str, list, or tuple, raise a TypeError
    raise TypeError

def allDigits(s):
    """Returns True iff every character in str s is a numerical digit."""
    for c in s:
        if not c in string.digits: return False
    return True

def allWhitespace(s):
    """Returns True iff s is a str and every character in s is a whitespace character."""
    if type(s) == str:
        for c in s:
            if not c in string.whitespace:
                return False
        return True
    return False

def stripComments(s):
    """
    Returns the initial substring of s up to a non-quoted instance of 
    globalConfig.COMMENT_MARKER
    """
    #  There are currently no quotation symbols in the proof input and output file formats,
    #  so we can just dump any characters from the first globalConfig.COMMENT_MARKER character
    #  found.
    try:
        return s[:s.index(gc.COMMENT_MARKER)]
    except ValueError:
        return s

def flatten(l, ltypes=(list, tuple)):
    """
    Flattens the iterable l (in place if mutable)
    For example, flatten(["first",["second","third"],[["fourth"]]])
    returns ["first", "second", "third", "fourth"].
    Lifted from http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
    """
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

