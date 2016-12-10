def getDecompressedLengthUtil(line, startIndex, endIndex, decompressAllMarkers = False):
    decompressedLength = 0
    lineIndex = startIndex
    while lineIndex < endIndex:
        if line[lineIndex] != '(': #if it's a letter
            decompressedLength += 1
            lineIndex += 1
        else:
            lineIndex += 1 #skip '('
            indexRightParen = line.index(')', lineIndex)
            length, repeat = map(int, line[lineIndex:indexRightParen].split('x'))
            lineIndex = indexRightParen + 1
            if decompressAllMarkers:
                decompressedLength += repeat * getDecompressedLengthUtil(line, lineIndex, lineIndex + length, decompressAllMarkers)
            else:
                decompressedLength += repeat * length
            lineIndex += length
    return decompressedLength

def getDecompressedLength(line, decompressAllMarkers = False):
    return getDecompressedLengthUtil(line, 0, len(line), decompressAllMarkers)

DATA_FILENAME = "data.txt"
line = open(DATA_FILENAME).read().strip()

print(getDecompressedLength(line)) #part 1 answer
print(getDecompressedLength(line, True)) #part 2 answer