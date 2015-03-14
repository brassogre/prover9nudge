"""For reading and parsing Prover9 input and output files."""

import os
import gzip
import hashlib
import random
import collections
import globalConfig as gc
import sqlInterface
import textUtilities as util
import clause as ladrClause

def isOutputFile(fileName):
    """Returns True if it's an output file with a proof."""
    return gc.PROOF_START in readFile(fileName)

def isInputFile(fileName):
    """Returns True if it's an input file (i.e. has at least
       one list we typically find in an input file)."""
    f = readFile(fileName)
    return  gc.SEARCH_STRING not in f and \
            gc.SOS_START in f or \
            gc.USABLE_START in f or \
            gc.GOALS_START in f or \
            gc.ASSUMPTIONS_START in f

def determineFile(fileName):
    """Tests whether fileName contains proofs. If it does, call readOutputFile;
       if it doesn't, call readInputFile."""
    if isOutputFile(fileName):
        return readOutputFile(fileName)
    if isInputFile(fileName):
        return readInputFile(fileName)
    return None

def readOutputFile(fileName):
    """Given the name of a file containing proofs, returns
       a list of lists of NonUnitClauses."""
    proofs = []
    inProof = False
    lines = readFile(fileName).splitlines()
    for line in lines:
        if '&' in line: continue
        if '<->' in line: continue
        if '->' in line: continue
        if util.allWhitespace(line): continue
        if '(all' in line: continue
        if '(exists' in line: continue
        if gc.PROOF_START in line:
            inProof = True
            oneProof = []
            continue
        if gc.PROOF_END in line:
            inProof = False
            proofs.append(oneProof)
        if inProof and '.' in line:
            raw_clause = extractClauseFromLine(line) #  here
            if len(raw_clause) > 5:
                one_clause = ladrClause.Clause(raw_clause)
                oneProof.append(one_clause)
    return proofs

def extractClauseFromLine(line):
    line = line.split('#')[0] #  Discard all labels
    line = line.split(gc.COMMENT_MARKER)[0] #  Discard all comments
    if r'$' in line: return '' #  Abort with empty string if a $ appears in the line.
    line = line.strip() #  Discard any remaining whitespace
    if '[' in line and ']' in line: #  Discard anything in square brackets (inclusive)
        line = line[:line.index('[')] + line[line.rindex(']') + 1:]
    #  Discard any numeric substrings that are separated from
    #  the rest of the string by whitespace.
    line = line.split()
    line = [i for i in line if not util.allDigits(i)]
    line = ' '.join(line)
    #  Discard all periods
    line = ''.join([c for c in line if not c == gc.END_OF_STATEMENT])
    line = line.strip() #  Discard any remaining whitespace
    line = line + gc.END_OF_STATEMENT #  Insert a period at the end of the line.
    if len(line) > 3:
        return line
    return ''

def readFile(fileName):
    """Returns a string for the supplied text file, fileName.
    This function does not catch any IO exceptions."""
    #  Ascertain the correct function for opening fileName depending on
    #  whether it is compressed.
    openfunc = ('gz' == fileName[-2:]) and gzip.open or open
    #  Return a string containing the contents of the file.
    with openfunc(fileName) as file:
        return file.read()

def readInputFile(fileName):
    """Given the name of an input file, returns a list of 
       NonUnitClauses, including labels for which list the
       clauses were in."""
    allClauses = [] #  TODO: Why is this a list rather than a set? Why is this function called?
    inSos = False
    inUsable = False
    inGoals = False
    #  inAssumptions = False

    lines1 = readFile(fileName).splitlines() #  Construct a list of all lines in the file.
    lines2 = list(map(util.stripComments, lines1)) #  Eliminate comments from every line.
    #  lines3 = [line for line in lines2 if not util.allWhitespace(line)] #  Eliminate empty lines.
    #  Split multiple commands in one element (line) of the list into a list of separate commands.
    #  lines4 = list(map(str.split(gc.END_OF_STATEMENT), lines3))
    lines4 = [s.split(gc.END_OF_STATEMENT) for s in lines2]
    #  Convert the list of separate commands into their own lines.
    lines5 = util.flatten(lines4)
    lines = util.stripWhitespace(lines5) #  Eliminate all whitespace from every line and all empty lines.
    #  TODO: Potential Error:
    #  The for loop below had this next line as one part but also a condition that handles gc.END_OF_LIST in line
    #  lines = [line for line in lines if not gc.END_OF_LIST in line] #  Eliminate lines with 'end_of_list'.

    for statement in lines:
        #  print('sending:', statement)
        statement = extractClauseFromLine(statement)
        #  print('returning:', statement)
        if len(statement) < 5: continue
        #  if gc.ASSUMPTIONS in statement:
            #  inAssumptions = True # Unused
            #  continue
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
            #  inAssumptions = False # Unused
            inSos = False
            inUsable = False
            inGoals = False
            continue
        if inSos or inUsable or inGoals:
            clause = ladrClause.Clause(statement)
            allClauses.append(clause)
    return allClauses

