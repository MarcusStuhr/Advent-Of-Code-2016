from collections import deque

FAVE_NUM = 1362
WALL_CHAR = '#'
OPEN_CHAR = '.'
IMPOSSIBLE_DIST = float('inf')

def f(x, y, memo = {}):
    key = (x,y)
    if key in memo: return memo[key]
    memo[key] = [OPEN_CHAR, WALL_CHAR][bin(x*x + 3*x + 2*x*y + y + y*y + FAVE_NUM).count('1') % 2]
    return memo[key]

def BFS(initialPos, goalPos, distMax = None):
    q = deque()
    q.append((initialPos, 0))
    visited = set()
    posWithinDistMax = set()
    while q:
        curPos, dist = q.popleft()
        if curPos == goalPos:
            return (dist, posWithinDistMax)
        if distMax != None and dist <= distMax:
            posWithinDistMax.add(curPos)
        if curPos not in visited:
            visited.add(curPos)
            y, x = curPos
            for deltaY, deltaX in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                newY, newX = y + deltaY, x + deltaX
                if 0 <= newY and 0 <= newX \
                    and f(newX, newY) == OPEN_CHAR \
                    and (newY, newX) not in visited:
                        q.append(((newY, newX), dist + 1))
    return (IMPOSSIBLE_DIST, posWithinDistMax)

print(BFS((1, 1), (39, 31))[0]) #part 1 answer
print(len(BFS((1, 1), None, 50)[1])) #part 2 answer
