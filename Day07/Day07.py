import re

DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")

def isAbba(line):
    return len(line)==4 and line[0]==line[3] and line[1]==line[2] and line[0]!=line[1]

def isAba(line):
    return len(line)==3 and line[0]==line[2] and line[0]!=line[1]

def getNets(line):
    splitline = re.split("\[|\]", line)
    supernets, hypernets = splitline[::2], splitline[1::2]
    return supernets, hypernets

def getChunks(line, chunkSize):
    for i in range(0, len(line)-chunkSize+1):
        yield line[i:i+chunkSize]

def isTLS(line):
    supernets, hypernets = getNets(line)
    return any(isAbba(chunk) for supernet in supernets for chunk in getChunks(supernet, 4)) \
            and all(isAbba(chunk) == False for hypernet in hypernets for chunk in getChunks(hypernet, 4))

def isSSL(line):
    supernets, hypernets = getNets(line)
    for supernet in supernets:
        for chunk in getChunks(supernet, 3):
            if isAba(chunk) and any(chunk[1] + chunk[0] + chunk[1] in hypernet for hypernet in hypernets):
                return True
    return False

def countTLS(lines):
    return sum(isTLS(line) for line in lines)

def countSSL(lines):
    return sum(isSSL(line) for line in lines)

print(countTLS(lines)) #part 1 answer
print(countSSL(lines)) #part 2 answer