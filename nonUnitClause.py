import os
import sys
import string
import pickle
import unitClause
import cPickle as pickle
import hashlib
import globalConfig as gc 

def allWhiteSpace(s):
    sentinal = True
    for c in s:
        if not c in string.whitespace: sentinal = False
    return sentinal

class NonUnitClause:
    """Class for defining non-unit clauses and related methods.
       Relies heavily on UnitClause class."""
    original = ''
    originalPrefix = False
    originalInfix = False
    prefix = ''
    infix = ''
    functions = []
    variables = []
    predicates = [] # unlike unit clauses, may be more than one
    arities = {}
    canonicalized = []
    canonicalizedDictionary = {}
    listCategory = None
    units = [] # list of disjuncts (instances of unitClause)
    hashKey = ''

    def __init__(self, s):
        self.original = s.replace(' ', '')
        self.original = self.original.replace('.', '')
        self.prefix = self.original # get rid of this later
        self.splitIntoUnits()
        self.findFunctions()
        self.findPredicates()
        self.findVariables()
        pickleString = pickle.dumps(self)
        self.hashKey = hashlib.sha224(pickleString).hexdigest()

    def splitIntoUnits(self):
        unitStrings = self.original.replace(' ', '').split(gc.DISJUNCTION)
        self.units = [unitClause.UnitClause(unitString) for unitString in unitStrings if not allWhiteSpace(unitString)]

    def canonicalize(self):
        functionsDict = {}
        variablesDict = {}
        predicatesDict = {}
        nonUnitString = ''
        unitFunctions = []
        unitVariables = []
        unitPredicates = []
        for unit in self.units:
            nonUnitString = nonUnitString + ' ' + unit.prefix
            unitFunctions += unit.functions
            unitVariables += unit.variables
            unitPredicates.append(unit.predicate)

        for c in ['(', ')', ',']:
            nonUnitString = nonUnitString.replace(c, ' ')
        while '  ' in nonUnitString:
            nonUnitString = nonUnitString.replace('  ', ' ')
        nonUnitString = nonUnitString.strip()
        nonUnitSymbols = nonUnitString.split(' ')
        #print nonUnitSymbols
        for symbol in nonUnitSymbols:
            if symbol in unitFunctions and not symbol in functionsDict:
                functionsDict[symbol] = len(functionsDict)
            if symbol in unitVariables and not symbol in variablesDict:
                variablesDict[symbol] = len(variablesDict)
            if symbol in unitPredicates and not symbol in predicatesDict:
                predicatesDict[symbol] = len(predicatesDict)
        #print unitFunctions, unitVariables, unitPredicates
        #print functionsDict
        #print variablesDict
        #print predicatesDict

    def findFunctions(self):
        tmpFunctions = []
        for unit in self.units:
            tmpFunctions += unit.functions
        self.functions = list(set(tmpFunctions))

    def findPredicates(self):
        tmpPredicates = []
        for unit in self.units:
            tmpPredicates += unit.predicate
        self.predicates = list(set(tmpPredicates))

    def findVariables(self):
        tmpVariables = []
        for unit in self.units:
            tmpVariables += unit.variables
        self.variables = list(set(tmpVariables))

    def prettyPrint(self):
        counter = 0
        for unit in self.units:
            print '==== Unit at position', counter, '===='
            unit.prettyPrint()
            counter += 1
        print 'hash key:      ', self.hashKey

"""
foo = NonUnitClause('P(i(x,f(y))) | Q(x)')
foo.prettyPrint()
foo.canonicalize()
"""
