from collections import Counter
import re, string

DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")
realIdSum = 0
northPoleSectorId = -1
az = string.ascii_lowercase

for line in lines:
    pattern = r"([a-z-]+)(\d+)\[(\w+)\]"
    encryptedName, sectorId, checksum  = re.findall(pattern, line)[0]
    encryptedNameNoDash, sectorId = encryptedName.replace("-", ""), int(sectorId)
    freqLetters = ''.join(letter for letter, freq in sorted(Counter(encryptedNameNoDash).most_common(), key = lambda x : (-x[1], x[0])))[:5]
    if freqLetters == checksum:
        realIdSum+=sectorId
        shift = sectorId % len(az)
        if "north" in encryptedNameNoDash.translate(str.maketrans(az, az[shift:] + az[:shift])):
            northPoleSectorId = sectorId

print(realIdSum) #Part 1 answer
print(northPoleSectorId) #Part 2 answer