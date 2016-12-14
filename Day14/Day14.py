from hashlib import md5
from itertools import count
import re

SALT = "yjdafjpo"
TARGET_PAD_KEY_COUNT = 64
NUM_PEEK_AHEAD = 1000

def getHash(salt, index, numKeyStretchIterations, memo = {}):
    memoKey = (salt, index, numKeyStretchIterations)
    if memoKey in memo:
        return memo[memoKey]
    hash = md5(str(salt + str(index)).encode('utf-8')).hexdigest()
    for stretchIndex in range(numKeyStretchIterations):
        hash = md5(hash.encode('utf-8')).hexdigest()
    memo[memoKey] = hash
    return hash

def getRepMatch(hash, numReps, memo = {}):
    memoKey = (hash, numReps)
    if memoKey in memo:
        return memo[memoKey]
    pattern = r"(\w){}".format("\\1" * (numReps - 1))
    matchObject = re.search(pattern, hash)
    memo[memoKey] = matchObject
    return matchObject

def findIndexOneTimePadKey(salt, targetPadKeyCount, numPeekAhead, numKeyStretchIterations = 0):
    padsFound = 0
    for index in count(0):
        hash = getHash(salt, index, numKeyStretchIterations)
        trip = getRepMatch(hash, 3)
        if trip:
            tripChar = trip.group()[0]
            for peekIndex in range(1, numPeekAhead + 1):
                newHash = getHash(salt, index + peekIndex, numKeyStretchIterations)
                quint = getRepMatch(newHash, 5)
                if quint and quint.group()[0] == tripChar:
                    padsFound += 1
                    if padsFound == targetPadKeyCount:
                        return index

print(findIndexOneTimePadKey(SALT, TARGET_PAD_KEY_COUNT, NUM_PEEK_AHEAD))
print(findIndexOneTimePadKey(SALT, TARGET_PAD_KEY_COUNT, NUM_PEEK_AHEAD, 2016))