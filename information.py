"""A set of utilities for measuring information and collecting statistics
   useful for measuring information."""

import os
import sys
import string
import math
import random
import copy
import globalConfig as gc

def uniqueTokens(d):
    """Takes a dictionary and returns a set of all unique
       tokens appearing in the values (assumed to be lists)."""
    allTokens = set([])
    for k in d:
        allTokens = allTokens | set(d[k])
    return allTokens

def tallyTokens(d):
    """Takes a dictionary and returns a dictionary.
       Returned dictionary is each token as a key,
       value is the total number of occurrences of
       that token."""
    allTokens = uniqueTokens(d)
    tally = {}
    for token in allTokens:
        tally[token] = 0
    for k in d:
        for token in d[k]:
            tally[token] += 1
    return tally

def totalTokens(d):
    """Takes a dictionary and returns an integer.
       Integer is the total number of tokens appearing
       in the dictionary."""
    total = 0
    for k in d:
        total += len(d[k])
    return total    

def probTokenDict(d):
    """Takes a dictionary and returns a dictionary.
       Dictionary contains each token as a key,
       the value is the probability that a randomly
       selected token will be that one."""
    allTokens = uniqueTokens(d)
    tally = tallyTokens(d)
    total = totalTokens(d)
    probDict = {}
    for k in tally:
        probDict[k] = float(tally[k]) / float(total)
    return probDict

def tokenPairTally(d):
    """Takes a dictionary and returns a nested dictionary.
       For each token1, token2 in dictionary, it returns
       a dictionary d where d[token1][token2] is the total
       number of documents in which token1 and token2 both
       occur. If token1, token2 aren't in the output, then 
       they never occur together."""
    tokenProb = probTokenDict(d)
    tokenList = uniqueTokens(d)
    jointTally = {}
    for k in d.keys():
        for token1 in d[k]:
            for token2 in d[k]:
                if token2 <= token1: continue
                if not token1 in jointTally: jointTally[token1] = {}
                if not token2 in jointTally[token1]: jointTally[token1][token2] = 0
                jointTally[token1][token2] += 1    
    return jointTally

def jointProbDict(d):
    """Takes a dictionary and returns a nested dictionary.
       Like tokenPairTally, but instead of a tally, it returns
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
       Takes a dictionary and returns a nested dictionary.
       d[token1][token2] is the MIC score for each token pair.
       Note that MIC is symmetric."""
    jointProb = jointProbDict(d)
    tokenProb = probTokenDict(d)
    tokenList = uniqueTokens(d)
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
       Dictionary keys are tokens, values are a sum
       over all the MIC scores for that token and each
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

def nestedDictThreshold(d, thresholdValue = .1):
    """Takes a nested dictionary d where d[k1][k2]
       is assumed to be a number. Returns the value for
       the top "thresholdValue"."""
    values = []
    for k1 in d:
        for k2 in d[k1]:
            values.append(d[k1][k2])
    values.sort()
    values.reverse()
    ind = int(float(len(values)) * thresholdValue)
    out = values[ind]
    return out

def pruneNestedDictByThreshold(d, thresholdValue = .1):
    """Takes a nested dictionary where d[k1][k2] is 
       assumed to be a number. Prunes the dictionary
       so that every value is in the top "thresholdValue"
       of values from the original dictionary."""
    d1 = copy.deepcopy(d)
    threshold = nestedDictThreshold(d1, thresholdValue = thresholdValue)
    for k1 in d:
        for k2 in d[k1]:
            if d1[k1][k2] < threshold: del(d1[k1][k2])
    return d1
