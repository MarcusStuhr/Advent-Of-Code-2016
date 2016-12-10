DATA_FILENAME = "data.txt"

def convertLinesToColFormat(lines):
    return [[lines[i][j], lines[i+1][j], lines[i+2][j]]
            for i in range(0, len(lines)-2, 3)
            for j in range(len(lines[i]))]

def countValidTriangles(lines, countByCols):
    if countByCols:
        lines = convertLinesToColFormat(lines)
    numValid = 0
    for line in lines:
        a, b, c = sorted(line)
        if a + b > c:
            numValid+=1
    return numValid

lines = open(DATA_FILENAME).read().split("\n")
triangles = [map(int,line.split()) for line in lines]
print(countValidTriangles(triangles, False))
print(countValidTriangles(triangles, True))