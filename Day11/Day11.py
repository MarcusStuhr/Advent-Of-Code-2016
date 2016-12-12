import re
from collections import deque

DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")

def countMinMoves(initialFloors):
    q = deque()
    q.append((initialFloors, 0, 0))
    visited = set()
    while q:
        floors, curFloor, numMoves = q.popleft()
        if all(floors[i] == (0, 0) for i in range(len(floors)-1)):
            return numMoves
        if (tuple(floors), curFloor) not in visited:
            visited.add((tuple(floors), curFloor))
            for floorDelta in (-1, 1):
                nextFloor = curFloor + floorDelta
                if not 0 <= nextFloor < len(floors):
                    continue
                for numGensTake, numChipsTake in [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]:
                    newFloors = list(floors)
                    if newFloors[curFloor][0] - numGensTake < 0 or newFloors[curFloor][1] - numChipsTake < 0:
                        continue
                    newFloors[curFloor] = (newFloors[curFloor][0] - numGensTake, newFloors[curFloor][1] - numChipsTake)
                    newFloors[nextFloor] = (newFloors[nextFloor][0] + numGensTake, newFloors[nextFloor][1] + numChipsTake)
                    if (tuple(newFloors), nextFloor) not in visited and all(g == 0 or g >= m for (g, m) in newFloors):
                        q.append((tuple(newFloors), nextFloor, numMoves + 1))
    return None

floors = [(len(re.findall("([\w]+) generator", line)), len(re.findall("([\w]+)-compatible", line))) for line in lines]

print(countMinMoves(floors)) #part 1 answer
floors[0] = (floors[0][1] + 2, floors[0][1] + 2)
print(countMinMoves(floors)) #part 2 answer