def parseProofFilesInDirectory(directory):
    fileList = [directory + '/' + i for i in os.listdir(directory)]
    for fileName in fileList:
        #  print fileName
        if isOutputFile(fileName):
            #  print '--->', fileName
            parsed = readOutputFile(fileName)
            for one_list in parsed:
                for unit in one_list:
                    unit.prettyPrint()

def makeGraphFromDirectory(directory):
    #  print 'source,target'
    d = collections.defaultdict(list)
    fileList = [directory + '/' + i for i in os.listdir(directory) if 'GRP' in i]
    counter = 0
    for fileName in fileList:#  random.sample(fileList, 1750):
        #  print fileName
        #  related = []
        if isOutputFile(fileName):
            print('--->', fileName, counter)
            counter += 1
            parsed = readOutputFile(fileName)
            for proof in parsed:
                for clause1 in proof:
                    for clause2 in proof:
                        f1 = [[i for i in unit.canonicalized] for unit in clause1.units]
                        f2 = [[i for i in unit.canonicalized] for unit in clause2.units]
                        if len(f1) < 4 or len(f2) < 4: continue
                        s1 = ''.join([''.join([i for i in unit.canonicalized]) for unit in clause1.units])
                        s2 = ''.join([''.join([i for i in unit.canonicalized]) for unit in clause2.units])
                        #  if s1 <= s2: continue
                        h1 = hashlib.sha224(s1).hexdigest()
                        h2 = hashlib.sha224(s2).hexdigest()
                        d[h1].append(h2)
                        d[h2].append(h1)
                        #  print '"' + h1 + '","' + h2 + '"'
    d = dict(d)
    return d


def directoryToSQL(directory):
    #  print 'source,target'
    #  d = collections.defaultdict(list)
    fileList = [directory + '/' + i for i in os.listdir(directory)]
    counter = 0
    for fileName in random.sample(fileList, 1600):
        #  print fileName
        #  related = []
        if isOutputFile(fileName):
            print('--->', fileName, counter)
            counter += 1
            parsed = readOutputFile(fileName)
            rawFile = readFile(fileName)
            #  print rawFile
            proofHash = hashlib.sha224(rawFile).hexdigest()
            print(proofHash)
            sqlInterface.insertValues(gc.MYSQL_PROOFS_TABLE,
                           [gc.MYSQL_PROOF_HASH, gc.MYSQL_RAW_PROOF_COLUMN, gc.MYSQL_PARSED_PROOF_COLUMN], [proofHash, rawFile, parsed],
                           [gc.MYSQL_RAW_PROOF_COLUMN, gc.MYSQL_PARSED_PROOF_COLUMN])

if __name__ == '__main__':
    s1 = '2 P(j(j(x,y),j(j(y,z),j(x,z)))) # label(non_clause) # label(goal).  [goal].'
    print(extractClauseFromLine(s1))
    s2 = '5 -P(j(x,y)) | -P(x) | P(y).  [assumption].'
    print(extractClauseFromLine(s2))
    print()
    outclauses = readOutputFile('./test_files/prop.out')
    for l in outclauses:
        print([c.__str__() for c in l])
    print()
    inclauses = readInputFile('./test_files/prop.in')
    print([c.__str__() for c in inclauses])
    #  directoryToSQL('./ladr_with_proofs')
