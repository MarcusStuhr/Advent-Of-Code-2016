from collections import deque

FAVE_NUM = 1362
MAZE_SIZE = 100
WALL_CHAR = '#'
OPEN_CHAR = '.'
IMPOSSIBLE_DIST = float('inf')

def f(x,y):
    return [OPEN_CHAR, WALL_CHAR][bin(x*x + 3*x + 2*x*y + y + y*y + FAVE_NUM).count('1') % 2]

def BFS(initialPos, goalPos, maze, distMax = None):
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
                if 0 <= newY < MAZE_SIZE and 0 <= newX < MAZE_SIZE \
                    and maze[newY][newX] == OPEN_CHAR \
                    and (newY, newX) not in visited:
                        q.append(((newY, newX), dist + 1))
    return (IMPOSSIBLE_DIST, posWithinDistMax)

maze = [[f(x, y) for x in range(MAZE_SIZE)] for y in range(MAZE_SIZE)]

print(BFS((1, 1), (39, 31), maze)[0]) #part 1 answer
print(len(BFS((1, 1), None, maze, 50)[1])) #part 2 answer
