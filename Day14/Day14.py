from hashlib import md5
from itertools import count
from collections import deque, defaultdict
import re

SALT = "yjdafjpo"

def getHash(salt, index, numKeyStretchIterations):
    hash = md5(str(salt + str(index)).encode()).hexdigest()
    for stretchIndex in range(numKeyStretchIterations):
        hash = md5(hash.encode()).hexdigest()
    return hash

def resolveKCounts(counts, k, hash, index):
    for chKey in "0123456789abcdef":
        counts[index][chKey] = counts[index - 1][chKey] + (chKey * k in hash)

def findIndexOneTimePadKey(salt, targetPadKeyCount, numPeekAhead, numRepsFirst, numRepsSecond, numKeyStretchIterations = 0):
    padsFound = 0
    rollingCache = deque([getHash(salt, index, numKeyStretchIterations) for index in range(numPeekAhead)])
    counts = defaultdict(lambda : defaultdict(int))
    for hashIndex, hash in enumerate(rollingCache):
        resolveKCounts(counts, numRepsSecond, hash, hashIndex)
    for index in count(0):
        hash  = rollingCache[0]
        peekHash = getHash(salt, index + numPeekAhead, numKeyStretchIterations)
        rollingCache.append(peekHash)
        resolveKCounts(counts, numRepsSecond, peekHash, index + numPeekAhead)
        curRep = re.search(r"(\w){}".format("\\1" * (numRepsFirst - 1)), hash)
        if curRep:
            chKey = curRep.group()[0]
            if counts[index + numPeekAhead][chKey] > counts[index][chKey]:
                padsFound += 1
                if (padsFound == targetPadKeyCount):
                    return index
        del counts[index]
        rollingCache.popleft()

targetPadKeyCount = 64
numPeekAhead = 1000
numRepsFirst, numRepsSecond = 3, 5
numKeyStretches = 2016

print(findIndexOneTimePadKey(SALT, targetPadKeyCount, numPeekAhead, numRepsFirst, numRepsSecond))
print(findIndexOneTimePadKey(SALT, targetPadKeyCount, numPeekAhead, numRepsFirst, numRepsSecond, numKeyStretches))
