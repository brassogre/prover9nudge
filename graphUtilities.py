"""A set of functions relating to graphs and building graphs from dictionaries.

   Graphs are dictionaries. Keys are nodes. Values are lists of nodes."""

import collections
import random
import numpy
import information

def overlapDictionary(d, ordered=False):
    """Takes as input a dictionary d of tokens and returns a dictionary
    where each key k is a unique token in d, and k's value
    is a list of tokens that co-occur with k."""
    tokenList = information.uniqueTokens(d)
    outDict = {}
    for token in tokenList:
        outDict[token] = []
    for k in d:
        for token1 in d[k]:
            for token2 in d[k]:
                if ordered and token2 <= token1: continue
                outDict[token1].append(token2)
    return outDict

def pageRank(d, restartProb=.08, restarts=10000):
    """Takes a dictionary and returns a dictionary.
       Dictionary keys are nodes. Values are PageRank scores."""
    iteration = 0
    counter = 0
    nodeList = d.keys()
    tally = {}
    for node in nodeList: tally[node] = 0
    nowNode = random.choice(nodeList)
    while iteration < restarts:
        tally[nowNode] += 1
        counter += 1
        if random.random() < restartProb:
            nowNode = random.choice(nodeList)
            iteration += 1
            continue
        nowNode = random.choice(d[nowNode])
    for node in tally:
        tally[node] = tally[node] / float(counter)
    return tally

def destinationsFromStart(d, node, pathLength=20, iterations=500):
    """Starting at node, and in paths no longer than pathLength, track
       the number of steps to each node that we eventually wind up on...
       take the average at the end, and return a dictionary. The
       dictionary keys are nodes reachable from node. The values
       are the average path lengths."""
    nowNode = node
    iteration = 0
    tally = {}
    while iteration < iterations:
        iteration += 1
        steps = 0
        while steps < pathLength:
            steps += 1
            nowNode = random.choice(d[nowNode])
            if not nowNode in tally: tally[nowNode] = []
            tally[nowNode].append(steps)
    for k in tally:
        tally[k] = numpy.mean(tally[k])
    return tally

def oneWayCommutes(d, pathLength=20, iterations=100):
    """Repeatedly calls destinationsFromStart. Takes a graph and returns
       a nested dictionary. commuteTimes[node1][node2] is the average
       path length from node1 to node2. The output is used to calculate
       the mean commute time between all pairs of nodes."""
    commuteTimes = {}
    for k in d:
        commuteTimes[k] = destinationsFromStart(d, k, pathLength=pathLength, iterations=iterations)
    return commuteTimes

def meanCommuteTime(d, pathLength=20, iterations=100):
    """Simply adds the one-way path lengths between all pairs of nodes
       to derive the mean commute time between all node pairs."""
    oneWayCommuteTimes = oneWayCommutes(d, pathLength=pathLength, iterations=iterations)
    commuteTimes = collections.defaultdict(dict) #  ##
    for node1 in oneWayCommuteTimes:
        for node2 in oneWayCommuteTimes[node1]:
            if node1 in oneWayCommuteTimes[node2]:
                commute = oneWayCommuteTimes[node1][node2] + oneWayCommuteTimes[node2][node1]
                #  if not node1 in commuteTimes: commuteTimes[node1] = {}
                #  if not node2 in commuteTimes: commuteTimes[node2] = {}
                commuteTimes[node1][node2] = commute
                commuteTimes[node2][node1] = commute
    return dict(commuteTimes)

def toGephi(d, fileName, minimumEdgeWeight=0):
    f = open(fileName, 'w')
    f.write('source,target,weight\n')
    maximum = -10000000
    minimum = 100000000
    for k1 in d:
        for k2 in d[k1]:
            if d[k1][k2] < minimum: minimum = d[k1][k2]
            if d[k1][k2] > maximum: maximum = d[k1][k2]
    print(maximum, minimum)
    for k1 in d:
        for k2 in d[k1]:
            d[k1][k2] = 1. - ((d[k1][k2] - minimum) / (maximum - minimum))
    for k1 in d:
        for k2 in d[k1]:
            s = '"' + k1 + '","' + k2 + '",' + str(d[k1][k2]) + '\n'
            if d[k1][k2] >= minimumEdgeWeight: f.write(s)

