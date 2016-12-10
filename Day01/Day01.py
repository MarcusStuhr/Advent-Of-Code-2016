DATA_FILENAME = "data.txt"
turnDirs = {"L":-1,"R":1}
deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def getLocation(moves, aocPart):
    dirFacing = 0
    x = 0
    y = 0
    visited = set()
    visited.add((x,y))
    for turnDir, amtToMove in moves:
        dirFacing = (dirFacing + turnDirs[turnDir]) % 4
        deltaX, deltaY = deltas[dirFacing]
        for i in range(1, amtToMove + 1):
            x += deltaX
            y += deltaY
            if aocPart == 2 and (x,y) in visited:
                return abs(x) + abs(y)
            visited.add((x,y))
    if aocPart == 1:
        return abs(x) + abs(y)
    return None

data = open(DATA_FILENAME).read()
lines = data.strip().split(", ")
moves = [(line[0], int(line[1:])) for line in lines]

print(getLocation(moves, 1)) #part 1 answer
print(getLocation(moves, 2)) #part 2 answer