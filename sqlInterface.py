"""This is a set of utilities for making it easier to interface with MySQL,
which is where all the proofs and input files will live.

Table structure in prover9nudge database:
    proofs:
        rawproof mediumtext (text output of proof)
        clauselist mediumtext (list of clauses -- python object)
"""

import mysql.connector
import hashlib
import globalConfig as gc
#  import cPickle as pickle
import pickle

def hashString(s):
    out = hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
    return out

def makeQuery(tableName, columnList, whereColumn=None, whereOperator=' = ', whereCondition=None, limit=None):
    """Takes a TABLENAME, list of COLUMNS, and some options, and returns a string.
       String is the SQL query."""
    columns = ', '.join(columnList)
    query = """SELECT %s FROM %s""" % (columns, tableName,)
    if whereColumn != None and whereCondition != None:
        tmp = """ WHERE %s %s %s""" % (whereColumn, whereOperator, whereCondition,)
        query += tmp
    if limit != None:
        tmp = """ LIMIT %s""" % (str(limit),)
        query += tmp
    query += ';'
    return query

def executeQuery(query):
    """Takes a query (string), executes it in MySQL.
       Returns a list of results."""
    gc.CURSOR.execute(query)
    results = []
    result = gc.CURSOR.fetchone()
    while result != None:
        #  print result
        results.append(result)
        result = gc.CURSOR.fetchone()
    return results

def queryDict(tableName, columnList, whereColumn=None, whereOperator=' = ', whereCondition=None, limit=None):
    query = makeQuery(tableName, columnList, whereColumn=whereColumn, whereOperator=whereOperator, whereCondition=whereCondition, limit=limit)
    queryResults = executeQuery(query)
    results = []
    for result in queryResults:
        d = {}
        for ind in range(len(columnList)):
            d[columnList[ind]] = result[ind]
            d = convertDictFrom64(d)
        results.append(d)
    return results

def makeInsert(tableName, columnList, values, encodeList=[]):
    """insert into outputfiles (id, hash) values (1123123, 'foo');"""
    query = "INSERT IGNORE INTO %s " % tableName
    columns = '('
    for column in columnList:
        columns += column
        if column != columnList[-1]: columns += ', '
    columns += ') '
    query += columns
    query += 'VALUES '
    columns = '('
    for ind in range(len(values)):
        value = values[ind]
        column = columnList[ind]
        if column in encodeList:
            value = toHex(pickle.dumps(value))
        if type(value) == str:
            value = '"' + value + '"'
        else:
            value = str(value)
        columns += value
        if ind != len(values) - 1:
            columns += ', '
    columns += ');'
    query += columns
    return query

def convertFrom64(s):
    try:
        out = fromHex(s)
    except:
        out = s
    return out

def convertDictFrom64(d):
    out = {}
    for key in d.keys():
        out[key] = pickle.loads(convertFrom64(d[key]))
    return out

def insertValues(tableName, columnList, values, encodeList=[]):
    query = makeInsert(tableName, columnList, values, encodeList=encodeList)
    gc.CURSOR.execute(query)
    gc.CURSOR.execute('commit;')

def insertDict(tableName, d, encodeList):
    columnList = []
    values = []
    for columnName in d.keys():
        columnList.append(columnName)
        values.append(d[columnName])
    insertValues(tableName, columnList, values, encodeList)

def toHex(s):
    b = s.encode('base64')
    b = b.strip()
    return b

#  I don't think this right...
def fromHex(s):
    """Takes a string and returns a string.
       Converts the string to base64 for the purpose of getting rid of
       and nasty special characters."""
    b = s.decode('base64')
    return b

#  insertValues('proofs', ['rawproof', 'clauselist'], ['imaproof', ['foo1', 'foo2']], encodeList = ['rawproof', 'clauselist'])

#  print makeInsert('thisisthetable', ['a', 'b', 'c'], [1, 'foo', 'goo'], encodeList = ['a', 'c'])
#  s = 'The quick brown fox...'
#  print toHex(s)
#  print fromHex(toHex(s))
#  exit()
#  print queryDict('proofs', ['rawproof', 'clauselist'])
