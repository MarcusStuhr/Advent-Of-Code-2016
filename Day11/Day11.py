import re
from collections import deque

"""
This is the slow, full, limited-pruning BFS approach
TODO: Still optimizing the faster implementation which uses better pruning and state management
"""

DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")

def areValidFloors(floors):
    for floor in floors:
        for item in floor:
            element, itemType = item[0], item[1]
            if itemType == "M":
                if all(x[1]=="M" for x in floor):
                    continue
                if element + "G" not in floor:
                    return False
    return True

def normalizeFloors(floors):
    normalFloors = []
    seen = {}
    index = 0
    for floor in floors:
        normalFloor = []
        for item in sorted(floor):
            element = item[0]
            if element not in seen:
                seen[element] = str(index)
                index+=1
            normalFloor.append(seen[element] + item[1])
        normalFloors.append(tuple(sorted(normalFloor)))
    return normalFloors


def countMinMoves(initialFloors):
    q = deque()
    q.append((normalizeFloors(initialFloors), 0, 0))
    visited = set()
    while q:
        floors, curFloorIndex, numMoves = q.popleft()
        if all(len(floors[i])==0 for i in range(len(floors)-1)):
            return numMoves
        if (tuple(floors), curFloorIndex) not in visited:
            visited.add((tuple(floors), curFloorIndex))
            for floorDelta in (-1, 1):
                nextFloorIndex = curFloorIndex + floorDelta
                if not 0 <= nextFloorIndex < len(floors):
                    continue
                for itemToMove in floors[curFloorIndex]:
                    newFloors = list(floors)
                    newFloors[curFloorIndex] = tuple(item for item in floors[curFloorIndex] if item != itemToMove)
                    newFloors[nextFloorIndex] = tuple(tuple(floors[nextFloorIndex]) + tuple([itemToMove]))
                    newFloors = normalizeFloors(newFloors)
                    if (tuple(newFloors), nextFloorIndex) not in visited and areValidFloors(newFloors):
                        q.append((tuple(newFloors), nextFloorIndex, numMoves + 1))
                for itemToMove1 in floors[curFloorIndex]:
                    for itemToMove2 in floors[curFloorIndex]:
                        if itemToMove1 == itemToMove2:
                            continue
                        newFloors = list(floors)
                        newFloors[curFloorIndex] = tuple(item for item in floors[curFloorIndex] if item != itemToMove1 and item != itemToMove2)
                        newFloors[nextFloorIndex] = tuple(tuple(floors[nextFloorIndex]) + tuple([itemToMove1, itemToMove2]))
                        newFloors = normalizeFloors(newFloors)
                        if (tuple(newFloors), nextFloorIndex) not in visited and areValidFloors(newFloors):
                            q.append((tuple(newFloors), nextFloorIndex, numMoves + 1))
    return None

floors = []
for line in lines:
    floor = []
    for generator in re.findall("([\w]+) generator", line):
        floor.append(generator[0] + "G")
    for microchip in re.findall("([\w]+)-compatible", line):
        floor.append(microchip[0] + "M")
    floors.append(floor)

print(countMinMoves(floors)) #part 1 answer
floors[0] = tuple(tuple(floors[0]) + tuple(["EM", "EG", "DM", "DG"]))
print(countMinMoves(floors)) #part 2 answer