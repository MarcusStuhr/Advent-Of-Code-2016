from hashlib import md5
from itertools import count
from collections import deque, defaultdict
import re

SALT = "yjdafjpo"
VALID_REPEATABLE_CHARSPACE = "0123456789abcdef"
TARGET_PAD_KEY_COUNT = 64
NUM_PEEK_AHEAD = 1000
NUM_REPS_FIRST, NUM_REPS_SECOND = 3, 5
NUM_KEY_STRETCHES = 2016

def getHash(salt, index, numKeyStretchIterations):
    hash = md5(str(salt + str(index)).encode()).hexdigest()
    for stretchIndex in range(numKeyStretchIterations):
        hash = md5(hash.encode()).hexdigest()
    return hash

def resolveKCounts(counts, k, hash, index):
    for chKey in VALID_REPEATABLE_CHARSPACE:
        counts[index][chKey] = counts[index - 1][chKey] + (chKey * k in hash)

def findIndexOneTimePadKey(salt, targetPadKeyCount, numPeekAhead, numKeyStretchIterations = 0):
    padsFound = 0
    rollingCache = deque([getHash(salt, index, numKeyStretchIterations) for index in range(numPeekAhead)])
    quintCounts = defaultdict(lambda : defaultdict(int))
    for hashIndex, hash in enumerate(rollingCache):
        resolveKCounts(quintCounts, NUM_REPS_SECOND, hash, hashIndex)
    for index in count(0):
        hash  = rollingCache[0]
        peekHash = getHash(salt, index + numPeekAhead, numKeyStretchIterations)
        rollingCache.append(peekHash)
        resolveKCounts(quintCounts, NUM_REPS_SECOND, peekHash, index + numPeekAhead)
        trip = re.search(r"(\w){}".format("\\1" * (NUM_REPS_FIRST - 1)), hash)
        if trip:
            chKey = trip.group()[0]
            if quintCounts[index + numPeekAhead][chKey] > quintCounts[index][chKey]:
                padsFound += 1
                if (padsFound == targetPadKeyCount):
                    return index
        del quintCounts[index]
        rollingCache.popleft()

print(findIndexOneTimePadKey(SALT, TARGET_PAD_KEY_COUNT, NUM_PEEK_AHEAD))
print(findIndexOneTimePadKey(SALT, TARGET_PAD_KEY_COUNT, NUM_PEEK_AHEAD, NUM_KEY_STRETCHES))