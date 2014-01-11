"""Class for defining and processing unit clauses..."""

import os
import sys
import string
import cPickle as pickle
import hashlib
import globalConfig as gc

class UnitClause:
    """Class for defining unit clauses and related methods.
       Non-unit clauses will be built from this class.
    """
    original = ''                # Unprocessed string
    originalPrefix = False       # Is the original in prefix notation?
    originalInfix = False        # Is the original in infix notation?
    prefix = ''                  # Prefix form of the formula
    infix = ''                   # Infix form of the formula
    functions = []               # List of functions appearing in the formula
    variables = []               # List of variables appearing in the formula
    predicate = ''               # The predicate (if any)
    arities = {}                 # Dictionary mapping functions and predicate to arities
    canonicalized = []           # Canonicalized formula with generic functions, etc.
    canonicalizedDictionary = {} # Dictionary used to generate canonical form
    listCategory = None          # SOS, hints, usable, etc. (if applicable)
    negated = False              # Is the unit clause negated?
    hashKey = ''

    def __init__(self, s):
        self.original = s
        self.original = self.original.strip()
        self.original = self.original.replace('.', '')
        if not self.isInfix(): self.prefix = self.original
        self.findFunctions()
        self.findVariables()
        self.findPredicate()
        self.isNegated()
        pickleString = pickle.dumps(self)
        self.hashKey = hashlib.sha224(pickleString).hexdigest()
        self.functionArities()
        self.canonicalize()

    def canonicalize(self):
        """Generate a list of symbols, using canonical forms for the functions, 
           predicates, and variables. May have to rethink this in order to handle
           non-unit clauses. We can use the replacement dictionary to compose one
           replacement function with the inverse of the other, in order to do a 
           cheap unification of two unit clauses."""
        tokenList = self.toList()
        replacementDict = {}
        canonicalList = []
        variableCounter = 0
        functionCounter = 0
        predicateCounter = 0
        for token in tokenList:
            if token in replacementDict:
                canonicalList.append(replacementDict[token])
            elif token in self.variables:
                replacement = ':VARIABLE:' + str(variableCounter) + ':'
                replacementDict[token] = replacement
                canonicalList.append(replacement)
                variableCounter += 1
            elif token in self.functions:
                replacement = ':FUNCTION:' + str(functionCounter) + ':'
                replacementDict[token] = replacement
                canonicalList.append(replacement)
                functionCounter += 1
            elif token == self.predicate:
                replacement = ':PREDICATE:' + str(predicateCounter) + ':'
                replacementDict[token] = replacement
                canonicalList.append(replacement)
                predicateCounter += 1
            else:
                canonicalList.append(token)
        self.canonicalized = canonicalList
        self.canonicalizedDictionary = replacementDict

    def parse(self):
        """Do all the parsing, arity-finding, and so on to populate the object's
           fields.
        """
        pass

    def toList(self):
        """Translate a formula into a list of tokens."""
        delimiters = ['-', ',', '(', ')', '.']
        delimited = self.prefix
        for delimiter in delimiters:
            delimited = delimited.replace(delimiter, ' ' + delimiter + ' ')
        while '  ' in delimited: delimited = delimited.replace('  ', ' ')
        delimited = delimited.split()
        return delimited

    def functionArities(self):
        """Return a dictionary mapping functions and predicates to their arities."""
        tmp = self.toList()
        #print tmp, self.variables
        delimited = []
        for i in tmp:
            if i == '-': continue
            if i in self.variables: delimited.append(gc.JUNK_SYMBOL)
            else: delimited.append(i)
        allFunctions = list(set(self.functions) | set([self.predicate]))
        arityDict = {}
        while len(delimited) > 3:
            #print delimited
            i = 0
            while i < len(delimited) - 0:
                if not delimited[i] in set(self.functions) and delimited[i] != self.predicate:
                    i += 1
                    continue
                j = i + 1
                while delimited[j] != ')': j += 1
                symbols = set(delimited[i + 1:j + 1]) - set(self.variables)
                symbols = symbols - set(['(', ')'])
                if symbols != set([gc.JUNK_SYMBOL]) and symbols != set([gc.JUNK_SYMBOL, ',']):
                    i += 1
                    continue
                arityDict[delimited[i]] = delimited[i:j + 1].count(gc.JUNK_SYMBOL)
                delimited = delimited[:i] + [gc.JUNK_SYMBOL] + delimited[j + 1:]
                i += 1
        self.arities = arityDict
                
    def prettyPrint(self):
        """Print the UnitClause:"""
        print 'original string: ', self.original
        print 'prefix form:     ', self.prefix
        print 'infix form:      ', self.infix
        print 'functions:       ', self.functions
        print 'variables:       ', self.variables
        print 'predicate:       ', self.predicate
        print 'list category:   ', self.listCategory
        print 'arities:         ', self.arities
        print 'canonicalized:   ', self.canonicalized
        print 'replacement dict:', self.canonicalizedDictionary
        print 'negated:         ', self.negated
        print 'hash key:        ', self.hashKey

    def setOriginal(self, originalString):
        """Set the value of self.original. Will be used to record the original,
           unprocessed string (stripped of whitespace).
        """
        s = ''
        for c in originalString:
            if not c in string.whitespace: self.original += c

    def isPrefix(self):
        """Test whether the original string representation is prefix."""
        pass

    def isInfix(self):
        """Test whether the original string representation is infix."""
        sentinal = False
        for function in gc.BUILT_IN_FUNCTIONS:
            if ')' + function in self.original: sentinal = True
            if function + '(' in self.original: sentinal = True
        self.originalInfix = True
        return sentinal

    def infixToPrefix(self):
        pass

    def findVariables(self):
        """Create list of variables appearing in the formula. Assume the formula
           has been processed into prefix notation."""
        delimiters = [',', '(', ')']
        tmp = self.prefix
        for delimiter in delimiters:
            tmp = tmp.replace(delimiter, ' ' + delimiter + ' ')
        while '  ' in tmp: tmp = tmp.replace('  ', ' ')
        l = tmp.split()
        #print 'l:', l
        variableList = []
        for i in range(1, len(l) - 1):
            before = l[i - 1]
            during = l[i]
            after = l[i + 1]
            #print 'BDA:', before, during, after
            if before == ',' and after == ',':
                variableList.append(during)
                #print 'added variable:', during
            if before == ',' and after == ')':
                variableList.append(during)
                #print 'added variable:', during
            if before == '(' and after == ')':
                variableList.append(during)
                #print 'added variable:', during
            if before == '(' and after == ',':
                variableList.append(during)
                #print 'added variable:', during
        variableList = list(set(variableList))
        self.variables = variableList

    def findFunctions(self):
        """Create list of functions appearing in the formula. Assume the formula
           has been processed into prefix notation."""
        tmp = self.prefix
        tmp = tmp.replace(',', ' , ')
        tmp = tmp.replace(')', ' ) ')
        tmp = tmp.replace('(', ' ( ')
        while '  ' in tmp: tmp = tmp.replace('  ', ' ')
        l = tmp.split()
        functions = []
        for i in range(1, len(l) - 2):
            before = l[i - 1]
            during = l[i]
            after = l[i + 1]
            if before == '(' and after == '(':
                functions.append(during)
            if before == ',' and after == '(':
                functions.append(during)
        functions = list(set(functions))
        self.functions = functions

    def findPredicate(self):
        """Unless there's an equality, a predicate will always be the first symbol
           before an open parenthesis."""
        parenIndex = self.original.index('(')
        predicate = self.original[:parenIndex]
        if '-' in predicate: predicate = predicate.replace('-', '')
        self.predicate = predicate.strip()

    def hasEquality(self):
        """Highly complex function."""
        return '=' in self.original

    def isNegated(self):
        """Test whether the unit clause is negated."""
        tmp = self.prefix
        tmp = tmp.strip()
        if tmp[0] == '-': self.negated = True
        else: self.negated = False

def hasSequentialNames(l):
    returnIndex = None
    for index in range(len(l) - 1):
        firstSymbol = l[index]
        secondSymbol = l[index + 1]
        if not firstSymbol in gc.BUILT_IN_FUNCTIONS and (
            not firstSymbol in gc.PARENTHESES and 
            not secondSymbol in gc.BUILT_IN_FUNCTIONS and
            not secondSymbol in gc.PARENTHESES):
            returnIndex = index
    return returnIndex

infixExpression = '(((2+(3*4))-51)=6)'
infixList = [c for c in infixExpression]
print 'original infix:', infixList
print 'sequential:', hasSequentialNames(infixList)
infixList.reverse()
stack = []
prefixList = []
for token in infixList: # scanning from right to left, effectively
    print 'token:', token
    if token == ')':
        stack.append(token)
    elif token in string.digits:
        print 'adding to prefixList:', token
        prefixList.append(token)
    elif token in gc.BUILT_IN_FUNCTIONS:
        stack.append(token)
    elif token == '(':
        try:
            prefixList.append(stack.pop())
            stack.pop()
        except IndexError:
            pass

print infixList
prefixList.reverse()
print infixExpression
print prefixList
