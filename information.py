"""A set of utilities for measuring information and collecting statistics
   useful for measuring information.
   
   Many functions are intended to take as input a token-dictionary, which is a
   dict whose values are sequences (typically lists)
   of (not necessarily distinct) tokens."""

import math
import copy

def uniqueTokens(d):
    """Takes as input a token-dictionary d, and returns a set of every
    distinct token appearing somewhere in d's values."""
    allTokens = set([])
    for k in d:
        allTokens |= set(d[k]) #  Add d[k]'s tokens to allTokens
    return allTokens

def tallyTokens(d):
    """Takes as input a token-dictionary d, and returns a dictionary
       where each key k is a token in one of d's sequences and each value of k
       is an int representing the total number of occurrences of the token k
       appearing in d's sequences."""
    allTokens = uniqueTokens(d)
    tally = {}
    for token in allTokens:
        tally[token] = 0
    for k in d:
        for token in d[k]:
            tally[token] += 1
    return tally

def totalTokens(d):
    """Takes as input a token-dictionary d and returns the total number of
    (not necessarily distinct) tokens appearing somewhere in d's sequences."""
    total = 0
    for k in d:
        total += len(d[k])
    return total

def probTokenDict(d):
    """Takes as input a token-dictionary d and returns a dictionary
    where each key k is a token in one of d's sequences and each value of k
    is a float representing the probability that a randomly selected token is k."""
    #  allTokens = uniqueTokens(d)
    tally = tallyTokens(d)
    total = totalTokens(d)
    probDict = {}
    for k in tally:
        probDict[k] = float(tally[k]) / float(total)
    return probDict

def tokenPairTally(d):
    """Takes as input a token-dictionary d and returns a nested dictionary.
       For each token1, token2 in dictionary d, it returns
       a dictionary jointTally where jointTally[token1][token2] is the total
       number of documents (sequences of d?) in which token1 and token2 both
       occur. If token1, token2 aren't in the output, then 
       they never occur together."""
    #  tokenProb = probTokenDict(d)
    #  tokenList = uniqueTokens(d)
    jointTally = {}
    for k in d.keys():
        for token1 in d[k]:
            for token2 in d[k]:
                if token2 <= token1: continue #  TODO: Question: Why '<=' ?
                #  Don't want to double count, but are the other functions that call tokenPairTally
                #  accounting for this fact? Could one use instead unordered pairs {token1, token2} ?
                if not token1 in jointTally: jointTally[token1] = {}
                if not token2 in jointTally[token1]: jointTally[token1][token2] = 0
                jointTally[token1][token2] += 1
    return jointTally

def jointProbDict(d):
    """Takes as input a token-dictionary d and returns a nested dictionary
       like tokenPairTally, but instead of a tally, it returns
       a probability.
       Check to make sure the probability makes sense..."""
    jointTally = tokenPairTally(d)
    jointProbabilities = {}
    for k1 in jointTally:
        jointProbabilities[k1] = {}
        for k2 in jointTally[k1]:
            jointProbabilities[k1][k2] = jointTally[k1][k2] / float(len(jointTally))
    return jointProbabilities

def jointInformationDict(d):
    """Calculates the mutual information criterion for each
       pair of co-occurring tokens in d.
       Takes a dictionary d and returns the nested dictionary infoDict.
       infoDict[token1][token2] is the MIC score for each token pair.
       Note that MIC is symmetric."""
    jointProb = jointProbDict(d)
    tokenProb = probTokenDict(d)
    #  tokenList = uniqueTokens(d)
    infoDict = {}
    for token1 in jointProb:
        infoDict[token1] = {}
        for token2 in jointProb[token1]:
            dependent = jointProb[token1][token2]
            independent = tokenProb[token1] * tokenProb[token2]
            jointInfo = dependent * math.log(dependent / independent)
            infoDict[token1][token2] = jointInfo
    return infoDict

def tokenInfoDict(d):
    """Takes a dictionary and returns a dictionary.
       Dictionary keys are tokens, values are the sum
       of all MIC scores for that token and each
       other token that co-occurs with it."""
    jointInfo = jointInformationDict(d)
    tokenList = uniqueTokens(d)
    tokenInfo = {}
    for token in tokenList: tokenInfo[token] = 0.
    for token1 in jointInfo:
        for token2 in jointInfo[token1]:
            tokenInfo[token1] += jointInfo[token1][token2]
            tokenInfo[token2] += jointInfo[token1][token2]
    return tokenInfo

def nestedDictThreshold(d, thresholdValue=.1):
    """Takes a nested dictionary d where d[k1][k2]
       is assumed to be a number. Returns the value for
       the top "thresholdValue"."""
    values = []
    for k1 in d:
        for k2 in d[k1]:
            values.append(d[k1][k2])
    values.sort(reverse=True)
    ind = int(float(len(values)) * thresholdValue)
    out = values[ind] #  TODO: This will crash when values is []. Need a default!
    return out

def pruneNestedDictByThreshold(d, thresholdValue=.1):
    """Takes a nested dictionary where d[k1][k2] is
       assumed to be a number. Returns a pruned copy of the dictionary
       where every value is in the top "thresholdValue"
       of values from the original dictionary."""
    d1 = copy.deepcopy(d)
    threshold = nestedDictThreshold(d1, thresholdValue=thresholdValue)
    for k1 in d:
        for k2 in d[k1]:
            if d1[k1][k2] < threshold: del d1[k1][k2]
    return d1

