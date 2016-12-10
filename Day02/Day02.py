DATA_FILENAME = "data.txt"
PAD_CHAR = -1
moveDirs = {"U":0, "R":1, "D":2, "L":3}
deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def padGrid(grid):
    def padRow(row, maxLenPaddedRow):
        rowPadding = [PAD_CHAR]*((maxLenPaddedRow-len(row))//2)
        return rowPadding + row + rowPadding
    maxLenPaddedRow = max(len(row) for row in grid) + 2
    fullyPaddedRow = [PAD_CHAR] * maxLenPaddedRow
    return [fullyPaddedRow] + [padRow(row, maxLenPaddedRow) for row in grid] + [fullyPaddedRow]

def getCode(lines, grid, initR, initC):
    paddedGrid = padGrid(grid)
    r = initR + 1
    c = initC + paddedGrid[initR].count(PAD_CHAR)//2
    code = ""
    for line in lines:
        for move in line:
            deltaR, deltaC = deltas[moveDirs[move]]
            if (paddedGrid[r+deltaR][c+deltaC]) != PAD_CHAR:
                r+=deltaR
                c+=deltaC
        code += str(paddedGrid[r][c])
    return code

data = open(DATA_FILENAME).read()
lines = data.strip().split()
print(getCode(lines, [[1,2,3],[4,5,6],[7,8,9]], 1, 1))
print(getCode(lines, [[1],[2,3,4],[5,6,7,8,9],['A','B','C'],['D']], 2, 0))