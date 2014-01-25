"""For reading and parsing Prover9 input and output files."""

import os
import sys
import string
import gzip
import globalConfig as gc
import unitClause
import nonUnitClause

def allWhiteSpace(s):
    sentinal = True
    for c in s:
        if not c in string.whitespace: sentinal = False
    return sentinal

def isOutputFile(fileName):
    """Returns True if it's an output file with a proof."""
    if 'gz' == fileName[-2:]:
        f = gzip.open(fileName, 'r')
    else:
        f = open(fileName, 'r')
    sentinal = False
    for line in f:
        if gc.PROOF_START in line:
            #print '++++++++++++++++++++++++'
            sentinal = True
    f.close()
    #print fileName, sentinal
    return sentinal

def isInputFile(fileName):
    """Returns True if it's an input file (i.e. has at least
       one list we typically find in an input file)."""
    f = open(fileName, 'r')
    sentinal = False
    search_string_sentinal = False
    for line in f:
        if gc.SOS_START in line: sentinal = True
        if gc.USABLE_START in line: sentinal = True
        if gc.GOALS_START in line: sentinal = True
        if gc.SEARCH_STRING in line: search_string_sentinal = True
    f.close()
    return (sentinal and not search_string_sentinal)

def readFile(fileName):
    """Tests whether it's got proofs. If it does, call readOutputFile;
       if it doesn't, call readInputFile."""
    out = None
    if isOutputFile(fileName):
        out = readOutputFile(fileName)
    if isInputFile(fileName):
       out = readInputFile(fileName)
    return out

def readOutputFile(fileName):
    """Given the name of a file containing proofs, returns
       a list of lists of NonUnitClauses."""
    if 'gz' == fileName[-2:]:
        f = gzip.open(fileName)
    else:
        f = open(fileName, 'r')
    inProof = False
    proofs = []
    for line in f:
        if '&' in line: continue
        if '<->' in line: continue
        if '->' in line: continue
        if allWhiteSpace(line): continue
        if '(all' in line: continue
        if '(exists' in line: continue
        if '=' in line and not gc.PROOF_START in line and not gc.PROOF_END in line: continue
        if gc.PROOF_START in line:
            inProof = True
            #print 'Im in a proof!'
            oneProof = []
            continue # so that we skip the first line
        if gc.PROOF_END in line:
            inProof = False
            proofs.append([nonUnitClause.NonUnitClause(clause) for clause in oneProof if len(clause) > 1])
        if inProof and '.' in line and line[0] != '%':
            terminatorIndex = line.index('.')
            #print line
            if '#' in line and line.index('#') < terminatorIndex:
                terminatorIndex = line.index('#')
            line = line[:terminatorIndex]
            tokens = line.split()[1:]
            clause = ' '.join(tokens)
            if clause != '$F': oneProof.append(clause)
    return proofs

def readInputFile(fileName):
    """Given the name of an input file, returns a list of 
       NonUnitClauses, including labels for which list the
       clauses were in."""
    f = open(fileName, 'r')
    allClauses = []
    inSos = False
    inUsable = False
    inGoals = False
    for s in f:
        #print s
        line = ''
        # strip out the whitespace
        for c in s:
            if not c in string.whitespace: line += c
        line = line.strip()
        # find comments and strip them out
        if gc.COMMENT_MARKER in line:
            commentStart = line.index(gc.COMMENT_MARKER)
            line = line[:commentStart]
        # split the line with each delimiter
        line = line.split(gc.END_OF_STATEMENT)
        if len(line) < 2: # line doesn't contain a period!
            continue
        for statement in line:
            if len(statement) < 2: continue
            print 'statement:', statement
            if gc.SOS_START in statement: 
                inSos = True
                continue
            if gc.USABLE_START in statement:
                inUsable = True
                continue
            if gc.GOALS_START in statement:
                inGoals = True
                continue
            if gc.END_OF_LIST in statement:
                inSos = False
                inUsable = False
                inGoals = False
                continue
            print '--->', '+'+statement+'+', inSos, inUsable, inGoals
            if not(inSos or inUsable or inGoals):
                continue
            print statement
            unit = nonUnitClause.NonUnitClause(statement)
            if inSos: unit.listCategory = gc.SOS
            if inUsable: unit.listCategory = gc.USABLE
            if inGoals: unit.listCategory = gc.GOALS  
            unit.prettyPrint()
            allClauses.append(unit)
    f.close()
    return allClauses

def parseProofFilesInDirectory(directory):
    fileList = [directory + '/' + i for i in os.listdir(directory)]
    for fileName in fileList:
        #print fileName
        if isOutputFile(fileName):
            print '--->', fileName
            print readOutputFile(fileName)

parseProofFilesInDirectory('./ladr_with_proofs')
